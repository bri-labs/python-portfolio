"""
autogen_backend.py
===================

Backend for the Literature Review Assistant.

This module defines:
- a custom arXiv search tool
- two AutoGen agents (search_agent and summarizer)
- a RoundRobinGroupChat team
- an async streaming orchestrator (`run_litrev`)

The system retrieves relevant arXiv papers and generates a structured
Markdown literature review using a multi-agent workflow.
"""



from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Dict, List

import arxiv
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import (
    TextMessage
)
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# ----
# 1. Tool Definition
# ---

# Arxiv - wrapper to help search for papers in arxiv database
def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Query the arXiv API and return a compact list of papers.

    Parameters
    ----------
    query : str
        Search query string (e.g., "graph neural networks chemistry").
    max_results : int, optional
        Maximum number of papers to retrieve before filtering.

    Returns
    -------
    List[Dict]
        Each dictionary contains:
        - title : str
        - authors : List[str]
        - published : str (YYYY-MM-DD)
        - summary : str
        - pdf_url : str

    Notes
    -----
    This function is wrapped as an AutoGen FunctionTool so that
    agents can invoke it during tool-use steps.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers: List[Dict] = []
    for result in client.results(search):
        papers.append(
            {
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "published": result.published.strftime("%Y-%m-%d"),
                "summary": result.summary,
                "pdf_url": result.pdf_url,
            }
        )
    return papers

# Wrap arxiv search into FunctionTool
arxiv_tool = FunctionTool(
    arxiv_search,
    description=(
        "Searches arXiv and returs up to *max_results* papers, each containing"
        "title, authors, publication date, abstract, and pdf_url."
    )
)

# ---
# 2. Define Agent and Buld Team
# ---
def build_team(model: str = 'gpt-4o-mini') -> RoundRobinGroupChat:
    """
    Construct the two-agent AutoGen team.

    Parameters
    ----------
    model : str
        Model name for the OpenAIChatCompletionClient.

    Returns
    -------
    RoundRobinGroupChat
        A team consisting of:
        - search_agent : retrieves and filters arXiv papers
        - summarizer : produces a Markdown literature review
    """
    llm_client = OpenAIChatCompletionClient(model=model, api_key=api_key)

    # Agent that **only** calls the arXiv tool and forwards top-N papers
    search_agent = AssistantAgent(
        name="search_agent",
        description="Crafts arXiv queries and retrieves candidate papers.",
        system_message=(
            "Given a user topic, think of the best arXiv query and call the "
            "provided tool. Always fetch five-times the papers requested so "
            " that you can down-select the most relevant ones. When the tool "
            " returns, choose exactly the number of papers requested and pass "
            " them as concise JSON to the summarizer."
        ),
        tools=[arxiv_tool],
        model_client=llm_client,
        reflect_on_tool_use=True,
    )

    # Agent that writes the final literature review
    summarizer = AssistantAgent(
        name="summarizer",
        description="Produces a short Markdown review from provided papers.",
        system_message=(
            "You are an expert researcher. When you receive hte JSON list of "
            "papers, write a literature-review style report in Markdown: \n" \
            "1. Start with a 2-3 sentence introduction of the topic. \n" \
            "2. Then include one bullet per paper with: title (as Markdown link), "
            "authrs, the specfic problem tackled, and its key contributions.\n" \
            "3. Close with a single-sentence takeaway."
        ),
        model_client=llm_client,
    )

    return RoundRobinGroupChat(
        participants=[search_agent, summarizer],
        max_turns=2
    )

# ---
# 3. Orchestrator (build our team and instruct how to run)
# ---

async def run_litrev(topic: str, num_papers: int = 5, model: str = 'gpt-4o-mini') -> AsyncGenerator[str, None]:
    """
    Run the literature review workflow and stream agent messages.

    Parameters
    ----------
    topic : str
        Research topic to search for.
    num_papers : int
        Number of papers to include in the final review.
    model : str
        Model used by both agents.

    Yields
    ------
    str
        Streaming messages in the format: "agent_name: content"
    """

    team = build_team(model=model)
    task_prompt = (
        f"Conduct a literature review on **{topic}** and return exactly {num_papers} papers."
    )

    async for msg in team.run_stream(task=task_prompt):
        if isinstance(msg, TextMessage):
            yield f"{msg.source}: {msg.content}"


# ---
# 4. CLI testing
# ---
if __name__=="__main__":
    async def _demo() -> None:
        async for line in run_litrev("graph neural networks for chemistry", num_papers=5):
            print(line)
    asyncio.run(_demo())