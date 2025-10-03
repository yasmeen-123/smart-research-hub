import os
import numpy as np
import faiss
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings_client = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

INDEX_PATH = "faiss_index.idx"
DIM = 1536  # OpenAI text-embedding-3-small/large dims vary; adjust if needed

def create_embeddings_index(vectors=None):
    index = faiss.IndexFlatL2(DIM)
    if vectors is not None:
        index.add(np.array(vectors).astype("float32"))
    return index

def chunk_text(text, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

def embed_texts(texts):
    # returns list of vectors (floats)
    vs = []
    for t in texts:
        emb = embeddings_client.embed_query(t)
        vs.append(np.array(emb).astype("float32"))
    return vs

# simple persistence
def save_index(index):
    faiss.write_index(index, INDEX_PATH)

def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        return create_embeddings_index()
