import json


def save(path, data):
    
    with open(path, "w") as output:
        
        json.dump(data, output, indent=4)
    
    return 1