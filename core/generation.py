from transformers import AutoModelForCausalLM,AutoTokenizer


model_name="Qwen/Qwen2.5-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name,
                                             dtype="float16",
                                             device_map="auto"
                                             )
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(query,system_prompt="You are Jarvis. You are a helpful assistant.",max_new_tokens=200,conversation_history=None):
    system_message = {"role": "system", "content": system_prompt}
    current_user_mesage={"role": "user", "content": query}
                
    if conversation_history is None:
        messages = [system_message,current_user_mesage]
    else:
        messages = [system_message]+ conversation_history+ [current_user_mesage]
    text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    outputs = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        temperature = 0.1
    )
    response = tokenizer.decode(outputs[0][len(model_inputs.input_ids[0]):],skip_special_tokens=True)
    return response

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
    