import json, os
from pathlib import Path

IN = Path("../curated_docs.jsonl")
OUT = Path("data/chunks.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 400  # characters
OVERLAP = 50

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    i = 0
    L = len(text)
    while i < L:
        end = min(i + chunk_size, L)
        chunk = text[i:end].strip()
        if len(chunk) >= 50:
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

with IN.open() as f_in, OUT.open("w") as f_out:
    for line in f_in:
        doc = json.loads(line)
        doc_id = doc.get("id")
        chunks = chunk_text(doc["text"])
        for idx, c in enumerate(chunks):
            out = {
                "orig_id": doc_id,
                "chunk_id": f"{doc_id}__{idx}",
                "source": doc["source"],
                "title": doc.get("title"),
                "url": doc.get("url"),
                "text": c
            }
            f_out.write(json.dumps(out, ensure_ascii=False) + "\n")

print("Chunking complete. Output:", OUT)
