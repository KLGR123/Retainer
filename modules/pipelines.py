from omegaconf import OmegaConf

from .nodes import *
from .memory import Memory
from .utils import *


class PlanPipeline:
    def __init__(self, openai_api_key):
        cfg = OmegaConf.load("config.yaml")

        self.plan_memory = Memory(openai_api_key=openai_api_key, **cfg.plan_memory)
        self.plan_base_prompt = read_file("modules/prompts/plan_base.md")
        self.plan_memory.add(role="system", content=self.plan_base_prompt)
        
        self.plan_switch_node = PlanSwitchNode(openai_api_key, memory=self.plan_memory, **cfg.plan_switch)
        self.plan_writing_node = PlanWritingNode(openai_api_key, memory=self.plan_memory, **cfg.plan_writing)
        self.plan_answer_node = PlanAnswerNode(openai_api_key, memory=self.plan_memory, **cfg.plan_answer)

    def step(self, query: str):
        mode = self.plan_switch_node.step(query)
        if mode == 0:
            self.plan_writing_node.step(query)
            return list("已更新游戏策划。")
        else:
            return self.plan_answer_node.step(query)


class CodePipeline:
    def __init__(self, openai_api_key):
        cfg = OmegaConf.load("config.yaml")

        self.code_memory = Memory(openai_api_key=openai_api_key, **cfg.code_memory)
        self.code_base_prompt = read_file("modules/prompts/codebase_base.md")
        self.code_memory.add(role="system", content=self.code_base_prompt)

        self.code_writing_prompt = read_file("modules/prompts/code_writing.md")

        self.read_plan_node = ReadPlanNode(memory=self.code_memory)
        self.code_writing_node = CodeWritingNode(openai_api_key, memory=self.code_memory, **cfg.code_writing)
        self.code_insight_node = CodeInsightNode(openai_api_key, memory=self.code_memory, **cfg.code_insight)

        self.step_memory_count = 0

    def init_step(self):
        if not os.path.exists("assets/code.json"):
            dump_json("assets/code.json", {})

        initial_memory_len = len(self.code_memory.memory)
        self.read_plan_node.step()
        self.code_memory.add(role="system", content=self.code_writing_prompt)

        plan_ = load_json("assets/plan.json")
        code_files = list(plan_["游戏策划"]["所需代码"].keys())

        for filename in code_files:
            yield f"{filename}"
            self.code_writing_node.step(filename)

        self.step_memory_count = len(self.code_memory.memory) - initial_memory_len
        return list("已更新代码素材。")

    def insight_step(self):
        return self.code_insight_node.step()

    def step(self, query: str):
        initial_memory_len = len(self.code_memory.memory)
        # TODO
        self.step_memory_count = len(self.code_memory.memory) - initial_memory_len
        return list("已更新代码素材。")
    
    def pop_step(self):
        for _ in range(self.step_memory_count):
            self.code_memory.pop()
        self.step_memory_count = 0
