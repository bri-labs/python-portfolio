# query.py
import sys
import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from chromadb.config import Settings

from meal_prep_rag.config import VECTORSTORE_PATH, EMBEDDING_MODEL
from meal_prep_rag.models.openai_embedding import OpenAIEmbeddingFunction


# Load env variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")


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
