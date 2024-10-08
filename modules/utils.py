import yaml

def read_config():
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config