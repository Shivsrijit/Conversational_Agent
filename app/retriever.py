import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class Retriever:
    def __init__(self, catalog_path, index_path):
        self.catalog = self.load_catalog(catalog_path)
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.index = faiss.read_index(index_path)
        
    def load_catalog(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search(self, query, top_k=15):
        query_embedding = self.model.encode([query], convert_to_tensor=False)
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.catalog):
                item = self.catalog[idx]
                results.append({
                    'score': float(distances[0][i]),
                    'item': item
                })
        return results