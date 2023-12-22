import json_reader


def inverted_index():
    
    json_data = json_reader.reader("data.json")
    unique_tokens_list = list()
    found_in_papers = list()
    inverted_result = dict()

    # find unique tokens in all documents

    for json_object in json_data:
        unique_terms = set(json_object['paper_abstract'])
        unique_tokens_list.extend(list(unique_terms))
    
    # create the inverted index 

    for unique_token in unique_tokens_list:
        for data in json_data:
            if unique_token in data['paper_abstract']:
                found_in_papers.append(data['paper_id'])
        inverted_result[unique_token] = found_in_papers.copy()
        found_in_papers.clear()
         
    return inverted_result
    