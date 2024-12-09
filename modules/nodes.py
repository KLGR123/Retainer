import requests
from copy import deepcopy
from openai import OpenAI
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_exponential

from .utils import *
from .memory import BaseMemory


class BaseNode(ABC):
    def __init__(self, memory: BaseMemory):
        self.memory = memory

    @abstractmethod
    def step(self, *args, **kwargs):
        pass


class LLMNode(ABC):
    def __init__(self, openai_api_key, 
        model: str, 
        temperature: float, 
        memory: BaseMemory,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
        self.temperature = temperature
        self.memory = memory
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    @abstractmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        reraise=True
    )
    def step(self, *args, **kwargs):
        pass


class PlanSwitchNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0, 
        memory_length: int = 3
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.memory_length = memory_length
        self.plan_switch_prompt = read_file("modules/prompts/plan_switch.md")
        self.plan_switch_format = load_json("modules/formats/plan_switch.json")

    def step(self, query: str):
        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_[:self.memory_length]
        memory_.append({"role": "user", "content": query})
        memory_.append({"role": "system", "content": self.plan_switch_prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=memory_,
            response_format=self.plan_switch_format
        )

        mode = json.loads(completion.choices[0].message.content)["mode"]
        assert mode in [0, 1]
        return mode


class PlanWriteNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.1, 
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        
        self.plan_write_format = load_json("modules/formats/plan_write.json")

    def step(self, query: str):
        self.memory.add(role="user", content=query)
        
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.memory.memory,
            response_format=self.plan_write_format
        )

        response = completion.choices[0].message.content
        self.memory.add(role="assistant", content=response)

        response_dict = json.loads(response)
        response_dict = json.loads(json.dumps(response_dict).replace('\\n', ''))
        return response_dict


class PlanAnswerNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.2, 
    ):
        super().__init__(openai_api_key, model, temperature, memory)

    def step(self, query: str):
        self.memory.add(role="user", content=query)

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            stream=True,
            messages=self.memory.memory
        )

        response = []
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                response.append(content)
                # yield content TODO

        full_response = "".join(response)
        self.memory.add(role="assistant", content=full_response)
        return full_response


class PlanReadNode(BaseNode):
    def __init__(self, memory: BaseMemory):
        super().__init__(memory)

    def step(self, plan: dict):
        response = "当前已有策划案内容如下：\n" + str(plan) if plan else "当前没有策划案，需要先生成。"
        self.memory.add(role="assistant", content=response)
        return response


class CodeWriteNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.code_write_format = load_json("modules/formats/code_write.json")

    def step(self, code: dict, filename: str) -> dict:
        memory_ = deepcopy(self.memory.memory)

        if code.get(filename):
            memory_.append({"role": "assistant", "content": f"现在，请生成或修改{filename}文件的代码。该文件已有代码内容如下：\n{code[filename]}"})
            assert self.memory.count_memory_tokens() + count_tokens(str(code[filename])) < 128000
        else:
            memory_.append({"role": "assistant", "content": f"现在，请生成或修改{filename}文件的代码。当前该代码文件为空。"})
        
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=memory_,
            response_format=self.code_write_format
        )

        response = completion.choices[0].message.content
        assert "code" in json.loads(response)
        code[filename] = json.loads(response)["code"]
        self.memory.add(role="assistant", content=response)
        return code


class CodeInsightNode(LLMNode):
    def __init__(self, openai_api_key,
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.5
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.code_insight_prompt = read_file("modules/prompts/code_insight.md")

    def step(self):
        self.memory.add(role="user", content=self.code_insight_prompt)

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            stream=True,
            messages=self.memory.memory
        )

        response = []
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                response.append(content)
                # yield content TODO

        full_response = "".join(response)
        self.memory.add(role="assistant", content=full_response)
        return full_response


class CodeRankingNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.1,
        memory_length: int = 1
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.code_ranking_prompt = read_file("modules/prompts/code_ranking.md")
        self.code_ranking_format = load_json("modules/formats/code_ranking.json")
        self.memory_length = memory_length

    def step(self, code: dict, query: str):
        self.memory.add(role="system", content=self.code_ranking_prompt)
        self.memory.add(role="user", content=query)

        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_ if len(memory_) <= self.memory_length else [memory_[0]] + memory_[-self.memory_length:]
        memory_.append({"role": "assistant", "content": "当前已有代码文件如下：\n" + str(code) if code else "当前没有代码，请先生成。"})
        assert self.memory.count_memory_tokens() + count_tokens(str(code)) < 128000

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=memory_,
            response_format=self.code_ranking_format
        )

        code_files = json.loads(completion.choices[0].message.content)["code_files"]
        self.memory.add(role="assistant", content=f"经过分析，对于当前用户意图：{query}，需要改动或新增的代码文件如下：\n{code_files}")
        assert isinstance(code_files, list)
        return code_files


class CodeSwitchNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0, 
        memory_length: int = 3
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.memory_length = memory_length
        self.code_switch_prompt = read_file("modules/prompts/code_switch.md")
        self.code_switch_format = load_json("modules/formats/code_switch.json")

    def step(self, query: str):
        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_ if len(memory_) <= self.memory_length else [memory_[0]] + memory_[-self.memory_length:]
        memory_.append({"role": "user", "content": query})
        memory_.append({"role": "system", "content": self.code_switch_prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=memory_,
            response_format=self.code_switch_format
        )

        mode = json.loads(completion.choices[0].message.content)["mode"]
        assert mode in [0, 1]
        return mode


class CodeAnswerNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.2,
        memory_length: int = 3
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.memory_length = memory_length

    def step(self, code: dict, query: str):
        self.memory.add(role="user", content=query)

        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_ if len(memory_) <= self.memory_length else [memory_[0]] + memory_[-self.memory_length:]
        memory_.append({"role": "assistant", "content": "当前已有代码文件如下：\n" + str(code) if code else "当前没有代码，请先生成。"})
        assert self.memory.count_memory_tokens() + count_tokens(str(code)) < 128000

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            stream=True,
            messages=memory_
        )

        response = []
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                response.append(content)
                # yield content TODO

        full_response = "".join(response)   
        self.memory.add(role="assistant", content=full_response)
        return full_response


class ImageGenNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06",
        image_gen_model: str = "dall-e-3",
        size: str = "1792x1024",
        quality: str = "standard",
        temperature: float = 0.2
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.image_gen_format = load_json("modules/formats/image_gen.json")
        self.size = size
        self.quality = quality
        self.image_gen_model = image_gen_model

    def step(self, images: dict, filename: str):
        self.memory.add(role="assistant", content=f"现在，请生成或修改{filename}图片对应的stable diffusion 生成提示词。")

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.memory.memory,
            response_format=self.image_gen_format
        )

        response = completion.choices[0].message.content
        self.memory.add(role="assistant", content=response)
        response_dict = json.loads(response)

        assert ".png" in filename

        if filename not in images:
            images[filename] = {}

        images[filename]["prompt"] = response_dict["prompt"]
        images[filename]["type"] = response_dict["type"]

        completion = self.client.images.generate(
            model=self.image_gen_model,
            prompt=response_dict["prompt"],
            size=self.size,
            quality=self.quality,
            response_format="b64_json",
            n=1,
        )

        image_base64 = completion.data[0].b64_json
        images[filename]["image"] = image_base64        
        return images


class ImageRankingNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.1,
    ):
        super().__init__(openai_api_key, model, temperature, memory)

        self.image_ranking_prompt = read_file("modules/prompts/image_ranking.md")
        self.image_ranking_format = load_json("modules/formats/image_ranking.json")

    def step(self, images: dict, query: str):
        self.memory.add(role="system", content=self.image_ranking_prompt)
        self.memory.add(role="user", content=query)

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.memory.memory,
            response_format=self.image_ranking_format
        )

        image_files = json.loads(completion.choices[0].message.content)["image_files"]
        self.memory.add(role="assistant", content=f"经过分析，对于当前用户意图：{query}，需要改动或新增的图片如下：\n{image_files}")
        assert isinstance(image_files, list)
        return image_files


class SceneGenNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: BaseMemory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.scene_gen_format = load_json("modules/formats/scene_gen.json")

    def step(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.memory.memory,
            response_format=self.scene_gen_format
        )

        response = completion.choices[0].message.content
        response_dict = json.loads(response)
        return response_dict