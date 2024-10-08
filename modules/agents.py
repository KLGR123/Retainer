from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings

from .utils import read_config
from .tools.codebase import *
from .tools.scripts import *


class CodeAgent:
    def __init__(self):
        config = read_config()
        Settings.llm = OpenAI(model=config.get("code_model"), 
            temperature=config.get("code_temperature"), 
            api_key=config.get("openai_api_key")
        )
    
        self.tools = [
            FunctionTool.from_defaults(fn=write_code_to_file),
            FunctionTool.from_defaults(fn=read_code_from_file),
            FunctionTool.from_defaults(fn=read_entire_codebase),
            FunctionTool.from_defaults(fn=delete_file_from_codebase),
            # FunctionTool.from_defaults(fn=query_codebase_content),
        ]

        with open("modules/prompts/codebase_base.md", "r", encoding="utf-8") as f:
            self.base_prompt = f.read()

        self.agent = ReActAgent.from_tools(
            self.tools,
            verbose=True,
            context=self.base_prompt,
        )

        self.memory = self.agent.memory

    def stream_chat(self, prompt):
        return self.agent.stream_chat(prompt)
        

class PlanAgent:
    def __init__(self):
        config = read_config()
        Settings.llm = OpenAI(model=config.get("plan_model"), 
            temperature=config.get("plan_temperature"), 
            api_key=config.get("openai_api_key")
        )
        
        self.tools = [
            FunctionTool.from_defaults(fn=write_gameplay_script),
            FunctionTool.from_defaults(fn=write_scene_script),
            FunctionTool.from_defaults(fn=read_entire_planning),
        ]

        with open("modules/prompts/plan_base.md", "r", encoding="utf-8") as f:
            self.base_prompt = f.read()

        self.agent = ReActAgent.from_tools(
            self.tools,
            verbose=True,
            context=self.base_prompt,
        )
        
        self.memory = self.agent.memory

    def stream_chat(self, prompt):
        return self.agent.stream_chat(prompt)