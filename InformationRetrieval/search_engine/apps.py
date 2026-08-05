from django.apps import AppConfig
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from django.conf import settings
import os
import pickle
import chromadb
from collections import defaultdict
import ir_datasets
from sentence_transformers import CrossEncoder
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class SearchEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_engine'

    stop_words = None
    lematizer = None
    bm25 = None
    collection = None
    doc_dict = None
    dataset = None
    cross_encoder_model = None
    sentence_transformer_ef = None

    def ready(self):
        dataset = ir_datasets.load("wikir/en1k/training")
        nltk.download("punkt_tab", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download('stopwords', quiet=True)

        print("nltk downloaded!")

        SearchEngineConfig.stop_words = set(stopwords.words('english'))
        SearchEngineConfig.lematizer = WordNetLemmatizer()
        self.lematizer.lemmatize("taha")
        print("Lemmatizer warmed up!")

        #! CHROMA DB
        db_path = os.path.join(settings.BASE_DIR, 'chroma_db_storage')
        chroma_client = chromadb.PersistentClient(path=db_path)
        SearchEngineConfig.sentence_transformer_ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L12-v2", device="cuda", normalize_embeddings=True)
        print("Sentence Transformer Ready!")
        SearchEngineConfig.collection = chroma_client.get_collection(name="django_embedding_collection", embedding_function=self.sentence_transformer_ef)
        print("Chroma DB ready!")

        self.collection.query(query_texts=["taha"])
        print("Sentence Transformer Warmed up!")

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

        #! DOC_DICT
        doc_dict_trial = defaultdict(str)

        for i, doc in enumerate(dataset.docs_iter()):
            doc_dict_trial[i] = doc.doc_id

        SearchEngineConfig.doc_dict = dict(doc_dict_trial)

        print("Doc dict ready!")

        #! CROSS ENCODER
        SearchEngineConfig.cross_encoder_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
        SearchEngineConfig.cross_encoder_model.predict([("Taha", "Soylu")])
        print("Cross encoder model warmed up!")
        print("Cross Encoder Ready!")