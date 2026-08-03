import os
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import ir_datasets
from tqdm import tqdm

CURRENT_DIR = os.getcwd()
DB_PATH = os.path.join(CURRENT_DIR, "chroma_db_storage")

chroma_client = chromadb.PersistentClient(path=DB_PATH)

sentence_transformer_ef = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L12-v2",
    device="cuda",
    normalize_embeddings=True
)

collection = chroma_client.get_or_create_collection(
    name="django_embedding_collection",
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "ip"}   # inner product
)

dataset = ir_datasets.load("wikir/en1k/training")

doc_texts = []
doc_ids = []

for doc in dataset.docs_iter():
    doc_texts.append(doc.text)
    doc_ids.append(doc.doc_id)

BATCH_SIZE = 5000
total_doc = len(doc_texts)

for i in tqdm(range(0, total_doc, BATCH_SIZE)):
    batch_texts = doc_texts[i: i + BATCH_SIZE]
    batch_ids = doc_ids[i: i + BATCH_SIZE]

    collection.add(
        documents=batch_texts,
        ids=batch_ids
    )

print("Vector database completed!")