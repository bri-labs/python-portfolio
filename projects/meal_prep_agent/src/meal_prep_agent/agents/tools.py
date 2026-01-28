from meal_prep_agent.retriever import Retriever

def retrieve_recipes(query: str, n: int = 5):
    retr = Retriever()
    recipes = retr.retrieve(query, n)
    return [r.model_dump() for r in recipes]