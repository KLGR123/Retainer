import requests
from copy import deepcopy
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI, RateLimitError, APIConnectionError, AuthenticationError

from .utils import *
from .memory import Memory


class BaseNode(ABC):
    def __init__(self, memory: Memory):
        self.memory = memory

    @abstractmethod
    def step(self, *args, **kwargs):
        pass


class LLMNode(ABC):
    def __init__(self, openai_api_key, 
        model: str, 
        temperature: float, 
        memory: Memory,
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
        memory: Memory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0, 
        k: int = 3
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.k = k
        self.plan_switch_prompt = read_file("modules/prompts/plan_switch.md")
        self.plan_switch_format = load_json("modules/formats/plan_switch.json")

    def step(self, query: str):
        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_[:self.k]
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


class PlanWritingNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: Memory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.1, 
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.plan_writing_format = load_json("modules/formats/plan_writing.json")

    def step(self, query: str):
        self.memory.add(role="user", content=query)
        
        completion =  self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.memory.memory,
            response_format=self.plan_writing_format
        )

        response = completion.choices[0].message.content
        response_dict = json.loads(response)
        response_dict = json.loads(json.dumps(response_dict).replace('\\n', ''))
        dump_json("assets/plan.json", response_dict) # TODO

        self.memory.add(role="assistant", content=response)
        return response


class PlanAnswerNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: Memory,
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
                yield content

        self.memory.add(role="assistant", content="".join(response))


class ReadPlanNode(BaseNode):
    def __init__(self, memory: Memory):
        super().__init__(memory)

    def step(self):
        plan = load_json("assets/plan.json") # TODO
        response = "当前已有策划案内容如下：\n" + str(plan) if plan else "当前没有策划案，请先生成。"
        self.memory.add(role="assistant", content=response)
        return response


class CodeWritingNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: Memory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.code_writing_format = load_json("modules/formats/code_writing.json")

    def step(self, filename: str):
        memory_ = deepcopy(self.memory.memory)
        codes = load_json("assets/code_buffer.json") # TODO

        if codes.get(filename):
            memory_.append({"role": "assistant", "content": f"现在，请生成或修改{filename}文件的代码。该文件已有代码内容如下：\n{codes[filename]}"})
        else:
            memory_.append({"role": "assistant", "content": f"现在，请生成或修改{filename}文件的代码。当前该代码文件为空。"})
        
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=memory_,
            response_format=self.code_writing_format
        )

        response = completion.choices[0].message.content
        print(f"CODE WRITING INTO {filename}:\n", response)
        codes[filename] = json.loads(response)["code"]
        dump_json("assets/code_buffer.json", codes) # TODO
        self.memory.add(role="assistant", content=response)
        return response


class CodeInsightNode(LLMNode):
    # Deprecated

    def __init__(self, openai_api_key,
        memory: Memory,
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
                yield content

        self.memory.add(role="assistant", content="".join(response))


class CodeRankingNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: Memory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.1,
        k: int = 1
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.code_ranking_prompt = read_file("modules/prompts/code_ranking.md")
        self.code_ranking_format = load_json("modules/formats/code_ranking.json")
        self.k = k

    def step(self, query: str):
        self.memory.add(role="system", content=self.code_ranking_prompt)
        self.memory.add(role="user", content=query)
        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_ if len(memory_) <= self.k else [memory_[0]] + memory_[-self.k:]

        codes = load_json("assets/code_buffer.json") # TODO
        codes_json = "当前已有代码文件如下：\n" + str(codes) if codes else "当前没有代码，请先生成。"
        memory_.append({"role": "assistant", "content": codes_json})

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
        memory: Memory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.0, 
        k: int = 1
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.k = k
        self.code_switch_prompt = read_file("modules/prompts/code_switch.md")
        self.code_switch_format = load_json("modules/formats/code_switch.json")

    def step(self, query: str):
        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_ if len(memory_) <= self.k else [memory_[0]] + memory_[-self.k:]
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
        memory: Memory,
        model: str = "gpt-4o-2024-08-06", 
        temperature: float = 0.2,
        k: int = 3
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.k = k

    def step(self, query: str):
        self.memory.add(role="user", content=query)

        memory_ = deepcopy(self.memory.memory)
        memory_ = memory_ if len(memory_) <= self.k else [memory_[0]] + memory_[-self.k:]
        codes = load_json("assets/code_buffer.json") # TODO
        codes_json = "当前已有代码文件如下：\n" + str(codes) if codes else "当前没有代码，请先生成。"
        memory_.append({"role": "assistant", "content": codes_json})

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
                yield content

        self.memory.add(role="assistant", content="".join(response))


class ImgGenNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: Memory,
        model: str = "gpt-4o-2024-08-06",
        img_model: str = "dall-e-3",
        size: str = "1792x1024",
        quality: str = "standard",
        temperature: float = 0.2
    ):
        super().__init__(openai_api_key, model, temperature, memory)
        self.img_gen_format = load_json("modules/formats/img_gen.json")
        self.size = size
        self.img_model = img_model
        self.quality = quality

    def step(self, query: str):
        self.memory.add(role="user", content=query)

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.memory.memory,
            response_format=self.img_gen_format
        )

        response = completion.choices[0].message.content
        response_dict = json.loads(response)
        dump_json("assets/images.json", response_dict) # TODO

        for item in response_dict["images"]:
            prompt = item["prompt"]
            filename = item["filename"] 
            img_type = item["type"]

            assert ".png" in filename
            yield f"{filename}"

            completion = self.client.images.generate(
                model=self.img_model,
                prompt=prompt,
                size=self.size,
                quality=self.quality,
                n=1,
            )

            image_url = completion.data[0].url
            response = requests.get(image_url) # return base64

            if response.status_code == 200:
                with open(f"assets/images/{filename}", "wb") as f: # TODO
                    f.write(response.content)

            if img_type == 0:
                remove_bg_with_rembg(f"assets/images/{filename}", f"assets/images/{filename}")
        
        return list("已生成图片。")


class SceneGenNode(LLMNode):
    def __init__(self, openai_api_key, 
        memory: Memory,
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
        dump_json("assets/scripts/SampleScene.json", response_dict) # TODO
        return 