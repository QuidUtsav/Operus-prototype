from core.generation import generate_structured_response, generate_response
from core.retrieval import hybrid_search, rerank
from core.memory import SemanticMemory

memory = SemanticMemory()
GREETINGS = ["hi", "hello", "hey", "thanks", "bye"]

def is_social(query):
    return any(g in query.lower() for g in GREETINGS)

def handle_query(query):
    if query.lower() in GREETINGS:
        return is_social(query)
    memory.store(query)