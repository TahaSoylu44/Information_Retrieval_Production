from nltk.tokenize import word_tokenize
from django.apps import apps

def process_query(query: str) -> str:
    tokenized_query = word_tokenize(query.lower())

    app_config = apps.get_app_config('search_engine')
    stop_words = app_config.stop_words
    tokenized_without_stopwords = []

    for word in tokenized_query:
        if word not in stop_words:
            tokenized_without_stopwords.append(word)

    lematizer = app_config.lematizer
    lemmatized_words = [lematizer.lemmatize(word) for word in tokenized_without_stopwords]

    return " ".join(lemmatized_words)