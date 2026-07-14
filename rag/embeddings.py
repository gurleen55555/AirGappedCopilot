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

    top_indices = scores.argsort()[-2:][::-1]

    results = []

    for index in top_indices:
        if scores[index] < 0.40:
            continue
        results.append(
            {
                "source": sources[index],
                "content": documents[index],
                "score": float(scores[index]),
            }
        )
        if not results:
            return [
                {
                "source": "none",
                "content": "No sufficiently relevant runbook was found.",
                "score": 0.0,
            }
        ]
        return results


if __name__ == "__main__":
    results = retrieve_runbook("CPU usage is very high")

    for result in results:
        print("\nSource:", result["source"])
        print("Score:", result["score"])
        print(result["content"])