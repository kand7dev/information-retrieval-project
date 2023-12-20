import json

def json_reader(path):
    with open(path, "r") as reader:
        json_data = json.load(reader)
        return json_data
    

# How to get all tokens from out JSON file

# json_data = json_reader("data.json")
# tokens_list = list()
# for json_object in json_data:
#     for tokens in json_object["paper_abstract"]:
#         tokens_list.append(tokens)
#     break # to iterate only one object. remove break to iterate all objects.
# print(tokens_list)