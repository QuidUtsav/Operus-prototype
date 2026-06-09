def chunking_with_overlapping(text,chunk_size=200,overlap=50):
    tokens= text.split(" ")
    
    chunks=[]
    i=0
    while i<len(tokens):
        window = tokens[i:i+chunk_size]
        
        chunk_text=" ".join(window)
        chunks.append({
            "chunk_id":len(chunks),
            "text":chunk_text,
            "start_token":i
        })
        i+=chunk_size-overlap
    
    
    return chunks

