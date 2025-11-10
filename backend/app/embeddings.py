import os
import numpy as np
import faiss
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Load API key from environment ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment. Add it to your .env file.")

# --- Embedding Model Settings ---
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
_MODEL_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
}
DIM = int(os.getenv("EMBEDDING_DIM", _MODEL_DIMENSIONS.get(EMBEDDING_MODEL, 1536)))

# --- Initialize Embedding Client ---
embeddings_client = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=OPENAI_API_KEY,
)

INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index.idx")

# --- FAISS Index Handling ---
def create_embeddings_index(vectors=None):
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
    return create_embeddings_index()

# --- Text Chunking ---
def chunk_text(text, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

# --- Embedding Generation ---
def embed_texts(texts):
    """
    Returns a (n, DIM) numpy array of embeddings for a list of texts.
    """
    if not texts:
        return np.zeros((0, DIM), dtype="float32")
    embs = embeddings_client.embed_documents(texts)
    return np.array(embs, dtype="float32")
