from django.apps import AppConfig
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from django.conf import settings
import os
import pickle

class SearchEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_engine'

    stop_words = None
    lematizer = None
    bm25 = None

    def ready(self):
        nltk.download("punkt_tab", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download('stopwords', quiet=True)

        print("nltk downloaded!")

        SearchEngineConfig.stop_words = set(stopwords.words('english'))
        SearchEngineConfig.lematizer = WordNetLemmatizer()

        #! BM25
        model_path = os.path.join(settings.BASE_DIR, 'bm25_object_location', 'bm25_obj.pkl')

        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                loaded_bm25 = pickle.load(f)

            SearchEngineConfig.bm25 = loaded_bm25   # bm25 bir kereligine yuklendi
            print("bm25 ready!")
        else:
            print("bm25 cannot be found!")
            print(settings.BASE_DIR)