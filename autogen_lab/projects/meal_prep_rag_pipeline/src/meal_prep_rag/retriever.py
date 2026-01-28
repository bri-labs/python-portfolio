# Vector search logic
import chromadb
import json
from openai import OpenAI
from chromadb.config import Settings
from typing import List

from meal_prep_rag.config import VECTORSTORE_PATH, EMBEDDING_MODEL, API_KEY
from meal_prep_rag.models.openai_embedding import OpenAIEmbeddingFunction
from meal_prep_rag.models.pydantic_recipe import Recipe

class Retriever:
    def __init__(self, collection=None):
        # Check if collection past in, if isn't, then load vectorstore
        if collection:
            self.collection = collection
        else:
            self.collection= self.load_vectorstore()
        
    # Load chroma DB
    def load_vectorstore(self):
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

    def retrieve(self, query: str, n: int = 5) -> List[Recipe]:
        """
        Retrieve the top-n most relevant chunks from ChromaDB. 
        """
        recipes = []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )

        metadatas = results["metadatas"][0]
        
        for meta in metadatas:
            # Decode JSON string back into list
            if isinstance(meta.get("ingredients"), str):
                try:
                    meta["ingredients"] = json.loads(meta["ingredients"])
                except Exception:
                    # Skip malformed rows
                    continue

            # Now meta matches Pydantic model
            # NOTE: Longer way to do the following line: `recipes.append(Recipe(**meta))`
            title = meta.get('title')
            ingredients = meta.get('ingredients')

            recipe = Recipe(title=title, ingredients=ingredients)
            recipes.append(recipe)
        
        return recipes
    


if __name__ == "__main__":
    retriever = Retriever()
    result = retriever.retrieve(query="strawberry", n=3)
    print(result)

