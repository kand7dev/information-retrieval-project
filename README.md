# Information Retrieval Project

## What this project does?
This project implements a small scientific articles search engine. For now it processes only the abstract provided by the articles.
1. It can scrape new data from [arxiv](https://arxiv.org/) or use existing data provided in this repository.
2. Processes data (tokenizing, lemmatizing/stemming, creates an inverted index).
3. Supports 3 searching algorithms:
    1. Boolean Retrieval
    2. Vector Space Model
    3. Okapi BM25
4. Users can put basic filters while searching for documents:
    1. By author name
    2. By date of publishment

## How can I run this project?
1. Users can install the `requirements.txt` in their local environment and execute the `main.py` script. This script automatically downloads all the important `nltk data` in users `$HOME` directory.
2. Users can use the containerized version of the application from my [docker repository](https://hub.docker.com/repository/docker/kand7dev99/kand7dev-projects/general) by pulling the `information_retrieval` tag.

## Contributions and Improvements
If someone would like to contribute to the project or suggest improvements, they can offer a PR or open an Issue. 


