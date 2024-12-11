from omegaconf import OmegaConf

from .nodes import *
from .utils import *
from .memory import BaseMemory


class PlanPipeline:
    def __init__(self):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key

        self.plan = {}
        self.plan_history = [{}] # TODO
        self.plan_memory = BaseMemory(openai_api_key=openai_api_key, **cfg.plan_memory)
        self.plan_base_prompt = read_file("modules/prompts/plan_base.md")
        self.plan_memory.add(role="system", content=self.plan_base_prompt)
        
        self.plan_switch_node = PlanSwitchNode(openai_api_key, memory=self.plan_memory, **cfg.plan_switch)
        self.plan_write_node = PlanWriteNode(openai_api_key, memory=self.plan_memory, **cfg.plan_write)
        self.plan_answer_node = PlanAnswerNode(openai_api_key, memory=self.plan_memory, **cfg.plan_answer)

    def step(self, query: str) -> dict:
        mode = self.plan_switch_node.step(query)
        result = {"mode": mode, "plan": self.plan, "response": None}

        if mode == 0:
            self.plan = self.plan_write_node.step(query)
            result.update({"plan": self.plan})
            self.plan_history.append(self.plan)
        else:
            result.update({"response": self.plan_answer_node.step(query)}) # TODO
            self.plan_history.append(self.plan_history[-1])

        return result
    
    def revert(self):
        if len(self.plan_memory.memory) <= 2:
            self.restart()
        else:
            self.plan_memory.pop(2)
            self.plan_history.pop()
            self.plan = self.plan_history[-1]

    def restart(self):
        self.plan_history = [{}] # TODO
        self.plan = {}
        self.plan_memory.clear()
        self.plan_memory.add(role="system", content=self.plan_base_prompt)

    def load_plan(self, plan: dict):
        assert all(key in plan["游戏策划"] for key in ["所需代码", "游戏玩法", "所需素材"])
        self.plan = plan


class CodePipeline:
    def __init__(self, plan: dict):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key

        self.code = {}
        self.code_history = [{}] # TODO
        self.revert_steps = []
        self.code_memory = BaseMemory(openai_api_key=openai_api_key, **cfg.code_memory)
        self.code_base_prompt = read_file("modules/prompts/code_base.md")
        self.code_memory.add(role="system", content=self.code_base_prompt)
        self.code_write_prompt = read_file("modules/prompts/code_write.md")

        self.plan_read_node = PlanReadNode(memory=self.code_memory)
        self.code_write_node = CodeWriteNode(openai_api_key, memory=self.code_memory, **cfg.code_write)
        self.code_answer_node = CodeAnswerNode(openai_api_key, memory=self.code_memory, **cfg.code_answer)
        self.code_switch_node = CodeSwitchNode(openai_api_key, memory=self.code_memory, **cfg.code_switch)
        self.code_ranking_node = CodeRankingNode(openai_api_key, memory=self.code_memory, **cfg.code_ranking)
        self.code_insight_node = CodeInsightNode(openai_api_key, memory=self.code_memory, **cfg.code_insight)

        self.plan = plan
        assert all(key in self.plan["游戏策划"] for key in ["所需代码", "游戏玩法", "所需素材"])
        self.plan_read_node.step(self.plan)

    def load_code(self, code: dict):
        self.code = code
        self.code_history[-1] = self.code
    
    def init_step(self) -> dict:
        self.code_memory.add(role="system", content=self.code_write_prompt)
        commit_files = list(self.plan["游戏策划"]["所需代码"].keys())

        for filename in commit_files:
            # yield f"{filename}" TODO
            self.code = self.code_write_node.step(self.code, filename)

        self.revert_steps.append(len(commit_files) + 1)
        self.code_history.append(self.code)
        return {"code": self.code, "mode": 0, "response": None}

    def insight_step(self):
        self.revert_steps.append(2)
        self.code_history.append(self.code_history[-1])
        return {"mode": 1, "response": self.code_insight_node.step(), "code": self.code}

    def step(self, query: str) -> dict:
        mode = self.code_switch_node.step(query)
        result = {"mode": mode, "code": self.code, "response": None}

        if mode == 0:
            commit_files = self.code_ranking_node.step(self.code, query)
            assert all(filename in self.code.keys() for filename in commit_files) # TODO
            
            for filename in commit_files:
                # yield f"{filename}" TODO
                self.code = self.code_write_node.step(self.code, filename)

            result.update({"code": self.code})
            self.revert_steps.append(len(commit_files) + 3)
            self.code_history.append(self.code)
        else:
            result.update({"response": self.code_answer_node.step(self.code, query)})
            self.revert_steps.append(2)
            self.code_history.append(self.code_history[-1])

        return result
        
    def revert(self):
        if len(self.code_memory.memory) <= 3:
            self.restart()
        else:
            self.code_memory.pop(self.revert_steps.pop())
            self.code_history.pop()
            self.code = self.code_history[-1]
    
    def restart(self):
        self.code_history = [{}] # TODO
        self.code = {}
        self.code_memory.clear()
        self.code_memory.add(role="system", content=self.code_base_prompt)
        self.plan_read_node.step(self.plan)
        

