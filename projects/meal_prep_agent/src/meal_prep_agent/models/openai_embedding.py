class OpenAIEmbeddingFunction:
    def __init__(self, client, model: str):
        self.client = client
        self.model = model

    # Chroma uses for embedding for embedding documents when adding to the collection
    def __call__(self, input: list[str]) -> list[list[float]]:     
        response = self.client.embeddings.create(
            model=self.model,
            input=input # whole batch
        )
        return [item.embedding for item in response.data]
    
    # Chroma uses for embedding queries when calling collection.query() 
    def embed_query(self, input: list[str]) -> list[list[float]]: 
        response = self.client.embeddings.create( 
            model=self.model, 
            input=input ) 
        return [item.embedding for item in response.data]
    
    # chroma requires `name` for conflict detection
    def name(self) -> str:
        return f"openai={self.model}"