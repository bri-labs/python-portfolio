"""
autogen_frontend_streamlit.py
=============================

Streamlit UI for the Literature Review Assistant.

This frontend:
- collects user input (topic + number of papers)
- calls the async backend (`run_litrev`)
- streams the agent conversation in real time
- displays the final Markdown review

Run:
    streamlit run autogen_frontend_streamlit.py

    Runs Here:   Local URL: http://localhost:8501
"""

import asyncio
import streamlit as st

from autogen_lab.projects.research_assistant_agent.autogen_backend import run_litrev

# Define UI
st.set_page_config(page_title="Literature Review Assistant", page_icon="[BOOKS]")
st.title("[BOOKS] Literature Review Assistant")

query = st.text_input("Research topic")
n_papers = st.slider("Number of papers", 1, 10,5)

# setup search button
if st.button("Search") and query:   # If button clicked and query is populated

    async def _runner() -> None:
        chat_placehoder = st.container()
        async for frame in run_litrev(query, num_papers=n_papers):
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
    
    st.success("Review Complete [YAY]")
    