class ImagePipeline:
    def __init__(self, plan: dict):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key

        self.images = {}
        self.images_history = [{}] # TODO
        self.revert_steps = []
        self.image_gen_memory = BaseMemory(openai_api_key=openai_api_key, **cfg.image_gen_memory)
        self.image_base_prompt = read_file("modules/prompts/image_base.md")
        self.image_gen_memory.add(role="system", content=self.image_base_prompt)

        self.plan_read_node = PlanReadNode(memory=self.image_gen_memory)
        self.image_gen_node = ImageGenNode(openai_api_key, memory=self.image_gen_memory, **cfg.image_gen)
        self.image_ranking_node = ImageRankingNode(openai_api_key, memory=self.image_gen_memory, **cfg.image_ranking)

        self.plan = plan
        assert all(key in self.plan["游戏策划"] for key in ["所需代码", "游戏玩法", "所需素材"])
        self.plan_read_node.step(self.plan)

    def load_images(self, images: dict):
        self.images = images
        self.images_history[-1] = self.images

    def init_step(self) -> dict:
        commit_files = list(self.plan["游戏策划"]["所需素材"].keys())

        for filename in commit_files:
            # yield f"{filename}" TODO
            self.images = self.image_gen_node.step(self.images, filename)

        self.revert_steps.append(len(commit_files) * 2)
        self.images_history.append(self.images)
        return self.images

    def step(self, query: str) -> dict:
        commit_files = self.image_ranking_node.step(self.images, query)

        for filename in commit_files:
            # yield f"{filename}" TODO
            self.images = self.image_gen_node.step(self.images, filename)

        self.revert_steps.append(len(commit_files) * 2 + 3)
        self.images_history.append(self.images)
        return self.images

    def remove_background(self):
        for filename in self.images.keys():
            if self.images[filename]["type"] == 0:
                self.images[filename]["image"] = remove_background(self.images[filename]["image"])
        
        return self.images

    def revert(self):
        if len(self.image_gen_memory.memory) <= 3:
            self.restart()
        else:
            self.image_gen_memory.pop(self.revert_steps.pop())
            self.images_history.pop()
            self.images = self.images_history[-1]

    def restart(self):
        self.image_gen_memory.clear()
        self.image_gen_memory.add(role="system", content=self.image_base_prompt)
        self.plan_read_node.step(self.plan)
        self.images_history = [{}] # TODO
        self.images = {}


class ScenePipeline: # TODO
    def __init__(self, plan: dict):
        cfg = OmegaConf.load("config.yaml")
        openai_api_key = cfg.openai_api_key

        self.plan = plan
        self.scene_gen_memory = BaseMemory(openai_api_key=openai_api_key, **cfg.scene_gen_memory)
        self.scene_gen_prompt = read_file("modules/prompts/scene_gen.md")

        self.scene_gen_node = SceneGenNode(openai_api_key, memory=self.scene_gen_memory, **cfg.scene_gen)
        self.scene_gen_memory.add(role="system", content=self.scene_gen_prompt)
        self.plan_read_node = PlanReadNode(memory=self.scene_gen_memory)
        self.plan_read_node.step(plan)
        
    def step(self):
        self.restart()
        self.plan_read_node.step()
        scene = self.scene_gen_node.step()
        return scene

    def restart(self):
        self.scene_gen_memory.clear()
        self.scene_gen_memory.add(role="system", content=self.scene_gen_prompt)
        self.plan_read_node.step(self.plan)