import functools

from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings

from llama_index.core.storage.chat_store import SimpleChatStore
# from llama_index.storage.chat_store.upstash import UpstashChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool

from .utils import *
from .tools.codebase import *
from .tools.scripts import *

import json
from datetime import datetime

import streamlit as st


class BaseAgent:
    def __init__(self):
        config = read_config()
        self.chat_store = SimpleChatStore()
        self.memory = ChatMemoryBuffer.from_defaults(
            token_limit=config.get("memory_token_limit"),
            chat_store=self.chat_store,
            chat_store_key=self.get_agent_key(),
        )
        self.memory_history = []
        self.tool_list = []
        self.tool_called_callback = None

    @staticmethod
    def get_agent_key():
        raise NotImplementedError("AGENT: NO AGENT TYPE DEFINED.")

    def set_tool_called_callback(self, callback):
        self.tool_called_callback = callback

    def _wrap_tool(self, tool_fn):
        @functools.wraps(tool_fn)
        def wrapped_tool(*args, **kwargs):
            if self.tool_called_callback:
                self.tool_called_callback(tool_fn.__name__)
                self.tool_list.append(tool_fn.__name__)
            return tool_fn(*args, **kwargs)
        return wrapped_tool

    def stream_chat(self, prompt):
        return self.agent.stream_chat(prompt)
    
    def get_tool_list(self):
        return self.tool_list

    def save_memory_to_chat_store(self, persist_path="./memory/chat_store.json"):
        self.chat_store.persist(persist_path)

    def load_chatstore_memory(self, persist_path="./memory/chat_store.json"):
        return self.chat_store.from_persist_path(persist_path) 

    def convert_chat_store_to_str(self):
        return json.dumps(self.chat_store.dict(), ensure_ascii=False)
    
    def load_chatstore_str(self, chat_store_string: str):
        return self.chat_store.parse_raw(chat_store_string)
    
    def get_current_history(self, chat_store_persist_path="./memory/chat_store.json"):
        timestamp = get_current_timestamp()
        current_tool_list = self.get_tool_list()
        self.save_memory_to_chat_store(persist_path=chat_store_persist_path)
        chatstore_dict = json.loads(self.convert_chat_store_to_str())

        chat_store_key = list(chatstore_dict['store'].keys())[0]
        user_content = next((msg['content'] for msg in chatstore_dict['store'][chat_store_key] if msg['role'] == 'user'), None)
        assistant_content = next((msg['content'] for msg in chatstore_dict['store'][chat_store_key] if msg['role'] == 'assistant'), None)

        history_dict = {
            timestamp: {
                "history": {
                    "chat_store_key": chat_store_key,
                    "user_content": user_content,
                    "assistant_content": assistant_content,
                    "class_name": chatstore_dict['class_name'],
                    "tool_used": str(current_tool_list)
                }
            }
        }

        if chat_store_key == 'code_agent':
            history_dict[timestamp]['codebase_info'] = {
                "entire_codebase": read_entire_codebase()
            }
        
        if chat_store_key == 'plan_agent':
            history_dict[timestamp]['planning_info'] = {
                "entire_planning": read_entire_planning()
            }

        return history_dict

    def save_current_history_to_memory(self, current_history: dict):
        self.memory_history.append(current_history)

    def save_current_history_to_json(self, current_history: dict, 
        filename='./memory/history_cache.json'
    ):
        history = load_json(filename)
        history.append(current_history)
        save_to_json(history, filename)

    def get_entire_memory_history(self):
        return self.memory_history

    def save_entire_history_to_json(self, memory_history: list, 
        filename='./memory/history_full.json'
    ):
        save_to_json(memory_history, filename)


class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        config = read_config()
        Settings.llm = OpenAI(model=config.get("codebase_model"), 
            temperature=config.get("code_temperature"), 
            api_key=st.secrets["openai_api_key"]
        )

        self.tools = [
            FunctionTool.from_defaults(fn=self._wrap_tool(write_code_to_file)),
            FunctionTool.from_defaults(fn=self._wrap_tool(read_code_from_file)),
            FunctionTool.from_defaults(fn=self._wrap_tool(read_entire_planning)),
            FunctionTool.from_defaults(fn=self._wrap_tool(delete_file_from_codebase)),
        ]

        with open("modules/prompts/codebase_base.md", "r", encoding="utf-8") as f:
            self.base_prompt = f.read()

        self.agent = ReActAgent.from_tools(
            self.tools,
            verbose=True,
            context=self.base_prompt,
            max_iterations=50,
            memory=self.memory,
        )

    @staticmethod
    def get_agent_key():
        return "code_agent"

    def add_rejected_change_to_memory(self, selected_file: str):
        """Add a record of a rejected change to the memory."""
        timestamp = get_current_timestamp()
        chatstore_dict = json.loads(self.convert_chat_store_to_str())
        rejected_change_record = {
            timestamp: {
                "history": {
                    "chat_store_key": "human",
                    "user_content": f"已废除 {selected_file} 的改动。",
                    # "assistant_content": "",
                    "class_name": chatstore_dict['class_name'],
                    "tool_used": "['discard_change']"
                },
                "codebase_info": {
                    "discarded_file": selected_file
                }
            }
        }
        return rejected_change_record


class PlanAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        config = read_config()
        Settings.llm = OpenAI(model=config.get("plan_model"), 
            temperature=config.get("plan_temperature"), 
            api_key=st.secrets["openai_api_key"]
        )

        self.tools = [
            FunctionTool.from_defaults(fn=self._wrap_tool(write_gameplay_script)),
            FunctionTool.from_defaults(fn=self._wrap_tool(write_scene_script)),
            FunctionTool.from_defaults(fn=self._wrap_tool(read_entire_planning)),
        ]

        with open("modules/prompts/plan_base.md", "r", encoding="utf-8") as f:
            self.base_prompt = f.read()
        
        self.agent = ReActAgent.from_tools(
            self.tools,
            verbose=True,
            context=self.base_prompt,
            max_iterations=20,
            memory=self.memory,
        )

    @staticmethod
    def get_agent_key():
        return "plan_agent"