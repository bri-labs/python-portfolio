# ingest.py
"""
This module is reponsible for loading the raw csv, cleaning the dataset, 
saving a cleaned CSV, adn converting rows into Pydantic Recipe models.
"""
import pandas as pd
import ast

from meal_prep_agent.config import RAW_DATA_PATH, PROCESSED_DATA_PATH
from meal_prep_agent.models.pydantic_recipe import Recipe

# Load CSV
def load_csv(input_path:str, keep_columns:list = []) -> pd.DataFrame:
    df = pd.read_csv(input_path, usecols=keep_columns)
    print(f"Inital Load Shape: {df.shape}")

    return df

def parse_ingredients(value):
    # if it's alrady a list, just clean it
    if isinstance(value, list):
        return [i.strip() for i in value if i.strip()]
    # if it's a string that looks like a list, parse it
    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed,list):
                return [i.strip() for i in parsed if isinstance (i,str) and i.strip()]
        except Exception:
            return []   # fallback if parsing fails

# Clean dataframe
def clean_df(df:pd.DataFrame) -> pd.DataFrame:
    df['ingredients'] = df['Cleaned_Ingredients'].apply(parse_ingredients)
    df.drop(columns='Cleaned_Ingredients', inplace=True)
    df.rename(columns={'Title': 'title'}, inplace=True)

    # Drop rows missing title or ingredients
    df.dropna(subset=['title', 'ingredients'], inplace=True)
    print(f"Filter Null Shape: {df.shape}")

    # Check type
    sample = df['ingredients'].iloc[0]
    if isinstance(sample, list):
        print("Loaded ingredients as a list")

    return df

# Create Pydantic objects
def create_pydantic_recipes(df:pd.DataFrame):
    records = df.to_dict(orient="records")
    recipes = [Recipe(**row) for row in records]    # unpack reach dict in records to Recipe model, compile as list
    
    # print("Example recipe:")
    # print(recipes[0].model_dump())
    
    return recipes

def main():
    print("++ Loading and Cleaning CSV ++")
    df = load_csv(RAW_DATA_PATH, keep_columns=['Title', 'Cleaned_Ingredients'])
    df = clean_df(df)
    
    # export cleaned results to `data/processed`
    print(f"++ Export cleaned results to: {PROCESSED_DATA_PATH}")
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("++ Create pydantic Recipe models++ ")
    recipes = create_pydantic_recipes(df)

    return recipes

if __name__ == "__main__":
    result = main()


