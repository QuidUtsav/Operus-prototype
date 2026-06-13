# from transformers import AutoModelForCausalLM,AutoTokenizer
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("api_key"))

# model_name="Qwen/Qwen2.5-1.5B-Instruct"
# model = AutoModelForCausalLM.from_pretrained(model_name,
#                                              dtype="float16",
#                                              device_map="auto"
#                                              )
# tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(query,system_prompt="You are Operus. You are a helpful assistant.",max_new_tokens=200,conversation_history=None):
        system_message = {"role": "system", "content": system_prompt}
        current_user_message={"role": "user", "content": query}
        if conversation_history is None:
            messages = [system_message,current_user_message]
        else:
            messages = [system_message] + conversation_history + [current_user_message]
        response = client.chat.completions.create(
        model="llama-3.1-8b-instant", #free model
        messages=messages,
        max_tokens=max_new_tokens
            )
        return response.choices[0].message.content

def generate_structured_response(query,intent,danger_level,source):
    text = generate_response(query)
    response_format = {
                "query": query,
                "intent": intent,
                "text":text,
                "danger_level": danger_level,
                "source": source
                }
    return response_format
    