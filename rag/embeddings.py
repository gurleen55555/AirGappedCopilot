from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")
docs_folder = Path("docs")


def retrieve_runbook(query: str):
    documents = []
    sources = []

    for file_path in docs_folder.glob("*.txt"):
        documents.append(file_path.read_text(encoding="utf-8"))
        sources.append(file_path.name)

    document_embeddings = model.encode(documents)
    query_embedding = model.encode([query])

    scores = cosine_similarity(query_embedding, document_embeddings)[0]
    best_index = scores.argmax()

    return {
        "source": sources[best_index],
        "content": documents[best_index],
        "score": float(scores[best_index]),
    }


if __name__ == "__main__":
    result = retrieve_runbook("CPU usage is very high")

    print("Best matching file:", result["source"])
    print("Similarity score:", result["score"])
    print("\nRetrieved content:")
    print(result["content"])