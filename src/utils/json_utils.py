import json

def getJSONdata(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)