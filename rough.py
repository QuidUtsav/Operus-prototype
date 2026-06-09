from core.chunking import chunking_with_overlapping
with open("document.txt","r") as file:
    chunks = file.read()
chunks = chunking_with_overlapping(text=chunks, chunk_size=15,overlap=4)
for i,chunk in enumerate(chunks):
    print(i,chunk)