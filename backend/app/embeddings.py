import os
import numpy as np
import faiss
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

OPENAI_API_KEY = os.getenv("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")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
_MODEL_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
}
DIM = int(os.getenv("EMBEDDING_DIM", _MODEL_DIMENSIONS.get(EMBEDDING_MODEL, 1536)))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

embeddings_client = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=OPENAI_API_KEY,
)

INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index.idx")


def create_embeddings_index(vectors=None):
    # Using flat L2 index — replace with IndexIVFFlat for larger scale
    index = faiss.IndexFlatL2(DIM)
    if vectors is not None and len(vectors) > 0:
        arr = np.vstack(vectors).astype("float32")
        index.add(arr)
    return index


def save_index(index):
    faiss.write_index(index, INDEX_PATH)


def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        return create_embeddings_index()


def chunk_text(text, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)


def embed_texts(texts):
    """
    Return list of vectors shaped (n, DIM) as numpy float32 arrays.
    """
    vectors = []
    for t in texts:
        emb = embeddings_client.embed_query(t)
        arr = np.array(emb, dtype="float32").reshape(1, -1)  # ensure 2D
        vectors.append(arr)
    if vectors:
        return np.vstack(vectors)  # shape (n, DIM)
    return np.zeros((0, DIM), dtype="float32")
