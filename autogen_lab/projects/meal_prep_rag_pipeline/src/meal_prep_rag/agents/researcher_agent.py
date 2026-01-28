"""
Researcher Agent

Responsible for:
- analyzing user queries
- calling the retriever tool
- returning structured recipe data
- avoiding synthesis or final answers
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

from meal_prep_rag.config import API_KEY, AGENT_MODEL
from meal_prep_rag.agents.tools import retrieve_recipes

model_client = OpenAIChatCompletionClient(model=AGENT_MODEL, api_key=API_KEY)

# Register the custom function as a tool
retriever_tool = FunctionTool(retrieve_recipes, description='A tool to retrieve recipes')

researcher = AssistantAgent(
    name="researcher",
    model_client=model_client,
    system_message=(
       "You are the Researcher agent in a multi-agent recipe retrieval system. " 
       "Your job is to analyze the user's query and gather factual information. " 
       "When recipe information is needed, ALWAYS call the `retrieve_recipes` tool. " 
       "Do not guess or fabricate information. " 
       "Return your findings as structured data, not narrative text. " 
       "Do not write final answers or summaries — that is the Writer agent's job."
    ),
    tools=[retriever_tool],
    reflect_on_tool_use=True
)

# Define task
task = "Find recipes that match criteria"

async def run_researcher(query: str):
    return await researcher.run(task=query)
