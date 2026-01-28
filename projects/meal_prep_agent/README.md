# Meal Prep RAG Pipeline
This project designs a Retrieval-Augmented (RAG) system that helps a user select personalized recipes for weekly meal prep. Users provide (3) inputs: 
    - List of ingredients they already have
    - Any dietary restrictions
    - Preferred category (breakfast, lunch, dinner, snack, dessert, or variety)
The system will then:
    - Retrieve relevant recipes from vector database (using the dataset listed below)
    - Filter out recipes based on dietary restrictions
    - Evaluate ingredient compatibility
    - Multi-agent RAG pipeline will then select a balanced set of meals (based on category selected) 

The final output will be a curated list of 5-10 recipes that the user can cook for the week. 

This project demonstrates dataset ingestion, vector database construction, embedding + retrieval, multi-agent reasoning, and filtering logic.  

Dataset: https://github.com/josephrmartinez/recipe-dataset/blob/main/13k-recipes.csv



