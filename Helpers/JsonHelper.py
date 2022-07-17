import json

def IsJson(string):
    try:
        json.loads(string)
    except ValueError as e:
        return False
    return True