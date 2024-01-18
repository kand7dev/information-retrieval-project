import json_reader
import text_processing
from datetime import datetime


def tokenizer(data_file):
    
    tokenized_data_list = list()
    tokenized_authors_list = list()
    data = json_reader.reader(data_file)
    
    for document in data:
        
        tokenized_data = dict()
        tokenized_data['paper_id'] = document['paper_id']
        tokenized_data['paper_title'] = document['paper_title']
        
        for author in document['paper_authors']:
            tokenized_authors_list.append(author.lower())
            
        tokenized_data['paper_authors'] = tokenized_authors_list.copy()
        tokenized_data['paper_abstract'] = text_processing.lemmatizer(text_processing.abstract_tokenize(document['paper_abstract']))
        
        date = datetime.strptime(document['paper_submission_date'], "%d %B, %Y")
        tokenized_data['paper_submission_date'] = date.strftime("%d/%m/%Y")
        tokenized_authors_list.clear()
        tokenized_data_list.append(tokenized_data)
        
    return tokenized_data_list
