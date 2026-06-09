import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
from core.generation import generate_response
from intent_routing.needs_retrieval import handle_retrieval
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

Query: summarize the document i uploaded
Intent: needs_retrieval

Query : could you sumarize the document i uploaded
intent : needs_retrieval

Query: what does the file say about X
Intent: needs_retrieval

Query: could you go through the document and find X
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
        result = generate_response(query=query,system_prompt=f"You are Jarvis. You are a helpful assistant. summaraize this given document{top_relevant_chunk}",max_new_tokens=200)
        print(result)