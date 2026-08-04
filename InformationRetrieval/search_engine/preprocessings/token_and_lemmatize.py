from nltk.tokenize import word_tokenize
from django.apps import apps
import numpy as np
from search_engine.models import Document

def process_query(query: str) -> str:
    app_config = apps.get_app_config('search_engine')
    stop_words = app_config.stop_words
    lematizer = app_config.lematizer
    tokenized_query = word_tokenize(query.lower())
    tokenized_without_stopwords = []

    for word in tokenized_query:
        if word not in stop_words:
            tokenized_without_stopwords.append(word)

    lemmatized_words = [lematizer.lemmatize(word) for word in tokenized_without_stopwords]
    return " ".join(lemmatized_words)

def formula(index: int) -> float:
    return 1 / (60 + index)

def reciprocal_rank_fusion(bm25: list, sen_transformer: list) -> list:
    set_of_examined = set()
    tuple_list = []

    for i,doc_id in enumerate(bm25):
        set_of_examined.add(doc_id)

        doc_score = 0

        doc_score += formula(i + 1)

        for j in range(len(sen_transformer)):
            if sen_transformer[j] == doc_id:
                doc_score += formula(j + 1)
                break

        tuple_list.append((doc_score, doc_id))

    for i in range(len(sen_transformer)):
        doc_id = sen_transformer[i]

        if doc_id not in set_of_examined:
            set_of_examined.add(doc_id)
            tuple_list.append((formula(i + 1), doc_id))

    tuple_list.sort(reverse=True)
    return tuple_list

def hybrid_search(search_text: str) -> list:
    app_config = apps.get_app_config('search_engine')
    doc_dict = app_config.doc_dict
    bm25 = app_config.bm25
    collection = app_config.collection

    processed_text = process_query(search_text)
    similarities = bm25.get_scores(processed_text.split(" "))

    results_10 = collection.query(
        query_texts=[search_text],
        n_results=10
    )

    sen_transformer_top_10 = list(results_10['ids'][0])

    index_of_found_docs = np.where(similarities > 0)[0]

    found_docs_with_scores = []

    for index in list(index_of_found_docs):
        found_docs_with_scores.append((similarities[index], doc_dict[index]))

    bm25_top_10 = []

    for mytuple in sorted(found_docs_with_scores, reverse=True):
        bm25_top_10.append(mytuple[1])

        if len(bm25_top_10) == 10:
            break

    reciprocal_with_scores = reciprocal_rank_fusion(
        bm25=bm25_top_10,
        sen_transformer=sen_transformer_top_10
    )

    hybrid_search_top_10 = []

    for mytuple in reciprocal_with_scores:
        hybrid_search_top_10.append(mytuple[1])

        if len(hybrid_search_top_10) == 10:
            break

    return hybrid_search_top_10

def cross_encoding(search_text: str) -> list:
    app_config = apps.get_app_config('search_engine')
    retrieval_list = hybrid_search(search_text)
    cross_encoder_model = app_config.cross_encoder_model

    query_doc_pairs = []

    for doc_id in retrieval_list:
        document_obj = Document.objects.filter(doc_id=doc_id).first()
        query_doc_pairs.append((search_text, document_obj.text))

    cross_encoder_scores = list(cross_encoder_model.predict(query_doc_pairs))

    index_and_score = []

    for i in range(len(retrieval_list)):
        index_and_score.append((cross_encoder_scores[i], i))

    result_of_reranking = []

    for mytuple in sorted(index_and_score, reverse=True):
        result_of_reranking.append(retrieval_list[mytuple[1]])

    return result_of_reranking