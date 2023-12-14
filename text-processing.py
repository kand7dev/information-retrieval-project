import string
from nltk import word_tokenize, corpus, PorterStemmer


def abstract_tokenize(abstract):
    
    tokens = word_tokenize(abstract) #nltk's tokenizer
    
    lowercase_tokens = [char.lower() for char in tokens]
    
    punctuation_removed_tokens = list()
    for token in lowercase_tokens:
        if token not in string.punctuation:
            punctuation_removed_tokens.append(token)

    stopwords = corpus.stopwords.words("english")
    final_tokens = list()
    for token in punctuation_removed_tokens:
        if token not in stopwords:
            final_tokens.append(token)
    
    return final_tokens


def stemmer(tokens):
    
    porter = PorterStemmer()
    stemmed_tokens = list()
    for token in tokens:
        stemmed_tokens.append(porter.stem(token))
        
    return stemmed_tokens
    
    