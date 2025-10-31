import pickle, numpy as np
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss.index")
data = pickle.load(open("data/chunks_meta.pkl", "rb"))

def retrieve(q, k=3):
    q_emb = model.encode([q], convert_to_numpy=True, normalize_embeddings=True)
    D, I = index.search(np.array(q_emb).astype('float32'), k)
    out = []
    for dist, idx in zip(D[0], I[0]):
        out.append({
            "score": float(dist),
            "text": data["texts"][idx],
            **data["meta"][idx]
        })
    print("🔍 Raw indices:", I)
    print("📊 Raw scores:", D)

    return out

if __name__ == "__main__":
    q = "What are common symptoms of breast cancer?"
    print("🔍 Query:", q)
    hits = retrieve(q, k=3)
    for h in hits:
        print("SCORE:", h["score"])
        print("SOURCE:", h["source"], h.get("title"), h.get("url"))
        print(h["text"][:400])
        print("-" * 60)
    if not hits:
        print("⚠️ No results found. Try a broader query or check your index.")

