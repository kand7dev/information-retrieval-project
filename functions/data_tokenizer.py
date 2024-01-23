from . import text_processing
# from datetime import datetime


def tokenizer(data_file):
    
    tokenized_data_list = list()
    
    for document in data_file:
        
        tokenized_data = dict()
        tokenized_data['paper_id'] = document['paper_id']
        tokenized_data['paper_title'] = document['paper_title']
        
        authors_list = list()
        for author in document['paper_authors']:
            
            authors_list.append(author.lower())
            
        tokenized_data['paper_authors'] = authors_list.copy()
        tokenized_data['paper_abstract'] = text_processing.lemmatizer(text_processing.abstract_tokenize(document['paper_abstract']))
        
        # date = datetime.strptime(document['paper_submission_date'], "%d %B, %Y")
        # tokenized_data['paper_submission_date'] = date.strftime("%d/%m/%Y")
        tokenized_data['paper_submission_date'] = document['paper_submission_date']
        tokenized_data_list.append(tokenized_data)
        
    return tokenized_data_list
