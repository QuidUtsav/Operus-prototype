# main.py
from core.generation import generate_response
from core.chunking import chunking_with_overlapping
from core.retrieval import build_faiss_index, build_bm25_index, hybrid_search, rerank
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#========================== needs_retrieval portion ===================================================
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
    
def classify_intent(query):
    
    system_prompt = (
        "You are an expert intent classification routing agent. "
        "Your job is to analyze a user query and output EXACTLY one of these four tags: "
        "[needs_retrieval, needs_web, chat, direct_answer]. "
        "Do not include any other text, explanation, or punctuation."
    )
    
    prompt = f"""Classify the user query into one of the following intents:
- needs_retrieval: If the user asks about personal documents, uploaded files, or private data.
- needs_web: If the user asks about real-time events, weather, news, or things requiring a Google search.
- chat: If it's a greeting, casual banter, or small talk.
- direct_answer: If it's a general knowledge question, logic puzzle, or creative task that requires no external data.

Examples:
Query: Hello there!
Intent: chat

Query: What is the weather in Pokhara right now?
Intent: needs_web

Query: Sumarize the PDF report I uploaded yesterday.
Intent: needs_retrieval

Query: What is the capital of Nepal?
Intent: direct_answer

Query: {query}
Intent:"""

    return generate_response(prompt, system_prompt=system_prompt,max_new_tokens=20).strip()

while True:
    
    query = input("how can i help you today? ")
    intent= classify_intent(query)
    print(intent)
    if intent == "chat" or intent == "direct_answer":
        print(generate_response(query))
    elif intent=="needs_retrieval":
        top_relevant_chunk = handle_retrieval(query)
        result = generate_response(query=query,system_prompt=f"You are Jarvis. You are a helpful assistant. summaraize this given document{top_relevant_chunk}")
        print(result)