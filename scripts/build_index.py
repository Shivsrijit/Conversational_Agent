import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def load_catalog(catalog_path):
    with open(catalog_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def prepare_texts(catalog):
    texts = []
    for item in catalog:
        text = f"{item['name']} {item['description']} {' '.join(item['keys'])} {' '.join(item['job_levels'])}"
        texts.append(text)
    return texts

def build_index(catalog_path, index_path):
    catalog = load_catalog(catalog_path)
    texts = prepare_texts(catalog)
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(texts, convert_to_tensor=False)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
    faiss.normalize_L2(embeddings)  # Normalize for cosine
    index.add(embeddings.astype('float32'))
    
    faiss.write_index(index, index_path)
    print(f"Index built with {len(catalog)} items")

if __name__ == "__main__":
    catalog_path = os.path.join(os.path.dirname(__file__), '..', 'shl_product_catalog.json')
    index_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss.index')
    build_index(catalog_path, index_path)