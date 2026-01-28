"""
streamlit_app.py
=============================

Streamlit UI for the Meal Prep RAG Pipeline

This frontend:
- collects user input (topic + number of papers)


Run:
    streamlit run streamlit_app.py

    Runs Here:   Local URL: http://localhost:8501
"""

import asyncio
import streamlit as st

from meal_prep_rag.agents.orchestrator import run_pipeline

# Define UI
st.set_page_config(page_title="Meal Prep RAG Pipeline", page_icon="🍽️")
st.title("🍽️ Meal Prep RAG Pipeline")

query = st.text_input("Ingredients to include")
n_recipes = st.slider("Number of recipes", 1, 10,5)

# setup search button
if st.button("Search") and query:   # If button clicked and query is populated

    async def _runner() -> None:
        chat_placehoder = st.container()
        async for frame in run_pipeline(query, n_recipes):
            role, *rest = frame.split(":", 1)
            content = rest[0].strip() if rest else ""
            with chat_placehoder:
                with st.chat_message("assistant"):
                    st.markdown(f"**{role}**: {content}")

    with st.spinner("Working..."):
        try:
            asyncio.run(_runner())
        except RuntimeError:
            # Fallback when an event loop is alrady running
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_runner())
    
    st.success("Review Complete ⌛️")
    