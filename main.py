# main.py
from core.generation import generate_response

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

Query: Summarize the PDF report I uploaded yesterday.
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