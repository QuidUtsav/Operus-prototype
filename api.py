from fastapi import FastAPI
from pydantic import BaseModel
from main import classify_intent
from core.generation import generate_response
from intent_routing.needs_retrieval import handle_retrieval
from intent_routing.needs_web import web_search
app = FastAPI()
sessions={}
def update_history(history, query, result):
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": result})
    return history[-10:]
def update_session(session,session_id,query,intent,result):
    session["history"]=update_history(session["history"],query,result)
    session["prev_intent"]=intent
    sessions[session_id]=session
class ChatRequest(BaseModel):
    query:str
    session_id:str


class ChatResponse(BaseModel):
    response:str
    intent:str
    session_id:str

@app.post("/chat")
def chat(request: ChatRequest):
    session = sessions.get(request.session_id, {"history": [], "prev_intent": None})

    intent = classify_intent(request.query,session["prev_intent"])
    if intent=="chat" or intent=="direct_answer":
         
        response_text = generate_response(request.query,system_prompt=f"You are Operus. You are a helpful assistant.",max_new_tokens=200,conversation_history=session["history"])
        result ={"response":response_text,
                 "intent":intent}
        update_session(session=session,session_id=request.session_id,query=request.query,intent=intent,result=response_text)
        return result
    elif intent=="needs_retrieval":
        top_relevant_chunk = handle_retrieval(request.query)
         
        response_text = generate_response(query=request.query,system_prompt=f"You are Operus. You are a helpful assistant. summaraize this given document{top_relevant_chunk}",max_new_tokens=200,conversation_history=session["history"])
        result ={"response":response_text,
                 "intent":intent}
        update_session(session=session,session_id=request.session_id,query=request.query,intent=intent,result=response_text)
        return result
    elif intent=="needs_web":
         
        response_text = web_search(request.query,session["history"])
        result ={"response":response_text,
                 "intent":intent}
        update_session(session=session,session_id=request.session_id,query=request.query,intent=intent,result=response_text)
        return result
    
    return {"message":"did not understand could you clarify your intent."}

@app.get("/health")
def health():
    return {"status":"okay"}