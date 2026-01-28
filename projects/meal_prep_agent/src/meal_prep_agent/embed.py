# embed.py
import pandas as pd
import chromadb
import time
import ast
import json

from chromadb.config import Settings
from chromadb.api.models import Collection
from openai import OpenAI

from meal_prep_agent.config import PROCESSED_DATA_PATH, VECTORSTORE_PATH, EMBEDDING_MODEL, API_KEY
from meal_prep_agent.models.openai_embedding import OpenAIEmbeddingFunction

EMBEDDING_BATCH_SIZE = 200
     
def create_vectorstore(store_path):
    db_path = store_path / 'chroma_db_rag_recipes'
    print(f"++ Create Chroma Vector Store at `{db_path}`")
    
    # Create file-based vector store
    client_settings = Settings(anonymized_telemetry=False)
    client = chromadb.PersistentClient(path=db_path, settings=client_settings)

    return client


def load_clean_data(csv_path: str):
    print("++ Load Clean CSV")
    df = pd.read_csv(csv_path)

    # Convert list-looking string back into real lists
    df["ingredients"] = df["ingredients"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    return df

def apply_doc_format(row:dict) -> str:
    title = row['title'].lower()
    ingredients = [i.lower() for i in row['ingredients']]

    doc = f"title: {title}\n\ningredients: {','.join(ingredients)}"
    
    return doc

def generate_doc_col(df):
    print("++ Apply doc column format")
    df['doc'] = df.apply(apply_doc_format, axis=1)
    df.head(5)

    return df

def apply_metadata_col(row: dict) -> dict:
    metadata = {
        "title": row["title"],
        "ingredients": json.dumps(row['ingredients'])   # list -> JSON string
    }
    return metadata

def generate_metadata_col(df):
    print("++ Apply metadata column")
    df['metadata'] = df.apply(apply_metadata_col, axis=1)
    df.head(5)

    return df

# Batch helper function
def batch(iterable, batch_size): 
    for i in range(0, len(iterable), batch_size): 
        yield iterable[i:i + batch_size]

def generate_openai_embeddings(df: pd.DataFrame, batch_size: int, collection:Collection):
    # Add documents to chroma in batches
    print("++ Generate embedding and add to Chroma DB")
    
    # Convert elements to embed into lists
    docs = df['doc'].tolist()
    ids = df['id'].tolist()
    metas = df['metadata'].tolist()
    
    # Stats - get total df length to calculate total batches
    total = len(df)
    num_batches = (total // batch_size) + 1

    # For each batch, send to openai to embed
    # NOTE: Executed this way, as can't send whole df elements in one api call (limit on tokens)
    for batch_idx, (docs_batch, ids_batch, meta_batch) in enumerate(
        zip(
            batch(docs, batch_size),
            batch(ids, batch_size),
            batch(metas, batch_size),
        )
    ):
        # Add to chroma collection
        start = time.time()
        collection.add(
            documents=docs_batch,
            ids=ids_batch,
            metadatas=meta_batch        
        )
        print(f"Embedding Batch {batch_idx + 1}/{num_batches} took {time.time() - start:.2f}s")
    
    print(f"Completed embedding {len(df)} recipes across {num_batches} batches")

def main():
    # Create Vectorestore
    chroma_client = create_vectorstore(VECTORSTORE_PATH)

    # Create embedding function
    openai_client = OpenAI(api_key=API_KEY)
    embedding_fn = OpenAIEmbeddingFunction(openai_client, EMBEDDING_MODEL)

    # Create chroma collection
    collection = chroma_client.get_or_create_collection(
        name="rag_recipes",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}   # Use cosine as standard metric for semantic embeddings
    )

    # Load clean CSV
    df = load_clean_data(PROCESSED_DATA_PATH)
    
    # Add additional columns
    df = generate_doc_col(df)
    df = generate_metadata_col(df)
    df['id'] = df.index.astype(str)     # create unique IDs column     

    # Add documents to chroma in batches
    generate_openai_embeddings(df=df, batch_size=EMBEDDING_BATCH_SIZE, collection=collection)

    # Sanity Check stats
    print("---")
    print(f"Ingested receipe dataframe rows: {len(df)}")
    print(f"Total embeddings stored: {collection.count()}")
    sample = collection.query(
        query_texts = ["strawberry"],
        n_results=1
    )
    print(f"Sample chroma documents: \n{sample}")
    
if __name__ == "__main__":
    main()