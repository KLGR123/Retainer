import os
import yaml
import json
from datetime import datetime


def dump_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def read_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d,%H:%M:%S')