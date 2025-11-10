import os
import numpy as np
import faiss
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Load API key from environment ---
# Note: The main application (main.py) should handle the global load_dotenv() call.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Changed to a print/log for a module file, letting the main app handle termination
    print("WARNING: Missing OPENAI_API_KEY in environment. Embeddings will fail if used.")


# --- Embedding Model Settings ---
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
_MODEL_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
}
# Safely get the dimension, defaulting to 1536
DIM = int(os.getenv("EMBEDDING_DIM", _MODEL_DIMENSIONS.get(EMBEDDING_MODEL, 1536)))

# --- Initialize Embedding Client ---
embeddings_client = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=OPENAI_API_KEY,
)

INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index.idx")

# --- FAISS Index Handling ---
def create_embeddings_index(vectors=None):
    """Initializes a new FAISS IndexFlatL2."""
    index = faiss.IndexFlatL2(DIM)
    if vectors is not None and len(vectors) > 0:
        # Ensures vectors is a NumPy array for correct addition
        arr = np.array(vectors).astype("float32")
        index.add(arr)
    return index

def save_index(index):
    """Saves the FAISS index to the specified path."""
    faiss.write_index(index, INDEX_PATH)

def load_index():
    """Loads the FAISS index from the path, or creates a new empty one."""
    if os.path.exists(INDEX_PATH):
        try:
            return faiss.read_index(INDEX_PATH)
        except Exception as e:
            print(f"Error loading FAISS index: {e}. Creating a new one.")
            return create_embeddings_index()
    return create_embeddings_index()

# --- Text Chunking ---
def chunk_text(text, chunk_size=500, overlap=50):
    """Splits a large text into smaller, overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

# --- Embedding Generation ---
def embed_texts(texts):
    """
    Generates embeddings for a list of text strings.
    Returns a (n, DIM) numpy array of embeddings.
    """
    if not texts or not isinstance(texts, list):
        return np.zeros((0, DIM), dtype="float32")
    
    # Ensure all elements are strings before embedding
    texts = [str(t) for t in texts]
    
    embs = embeddings_client.embed_documents(texts)
    return np.array(embs, dtype="float32")