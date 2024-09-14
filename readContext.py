import json

def read_context():
    try:
        with open("context.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_context(context):
    with open("context.json", "w") as file:
        json.dump(context, file)