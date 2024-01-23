import string

from nltk import PorterStemmer, WordNetLemmatizer, corpus, word_tokenize


def abstract_tokenize(abstract):
    tokens = word_tokenize(abstract)
    lowercase_tokens = [word.lower() for word in tokens]

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


def query_processing(query, boolean_retrieval=False):
    query_tokens = word_tokenize(query)
    lowercase_tokens = [word.lower() for word in query_tokens]

    punctuation_removed_tokens = list()
    for token in lowercase_tokens:
        if token not in string.punctuation:
            punctuation_removed_tokens.append(token)

    if not boolean_retrieval:
        stopwords = corpus.stopwords.words("english")
        final_tokens = list()
        for token in punctuation_removed_tokens:
            if token not in stopwords:
                final_tokens.append(token)

        return final_tokens

    else:
        stopwords = corpus.stopwords.words("english")
        boolean_operations = ["and", "or", "not"]
        custom_stopwords = [
            stopword for stopword in stopwords if stopword not in boolean_operations
        ]

        final_tokens = list()
        for token in punctuation_removed_tokens:
            if token not in custom_stopwords:
                final_tokens.append(token)

        return final_tokens


def stemmer(tokens):
    porter = PorterStemmer()
    stemmed_tokens = list()
    for token in tokens:
        stemmed_tokens.append(porter.stem(token))

    return stemmed_tokens


def lemmatizer(tokens):
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = list()
    for token in tokens:
        lemmatized_tokens.append(wordnet_lemmatizer.lemmatize(token))

    return lemmatized_tokens
