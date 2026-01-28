from pydantic import BaseModel
from typing import List

# Create Pydantic Recipe model
class Recipe(BaseModel):
    title: str
    ingredients: List[str]