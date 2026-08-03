from django.apps import AppConfig
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

class SearchEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_engine'

    stop_words = None
    lematizer = None

    def ready(self):
        nltk.download("punkt_tab")
        nltk.download("wordnet")

        SearchEngineConfig.stop_words = set(stopwords.words('english'))
        SearchEngineConfig.lematizer = WordNetLemmatizer()