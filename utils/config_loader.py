import json

def load_config(path="config/settings.json"):
    with open(path, "r") as f:
        return json.load(f)
