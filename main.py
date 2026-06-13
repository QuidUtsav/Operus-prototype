# import os
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
# from core.generation import generate_response
# from intent_routing.needs_retrieval import handle_retrieval
# from intent_routing.needs_web import web_search
# from core.memory import SemanticMemory
# # from core.voice import record_audio_and_transcribe
# # from core.speak import speak



# # intent=None
# # while True:
# #     mode = input("Input mode - text (t) or voice (v) or quit (q)? ").strip().lower()
# #     if mode == "v":
# #         query = record_audio_and_transcribe()
# #     elif mode=="q":
# #         break
# #     else:
# #         query = input("User: ").strip()
# #     if not query:
# #         print("Didn't catch that, please try again.")
# #         speak("Didn't catch that, please try again.")
# #         continue
# #     intent= classify_intent(query,prev_intent=intent)
# #     print(f"intent: {intent}\nquery:{query}")
# #     if intent == "chat" or intent == "direct_answer":
# #         result = generate_response(query,system_prompt=f"You are Operus. You are a helpful assistant.",max_new_tokens=200,conversation_history=last_5_conversation_history)
# #         last_5_conversation_history= update_history(last_5_conversation_history,query=query,result=result)    
# #         output(result=result,mode=mode)
# #     elif intent=="needs_retrieval":
# #         top_relevant_chunk = handle_retrieval(query)
# #         result = generate_response(query=query,system_prompt=f"You are Operus. You are a helpful assistant. summaraize this given document{top_relevant_chunk}",max_new_tokens=200,conversation_history=last_5_conversation_history)
# #         last_5_conversation_history= update_history(last_5_conversation_history,query=query,result=result)    
# #         output(result=result, mode = mode)
# #     elif intent=="needs_web":
# #         result = web_search(query,last_5_conversation_history)
# #         last_5_conversation_history= update_history(last_5_conversation_history,query=query,result=result)    
# #         output(result=result, mode = mode)