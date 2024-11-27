import os
import yaml
import json
from datetime import datetime
from rembg import remove


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


def remove_bg_with_rembg(input_path, output_path):
    with open(input_path, 'rb') as i:
        input_data = i.read()
    
    output_data = remove(input_data)
    
    with open(output_path, 'wb') as o:
        o.write(output_data)