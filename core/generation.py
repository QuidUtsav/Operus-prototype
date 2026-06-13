from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("api_key"))

# --- Local Qwen (uncomment to use locally, comment out Groq section) ---
# from transformers import AutoModelForCausalLM, AutoTokenizer
# model_name = "Qwen/Qwen2.5-1.5B-Instruct"
# model = AutoModelForCausalLM.from_pretrained(model_name, dtype="float16", device_map="auto")
# tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(query, system_prompt="You are Operus. You are a helpful assistant.", max_new_tokens=200, conversation_history=None):
    system_message = {"role": "system", "content": system_prompt}
    current_user_message = {"role": "user", "content": query}
    
    if conversation_history is None:
        messages = [system_message, current_user_message]
    else:
        messages = [system_message] + conversation_history + [current_user_message]

    # --- Groq API (default) ---
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=max_new_tokens
    )
    return response.choices[0].message.content

    # --- Local Qwen (uncomment to use locally) ---
    # text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    # model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    # outputs = model.generate(**model_inputs, max_new_tokens=max_new_tokens)
    # return tokenizer.decode(outputs[0][len(model_inputs.input_ids[0]):], skip_special_tokens=True)