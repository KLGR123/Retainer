import os
import yaml
import json
import tiktoken
from rembg import remove
from datetime import datetime


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def dump_json(filename: str, data: dict):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error dumping JSON to {filename}: {e}")


def load_json(filename: str) -> dict:
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {filename}: {e}")
        return {}


def write_file(filename: str, content: str):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing to {filename}: {e}")


def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading from {filename}: {e}")
        return ""


def get_current_timestamp() -> str:
    return datetime.now().strftime('%Y-%m-%d,%H:%M:%S')


def remove_background(input_data):
    try:
        return remove(input_data, force_return_bytes=True)

    except Exception as e:
        print(f"Error removing background: {e}")
