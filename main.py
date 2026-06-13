import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
from core.generation import generate_response
from intent_routing.needs_retrieval import handle_retrieval
from intent_routing.needs_web import web_search
from core.memory import SemanticMemory
from core.voice import record_audio_and_transcribe
from core.speak import speak

last_5_conversation_history=[]
def output(result,mode):
        print(f"ai: {result}")
        return speak(result)
        
def update_history(history, query, result):
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": result})
    return history[-10:]
memory = SemanticMemory()
def classify_intent(query,prev_intent):
    
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

    Query: Can you check in the internet?
    Intent: needs_web
    
    Query: Who is the current prime minister of Nepal?
    Intent: needs_web

    Query: Who is the CEO of OpenAI right now?
    Intent: needs_web

    Query: What happened in the news today?
    Intent: needs_web
    
    Query : could you sumarize the document i uploaded
    intent : needs_retrieval

    Query: what does the file say about X
    Intent: needs_retrieval

    Query: could you go through the document and find X
    Intent: needs_retrieval

    Query: What is the capital of Nepal
    Intent: direct_answer

    Previous intent: {prev_intent if prev_intent else "none"}

    Query: {query}
    Intent:"" """

    return generate_response(prompt, system_prompt=system_prompt,max_new_tokens=20,conversation_history=None).strip()


# intent=None
# while True:
#     mode = input("Input mode - text (t) or voice (v) or quit (q)? ").strip().lower()
#     if mode == "v":
#         query = record_audio_and_transcribe()
#     elif mode=="q":
#         break
#     else:
#         query = input("User: ").strip()
#     if not query:
#         print("Didn't catch that, please try again.")
#         speak("Didn't catch that, please try again.")
#         continue
#     intent= classify_intent(query,prev_intent=intent)
#     print(f"intent: {intent}\nquery:{query}")
#     if intent == "chat" or intent == "direct_answer":
#         result = generate_response(query,system_prompt=f"You are Operus. You are a helpful assistant.",max_new_tokens=200,conversation_history=last_5_conversation_history)
#         last_5_conversation_history= update_history(last_5_conversation_history,query=query,result=result)    
#         output(result=result,mode=mode)
#     elif intent=="needs_retrieval":
#         top_relevant_chunk = handle_retrieval(query)
#         result = generate_response(query=query,system_prompt=f"You are Operus. You are a helpful assistant. summaraize this given document{top_relevant_chunk}",max_new_tokens=200,conversation_history=last_5_conversation_history)
#         last_5_conversation_history= update_history(last_5_conversation_history,query=query,result=result)    
#         output(result=result, mode = mode)
#     elif intent=="needs_web":
#         result = web_search(query,last_5_conversation_history)
#         last_5_conversation_history= update_history(last_5_conversation_history,query=query,result=result)    
#         output(result=result, mode = mode)