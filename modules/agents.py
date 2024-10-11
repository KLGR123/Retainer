import functools

from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings

from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.storage.chat_store.upstash import UpstashChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool

from .utils import read_config
from .tools.codebase import *
from .tools.scripts import *


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

        self.intent_history: List[str] = []
        self.tool_history: List[dict] = []
        self.response_history: List[str] = []

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
            # memory=self.memory,
        )

        # self.memory = self.agent.memory
        self.tool_called_callback = None

    def set_tool_called_callback(self, callback):
        self.tool_called_callback = callback

    def _wrap_tool(self, tool_fn):
        @functools.wraps(tool_fn)
        def wrapped_tool(*args, **kwargs):
            if self.tool_called_callback:
                self.tool_called_callback(tool_fn.__name__)
                # TODO
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
        #     f.write("\ncoding agent:")
        #     f.write(memory_str)
        pass


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

        self.intent_history: List[str] = []
        self.tool_history: List[dict] = []
        self.response_history: List[str] = []

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
            # memory=self.memory,
        )
        
        # self.memory = self.agent.memory
        self.tool_called_callback = None

    def set_tool_called_callback(self, callback):
        self.tool_called_callback = callback

    def _wrap_tool(self, tool_fn):
        @functools.wraps(tool_fn)
        def wrapped_tool(*args, **kwargs):
            if self.tool_called_callback:
                self.tool_called_callback(tool_fn.__name__)
                # TODO
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
