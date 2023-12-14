import requests
from bs4 import BeautifulSoup
import json
import text_processing

def crawler(url):
    html_respone = requests.get(url)
    if html_respone.ok:
        soup = BeautifulSoup(html_respone.content,"lxml") # html_response.content contains the whole html document.
        
        # scraping data
        title = soup.find("p", class_="title is-5 mathjax").text.strip()
        
        authors = soup.find("p", class_="authors").find_all("a")  
        paper_authors_list = list()
        for author in authors:
            paper_authors_list.append(author.text)
    
        submission = soup.find("p", class_="is-size-7").find("span", class_="has-text-black-bis has-text-weight-semibold").nextSibling.text.strip().removesuffix(";")  
        
        abstract = soup.find("span", class_="abstract-full has-text-grey-dark mathjax").text.strip().replace("△ Less", "").strip()
        tokenized_abstract = text_processing.lemmatizer(text_processing.abstract_tokenize(abstract))
        id = 1
        
        # creating dict
        paper_dict = dict(paper_id = id, paper_title = title, paper_authors = paper_authors_list, paper_abstract = tokenized_abstract, paper_submission_date = submission )
        
        # convert dict to JSON
        json_object = json.dumps(paper_dict)
        return json_object


