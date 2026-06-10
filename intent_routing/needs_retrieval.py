from core.retrieval import build_faiss_index, build_bm25_index, hybrid_search, rerank,tokenize_for_bm25
from core.chunking import chunking_with_overlapping
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2",device="cpu")

with open("document.txt","r") as file:
    chunks = file.read()
chunks = chunking_with_overlapping(chunks)
for chunk in chunks:
    chunk["embedding"]=embedding_model.encode(chunk["text"])
  

def handle_retrieval(query):
    bm25 = build_bm25_index(chunks)
    faiss_index = build_faiss_index(chunks)
    query_embedding = embedding_model.encode(query)
    top_20_search_result = hybrid_search(faiss_index,bm25,query,query_embedding,chunks,top_k=20)
    top_3_search_result = rerank(query=query,chunks=top_20_search_result)
    return top_3_search_result