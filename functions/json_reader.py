import json


def reader(path):
    
    with open(path, "r") as reader:
        
        json_data = json.load(reader)
        
        return json_data