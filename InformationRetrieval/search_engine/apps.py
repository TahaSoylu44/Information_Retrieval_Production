from django.apps import AppConfig
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
import ir_datasets
from django.conf import settings
import os
import joblib

class SearchEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_engine'

    stop_words = None
    lematizer = None
    dataset = None
    bm25 = None

    def ready(self):
        nltk.download("punkt_tab", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download('stopwords', quiet=True)

        SearchEngineConfig.stop_words = set(stopwords.words('english'))
        SearchEngineConfig.lematizer = WordNetLemmatizer()

        SearchEngineConfig.dataset = ir_datasets.load("wikir/en1k/training")

        #! BM25
        model_path = os.path.join(settings.BASE_DIR, 'search_engine', 'bm_25_object_location', 'bm25_obj.joblib')

        if os.path.exists(model_path):
            SearchEngineConfig.bm25 = joblib.load(model_path)   # bm25 bir kereligine yuklendi