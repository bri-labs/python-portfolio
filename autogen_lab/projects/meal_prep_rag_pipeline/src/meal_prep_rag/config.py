from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# Project root (3) levels up
# config.py -> meal_prep_rag -> src -> project root
BASE_DIR = CURRENT_FILE.parents[2]

# data paths
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "13k-recipes.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "recipes_clean.csv"

# Vectorstore path
VECTORSTORE_PATH = BASE_DIR / "vectorstore"

# Embedding Model
EMBEDDING_MODEL = "text-embedding-3-small"