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

from .utils import read_config
from .tools.codebase import *
from .tools.scripts import *

import json
from datetime import datetime


class CodeAgent:
    def __init__(self, memory_token_limit=5000):
        config = read_config()
        Settings.llm = OpenAI(model=config.get("codebase_model"), 
            temperature=config.get("code_temperature"), 
            api_key=config.get("openai_api_key")
        )

        self.chat_store = SimpleChatStore()
        self.memory = ChatMemoryBuffer.from_defaults(
            token_limit=memory_token_limit,
            chat_store=self.chat_store,
            chat_store_key="code_agent",
        )

        # self.intent_history: List[str] = []
        # self.tool_history: List[dict] = []
        # self.response_history: List[str] = []

        self.memory_history: List[dict] = []

        self.tools = [
            FunctionTool.from_defaults(fn=self._wrap_tool(write_code_to_file)),
            FunctionTool.from_defaults(fn=self._wrap_tool(read_code_from_file)),
            # FunctionTool.from_defaults(fn=self._wrap_tool(read_entire_codebase)),
            # FunctionTool.from_defaults(fn=self._wrap_tool(delete_file_from_codebase)),
            FunctionTool.from_defaults(fn=self._wrap_tool(read_entire_planning)),
            # FunctionTool.from_defaults(fn=self._wrap_tool(query_codebase_content)),
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

        # self.memory = self.agent.memory
        self.tool_called_callback = None
        self.tool_list = []

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
        chat_store_string = json.dumps(self.chat_store.dict(), ensure_ascii=False)
        return chat_store_string
    
    def load_chatstore_str(self,chat_store_string):
        return self.chat_store.parse_raw(chat_store_string)
    
    # Get the current message and tool usage history.
    def get_current_history(self, chat_store_persist_path="./memory/chat_store.json"):
        timestamp = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        current_tool_list = self.get_tool_list()
        self.save_memory_to_chat_store(persist_path=chat_store_persist_path)
        chatstore_str = self.convert_chat_store_to_str()
        chatstore_dict = json.loads(chatstore_str)
        print("chatstore_str:",chatstore_str)
        print("chatstore_dict:",chatstore_dict)
        # Extract the chat store key, user content, and assistant content
        chat_store_key = list(chatstore_dict['store'].keys())[0]
        user_content = next((msg['content'] for msg in chatstore_dict['store'][chat_store_key] if msg['role'] == 'user'), None)
        assistant_content = next((msg['content'] for msg in chatstore_dict['store'][chat_store_key] if msg['role'] == 'assistant'), None)

        current_history = {
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
        return current_history

    def save_current_history_to_memory(self, current_history):
        self.memory_history.append(current_history)

    def save_current_history_to_json(self, current_history, filename='./memory/plan_history_cache.json'):
        # Load the existing history
        history = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                history = json.load(f)

        # Append the current history
        history.append(current_history)

        # Write the history to the JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False)

        print("Saved current history to", filename)


    def get_entire_memory_history(self):
        return self.memory_history

    def save_entire_history_to_json(self, memory_history, filename='./memory/code_history_full.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(memory_history, f, ensure_ascii=False)
            f.write('\n')
        print("Saved entire history memory",filename)

class PlanAgent:
    def __init__(self, memory_token_limit=5000):
        config = read_config()
        Settings.llm = OpenAI(model=config.get("plan_model"), 
            temperature=config.get("plan_temperature"), 
            api_key=config.get("openai_api_key")
        )

        self.chat_store = SimpleChatStore()
        self.memory = ChatMemoryBuffer.from_defaults(
            token_limit=memory_token_limit,
            chat_store=self.chat_store,
            chat_store_key="plan_agent",
        )

        self.memory_history: List[dict] = []

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
            max_iterations=50,
            memory=self.memory,
        )
        
        # self.memory = self.agent.memory
        self.tool_called_callback = None
        self.tool_list = []

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

    def get_memory(self):
        # return self.memory.get()
        pass
    
    def store_memory(self):
        # memory_str = str(self.get_memory())
        # with open('memory.txt', 'a') as f:
        #     f.write("\nplanning agent:")
        #     f.write(memory_str)
        pass
    
    def get_tool_list(self):
        return self.tool_list

    def save_memory_to_chat_store(self, persist_path="./memory/chat_store.json"):
        self.chat_store.persist(persist_path)

    def load_chatstore_memory(self, persist_path="memory/chat_store.json"):
        return self.chat_store.from_persist_path(persist_path) 

    def convert_chat_store_to_str(self):
        chat_store_string = json.dumps(self.chat_store.dict(), ensure_ascii=False)
        return chat_store_string
    
    def load_chatstore_str(self,chat_store_string):
        return self.chat_store.parse_raw(chat_store_string)
    
    # Get the current message and tool usage history.
    def get_current_history(self, chat_store_persist_path="./memory/chat_store.json"):
        timestamp = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        current_tool_list = self.get_tool_list()
        self.save_memory_to_chat_store(persist_path=chat_store_persist_path)
        chatstore_str = self.convert_chat_store_to_str()
        chatstore_dict = json.loads(chatstore_str)

        # Extract the chat store key, user content, and assistant content
        chat_store_key = list(chatstore_dict['store'].keys())[0]
        user_content = next((msg['content'] for msg in chatstore_dict['store'][chat_store_key] if msg['role'] == 'user'), None)
        assistant_content = next((msg['content'] for msg in chatstore_dict['store'][chat_store_key] if msg['role'] == 'assistant'), None)

        current_history = {
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
        return current_history

    def save_current_history_to_memory(self, current_history):
        self.memory_history.append(current_history)

    def save_current_history_to_json(self, current_history, filename='./memory/plan_history_cache.json'):
        # Load the existing history
        history = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                history = json.load(f)

        # Append the current history
        history.append(current_history)

        # Write the history to the JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False)

        print("Saved current history to",filename)


    def get_entire_memory_history(self):
        return self.memory_history

    def save_entire_history_to_json(self, memory_history, filename='./memory/code_history_full.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(memory_history, f, ensure_ascii=False)
            f.write('\n')
        print("Saved entire history memory to",filename)