import tiktoken
from openai import OpenAI

from .utils import *


class BaseMemory:
    def __init__(self, 
        openai_api_key: str, 
        model: str = "gpt-4o",
        max_tokens: int = 128000, 
        compressed_tokens: int = 8000,
        temperature: float = 0.3
    ):
        self.memory = []
        self.temperature = temperature
        self.model = model
        self.max_tokens = max_tokens
        self.compressed_tokens = compressed_tokens

        self.client = OpenAI(api_key=openai_api_key)
        self.summarize_history_prompt = read_file("modules/prompts/memory.md")
    
    def count_memory_tokens(self, skip_first=False) -> int:
        start_idx = 1 if skip_first and len(self.memory) > 0 else 0
        return sum(msg["tokens"] for msg in self.memory[start_idx:])
    
    def summarize_history(self) -> str:
        assert len(self.memory) > 1 
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.memory[1:]])

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.summarize_history_prompt},
                {"role": "user", "content": history_text}
            ],
            temperature=self.temperature,
            max_tokens=self.compressed_tokens
        )

        return response.choices[0].message.content
    
    def add(self, role: str, content: str) -> None:
        tokens = count_tokens(content)

        self.memory.append({
            "role": role,  
            "content": content,
            "tokens": tokens
        })
        
        if self.count_memory_tokens(skip_first=False) > self.max_tokens:
            first_message = self.memory[0]
            summary = self.summarize_history()
            summary_tokens = count_tokens(summary)
            self.memory = [first_message]
            self.memory.append({
                "role": "system",
                "content": f"历史对话总结如下：\n{summary}",
                "tokens": summary_tokens
            })
        else:
            pass

    def pop(self, length: int = 1) -> None:
        if self.memory:
            for _ in range(length):
                self.memory.pop()
        else:
            pass
    
    def clear(self) -> None:
        self.memory = []

    def load_memory(self, memory: list) -> None:
        assert all("role" in item and "content" in item and "tokens" in item for item in memory)
        self.memory = memory


if __name__ == "__main__":
    memory = BaseMemory(openai_api_key="", model="gpt-4o")
    memory.add("user", "Hello, how are you?")
    memory.add("assistant", "I'm fine, thank you!")
    print(memory.memory)