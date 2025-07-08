import numpy as np
import time
import uuid
import requests
# from qdrant_client import QdrantClient
# from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

from App.config import HF_ACCESS_TOKEN
# Init embedding model
# --- Hugging Face API Config ---
HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
HF_HEADERS = {"Authorization": f"Bearer {HF_ACCESS_TOKEN}"}  # ← Replace with your actual key

def get_embedding(text):
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": text})
    response.raise_for_status()
    return response.json()[0]

# APP/services/memory_store.py

# from sentence_transformers import SentenceTransformer

# Load embedding model
# embedder = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory memory store
MEMORY_STORE = []

# def get_embedding(text):
#     return embedder.encode([text])[0]

def save_memory(user_id=None, role=None, text=None, datetime=None, source=None, device_id=None):
    embedding = get_embedding(text)
    MEMORY_STORE.append({
        "user_id": user_id,
        "role": role,
        "text": text,
        "datetime": datetime,
        "source": source,
        "device_id": device_id,
        "embedding": embedding
    })

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_memory(user_id, query, top_k=5):
    query_embedding = get_embedding(query)
    relevant_memories = [
        (cosine_sim(query_embedding, mem["embedding"]), mem)
        for mem in MEMORY_STORE if mem["user_id"] == user_id
    ]
    top_hits = sorted(relevant_memories, key=lambda x: -x[0])[:top_k]
    return [mem["text"] for _, mem in top_hits]