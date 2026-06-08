from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
class SemanticMemory:
    def __init__(self):
        self.facts = []
        
        self.faiss_index=faiss.IndexFlatL2(384)
        
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        pass
    
    def store(self, key, value):
        fact = f"{key}:{value}"
        
        embedded_fact = self.embedding_model.encode(fact)
        
        embedded_fact= embedded_fact.reshape(1,-1).astype(np.float32)
        self.faiss_index.add(embedded_fact)
        self.facts.append(fact)
        pass
    
    def retrieve(self, query, top_k=3):
        if self.faiss_index.ntotal==0: return[]
        embedded_query =self.embedding_model.encode(query)
        embedded_query= embedded_query.reshape(1,-1).astype(np.float32)
        
        distance, indices = self.faiss_index.search(embedded_query,top_k)
        
        top_k_facts = [self.facts[i] for i in indices[0]]
        return top_k_facts
