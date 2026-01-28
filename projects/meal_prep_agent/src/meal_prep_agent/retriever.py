# Vector search logic
import chromadb
import json
from openai import OpenAI
from chromadb.config import Settings
from typing import List

from meal_prep_agent.config import VECTORSTORE_PATH, EMBEDDING_MODEL, API_KEY
from meal_prep_agent.models.openai_embedding import OpenAIEmbeddingFunction
from meal_prep_agent.models.pydantic_recipe import Recipe

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
    
    ## REVISED RETRIEVER
    # def retrieve(
    #     self,
    #     user_ingredients: List[str],
    #     query: str = "",
    #     n: int = 10
    # ) -> List[Recipe]:
    #     """
    #     Retrieve recipes that match as many of the user's on-hand ingredients
    #     as possible. Embeddings are used only as a secondary reranker.
    #     """

    #     # Normalize user ingredients
    #     user_set = {u.lower() for u in user_ingredients}

    #     # 1. Load all recipes from Chroma
    #     all_results = self.collection.get(include=["metadatas"])
    #     all_metas = all_results["metadatas"]

    #     scored = []

    #     for meta in all_metas:
    #         # Decode ingredients
    #         ingredients = meta.get("ingredients")
    #         if isinstance(ingredients, str):
    #             try:
    #                 ingredients = json.loads(ingredients)
    #             except Exception:
    #                 continue

    #         recipe_set = {i.lower() for i in ingredients}

    #         # 2. Compute overlap score
    #         overlap = len(recipe_set.intersection(user_set))

    #         # Skip recipes with zero overlap
    #         if overlap == 0:
    #             continue

    #         scored.append((meta, overlap))

    #     # If nothing matches, fall back to embedding search
    #     if not scored:
    #         return self._vector_search(query, n)

    #     # 3. Sort by overlap descending
    #     scored.sort(key=lambda x: x[1], reverse=True)

    #     # 4. Take top K candidates for embedding reranking
    #     top_candidates = scored[:50]  # adjustable
    #     candidate_ids = [meta["id"] for meta, _ in top_candidates]

    #     # 5. Embedding search restricted to candidates
    #     results = self.collection.query(
    #         query_texts=[query],
    #         n_results=n,
    #         where={"id": {"$in": candidate_ids}}
    #     )

    #     # 6. Convert to Recipe objects
    #     recipes = []
    #     for meta in results["metadatas"][0]:
    #         ingredients = meta.get("ingredients")
    #         if isinstance(ingredients, str):
    #             ingredients = json.loads(ingredients)

    #         recipes.append(Recipe(title=meta["title"], ingredients=ingredients))

    #     return recipes

    


if __name__ == "__main__":
    retriever = Retriever()
    result = retriever.retrieve(query="strawberry", n=3)
    print(result)

