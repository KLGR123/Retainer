from omegaconf import OmegaConf

from .nodes import *
from .memory import Memory
from .utils import *


class PlanPipeline:
    def __init__(self):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key

        self.plan_memory = Memory(openai_api_key=openai_api_key, **cfg.plan_memory)
        self.plan_base_prompt = read_file("modules/prompts/plan_base.md")
        self.plan_memory.add(role="system", content=self.plan_base_prompt)
        
        self.plan_switch_node = PlanSwitchNode(openai_api_key, memory=self.plan_memory, **cfg.plan_switch)
        self.plan_writing_node = PlanWritingNode(openai_api_key, memory=self.plan_memory, **cfg.plan_writing)
        self.plan_answer_node = PlanAnswerNode(openai_api_key, memory=self.plan_memory, **cfg.plan_answer)

    def step(self, query: str):
        mode = self.plan_switch_node.step(query)
        if mode == 0:
            return self.plan_writing_node.step(query)
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
        self.code_answer_node = CodeAnswerNode(openai_api_key, memory=self.code_memory, **cfg.code_answer)
        self.code_switch_node = CodeSwitchNode(openai_api_key, memory=self.code_memory, **cfg.code_switch)
        self.code_ranking_node = CodeRankingNode(openai_api_key, memory=self.code_memory, **cfg.code_ranking)

        self.step_memory_count = 0

        if not os.path.exists("assets/code_memo.json"): # TODO
            dump_json("assets/code_memo.json", {})
        
        if not os.path.exists("assets/code_buffer.json"): # TODO
            dump_json("assets/code_buffer.json", {})

    def init_step(self):
        initial_memory_len = len(self.code_memory.memory)
        self.read_plan_node.step()
        self.code_memory.add(role="system", content=self.code_writing_prompt)

        plan_ = load_json("assets/plan.json") # TODO
        code_files = list(plan_["游戏策划"]["所需代码"].keys())

        code_buffer = load_json("assets/code_buffer.json") # TODO
        keys_to_remove = [key for key in code_buffer.keys() if key not in code_files]
        for key in keys_to_remove:
            code_buffer.pop(key)

        dump_json("assets/code_buffer.json", code_buffer) # TODO
        dump_json("assets/code_memo.json", code_buffer) # TODO

        for filename in code_files:
            yield f"{filename}"
            self.code_writing_node.step(filename)

        self.step_memory_count = len(self.code_memory.memory) - initial_memory_len
        return list("已更新代码素材。")

    def insight_step(self):
        return self.code_insight_node.step()

    def step(self, query: str):
        initial_memory_len = len(self.code_memory.memory)
        mode = self.code_switch_node.step(query)

        if mode == 0:
            code_files = self.code_ranking_node.step(query)
            for filename in code_files:
                # yield f"{filename}"
                self.code_writing_node.step(filename)

            return list("已更新代码素材。")
        else:
            return self.code_answer_node.step(query)

        self.step_memory_count = len(self.code_memory.memory) - initial_memory_len
        
    def pop_step(self):
        for _ in range(self.step_memory_count):
            self.code_memory.pop()
        self.step_memory_count = 0


class ImgGenPipeline:
    def __init__(self):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key
        
        self.img_memory = Memory(openai_api_key=openai_api_key, **cfg.img_memory)
        self.img_base_prompt = read_file("modules/prompts/img_gen_base.md")
        self.img_memory.add(role="system", content=self.img_base_prompt)
        
        self.read_plan_node = ReadPlanNode(memory=self.img_memory)
        self.read_plan_node.step()

        self.img_gen_node = ImgGenNode(openai_api_key, memory=self.img_memory, **cfg.img_gen)
        
    def step(self, query: str):
        try:
            return self.img_gen_node.step(query)
        except requests.exceptions.RequestException as e:
            return ["网络错误，请重试。"]


class SceneGenPipeline:
    def __init__(self):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key

        self.scene_gen_memory = Memory(openai_api_key=openai_api_key, **cfg.scene_gen_memory)
        self.scene_gen_prompt = read_file("modules/prompts/scene_gen.md")

        self.scene_gen_node = SceneGenNode(openai_api_key, memory=self.scene_gen_memory, **cfg.scene_gen)
        self.scene_gen_memory.add(role="system", content=self.scene_gen_prompt)
        self.read_plan_node = ReadPlanNode(memory=self.scene_gen_memory)
        
    def step(self):
        self.read_plan_node.step()
        self.scene_gen_node.step()