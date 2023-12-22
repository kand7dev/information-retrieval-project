from turtle import position
import json_reader


def record_level_inverted_index():
    
    json_data = json_reader.reader("data.json")
    unique_tokens_list = list()
    found_in_papers = list()
    inverted_result = dict()

    # find unique tokens in all documents

    for json_object in json_data:
        unique_terms = set(json_object['paper_abstract'])
        unique_tokens_list.extend(list(unique_terms))
    
    # create the inverted index (record level)

    for unique_token in unique_tokens_list:
        for data in json_data:
            if unique_token in data['paper_abstract']:
                found_in_papers.append(data['paper_id'])
        inverted_result[unique_token] = found_in_papers.copy()
        found_in_papers.clear()
         
    return inverted_result


def word_level_inverted_index():
    
    json_data = json_reader.reader("data.json")
    all_tokens_list = list()
    positions_list = list()
    found_item = 0
    inverted_result = dict()
    
    # get all tokens (not unique)

    for data in json_data:
        all_tokens_list.extend(data['paper_abstract'])
        
    # create the inverted index (word level)
        
    for token in all_tokens_list:
        for data in json_data:
            for index, item in enumerate(data['paper_abstract']):
                if token == item:
                    found_item += 1 
                    positions = (data['paper_id'], index)
                    positions_list.append(positions)
        inverted_result[token] = [positions_list.copy(), found_item]
        positions_list.clear()
        found_item = 0
        
    return inverted_result
