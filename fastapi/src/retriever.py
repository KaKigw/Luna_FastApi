import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Initialize embedder and FAISS index once at module load
embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("src/data/faiss.index")

with open("src/data/chunks_meta.pkl", "rb") as f:
    data = pickle.load(f)
    meta = data["meta"]
    texts = data["texts"]

def retrieve_context(query, top_k=3):
    """
    Retrieves the top_k most relevant context chunks from the FAISS index.

    Args:
        query (str): The user's input query.
        top_k (int): Number of top documents to retrieve.

    Returns:
        list[dict]: A list of context hits with metadata.
    """
    q_vec = embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    D, I = index.search(np.array(q_vec).astype("float32"), top_k * 2)

    hits = []
    seen_docs = set()

    for score, idx in zip(D[0], I[0]):
        doc_id = meta[idx]["doc_id"]
        if doc_id in seen_docs:
            continue
        seen_docs.add(doc_id)
        hits.append({
            "chunk_id": meta[idx]["chunk_id"],
            "doc_id": doc_id,
            "title": meta[idx].get("title"),
            "url": meta[idx].get("url"),
            "excerpt": texts[idx][:500],
            "score": float(score)
        })
        if len(hits) == top_k:
            break

    return hits
