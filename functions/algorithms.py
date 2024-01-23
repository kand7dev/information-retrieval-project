from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from . import text_processing


def boolean_retrieval(query, tokenized_data, record_index):
    query_tokens = text_processing.query_processing(query, True)
    operations = ["and", "or", "not"]
    number_of_documents = [i + 1 for i in range(len(tokenized_data))]

    final_result = set()

    for index in range(len(query_tokens)):
        try:
            if len(query_tokens) == 1:
                final_result = set(record_index[query_tokens[0]])

            if query_tokens[index] not in operations:
                continue

            has_not = False
            previous_token = query_tokens[index - 1]
            next_token = query_tokens[index + 1]

            if (next_token) == "not":
                next_token = query_tokens[index + 2]
                has_not = True

            if query_tokens[index] == "and":
                if not final_result:
                    if has_not:
                        final_result = set(record_index[previous_token]).intersection(
                            set(
                                [
                                    item
                                    for item in number_of_documents
                                    if item not in record_index[next_token]
                                ]
                            )
                        )
                    else:
                        final_result = set(record_index[previous_token]).intersection(
                            set(record_index[next_token])
                        )
                else:
                    if has_not:
                        final_result = final_result.intersection(
                            set(
                                [
                                    item
                                    for item in number_of_documents
                                    if item not in record_index[next_token]
                                ]
                            )
                        )
                    else:
                        final_result = final_result.intersection(
                            set(record_index[next_token])
                        )

            elif query_tokens[index] == "or":
                if not final_result:
                    if has_not:
                        final_result = set(record_index[previous_token]).union(
                            set(
                                [
                                    item
                                    for item in number_of_documents
                                    if item not in record_index[next_token]
                                ]
                            )
                        )
                    else:
                        final_result = set(record_index[previous_token]).union(
                            set(record_index[next_token])
                        )
                else:
                    if has_not:
                        final_result = final_result.union(
                            set(
                                [
                                    item
                                    for item in number_of_documents
                                    if item not in record_index[next_token]
                                ]
                            )
                        )
                    else:
                        final_result = final_result.union(set(record_index[next_token]))

        except KeyError:
            final_result = set()

        except IndexError:
            final_result = set()

    return final_result


def vector_space_model(query, tokenized_data, plain_data):
    tokenized_query = text_processing.query_processing(query, False)
    preprocessed_query = " ".join(tokenized_query)
    tfidf_vectorizer = TfidfVectorizer()

    result = list()

    for index, document in enumerate(tokenized_data):
        preprocessed_documents = " ".join(document["paper_abstract"])
        tfidf_matrix = tfidf_vectorizer.fit_transform([preprocessed_documents])
        query_vector = tfidf_vectorizer.transform([preprocessed_query])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)
        result.append((plain_data[index]["paper_id"], cosine_similarities[0][0]))

    return result


def okapi_bm25(query, tokenized_data):
    tokenized_query = text_processing.query_processing(query, False)
    all_documents = list()

    for document in tokenized_data:
        all_documents.append(document["paper_abstract"])

    bm25 = BM25Okapi(all_documents)
    doc_scores = bm25.get_scores(tokenized_query)

    return doc_scores
