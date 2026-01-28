# query.py
import sys
import chromadb
from openai import OpenAI
from chromadb.config import Settings

from meal_prep_agent.config import VECTORSTORE_PATH, EMBEDDING_MODEL, API_KEY
from meal_prep_agent.models.openai_embedding import OpenAIEmbeddingFunction


def load_vectorstore():
    db_path = VECTORSTORE_PATH / "chroma_db_rag_recipes"
    client_settings = Settings(anonymized_telemetry=False)
    client = chromadb.PersistentClient(path=db_path, settings=client_settings)

    openai_client = OpenAI(api_key=API_KEY)
    embedding_fn = OpenAIEmbeddingFunction(openai_client, EMBEDDING_MODEL)

    collection = client.get_or_create_collection(
        name="rag_recipes",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def pretty_print_results(results):
    print("\n=== Top Results ===\n")

    metadatas = results["metadatas"][0]
    documents = results["documents"][0]

    for i, (meta, doc) in enumerate(zip(metadatas, documents), start=1):
        print(f"{i}. {meta['title']}")
        print(f"   Ingredients: {meta['ingredients']}")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python query.py \"your search query\"")
        return

    query = sys.argv[1]
    print(f"Searching for: {query}")

    collection = load_vectorstore()

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    pretty_print_results(results)


if __name__ == "__main__":
    main()
