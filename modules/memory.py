from openai import OpenAI
import tiktoken

from .utils import *


class Memory:
    def __init__(self, openai_api_key, 
        model="gpt-4o",
        max_tokens=128000, 
        compressed_tokens=8000,
        temperature=0.3
    ):
        self.memory = []
        self.temperature = temperature
        self.model = model
        self.max_tokens = max_tokens
        self.compressed_tokens = compressed_tokens
        self.client = OpenAI(api_key=openai_api_key)
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))
    
    def count_memory_tokens(self, skip_first=False) -> int:
        start_idx = 1 if skip_first and len(self.memory) > 0 else 0
        return sum(msg["tokens"] for msg in self.memory[start_idx:])
    
    def summarize_history(self) -> str:
        assert len(self.memory) > 1 
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.memory[1:]])
        summarize_history_prompt = read_file("modules/prompts/memory.md")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": summarize_history_prompt},
                {"role": "user", "content": history_text}
            ],
            temperature=self.temperature,
            max_tokens=self.compressed_tokens
        )

        return response.choices[0].message.content
    
    def add(self, role: str, content: str) -> None:
        tokens = self.count_tokens(content)
        self.memory.append({
            "role": role,  
            "content": content,
            "tokens": tokens
        })
        
        if self.count_memory_tokens(skip_first=False) > self.max_tokens:
            first_message = self.memory[0]
            summary = self.summarize_history()
            summary_tokens = self.count_tokens(summary)
            self.memory = [first_message]
            self.memory.append({
                "role": "system",
                "content": f"历史对话总结如下：\n{summary}",
                "tokens": summary_tokens
            })

    def pop(self) -> None:
        if self.memory:
            self.memory.pop()

    def save(self, filename: str) -> None:
        dump_json(filename, self.memory)