import requests
from bs4 import BeautifulSoup
import json
import text_processing
import random_word

def crawler():
    random = random_word.RandomWords()
    json_object_list = list()
    id = 1
    for i in range(10):
        
        word = random.get_random_word()
        url = url = "https://arxiv.org/search/?query=" + str(word) + "&searchtype=all&source=header"
        html_respone = requests.get(url)
        
        if html_respone.ok:
            
            try:
                soup = BeautifulSoup(html_respone.content,"html.parser") # html_response.content contains the whole html document.
                    
                # scraping data
                html_titles = soup.find_all("p", class_="title is-5 mathjax")
                html_authors = soup.find_all("p", class_="authors")
                html_submissions = soup.select("p.is-size-7:not(.comments)")
                html_abstracts = soup.find_all("span", class_="abstract-full has-text-grey-dark mathjax")
                authors_list = list() # is used to store all authors, gets re-initialized in each iteration
                
                for i in range(len(html_titles)):
                    
                    title = html_titles[i].text.strip()
                    for author in html_authors[i].find_all("a"):
                        authors_list.append(author.text)
                    
                    submission = html_submissions[i].find("span", class_="has-text-black-bis has-text-weight-semibold").nextSibling.text.strip().removesuffix(";")
                    abstract = html_abstracts[i].text.strip().replace("△ Less", "").strip()    
                    tokenized_abstract = text_processing.lemmatizer(text_processing.abstract_tokenize(abstract))
                    
                    # creating json object (must be a dictionary to use json.dumps)
                    paper_dict= dict(paper_id = id, paper_title = title, paper_authors = authors_list, paper_abstract = tokenized_abstract, paper_submission_date = submission )
                    json_object = json.dumps(paper_dict)
                    json_object_list.append(json_object)
                    authors_list.clear()
                    id+=1

            except AttributeError:
                
                continue
            
            
    # save data to .json file       
    with open("data.json","w") as output:
        json.dump(json_object_list,output, indent=2)
    
    return json_object_list
crawler()