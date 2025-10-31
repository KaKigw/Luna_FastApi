import pickle, json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

chunks_file = Path("data/chunks.jsonl")
chunks = []
meta = []
texts = []

for line in open(chunks_file):
    obj = json.loads(line)
    texts.append(obj["text"])
    meta.append({
        "chunk_id": obj["chunk_id"],
        "doc_id": obj["orig_id"], 
        "source": obj["source"],
        "url": obj["url"],
        "title": obj.get("title")
    })

emb = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
dim = emb.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(np.array(emb).astype('float32'))

faiss.write_index(index, "data/faiss.index")
with open("data/chunks_meta.pkl", "wb") as f:
    pickle.dump({"meta": meta, "texts": texts}, f)

print("✅ FAISS index and metadata saved.")
