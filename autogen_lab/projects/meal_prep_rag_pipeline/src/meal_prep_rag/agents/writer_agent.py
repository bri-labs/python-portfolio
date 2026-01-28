"""
Writer Agent

Responsible for:
- Receiving structured recipe data
- Turning data into polished repsponse
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from meal_prep_rag.config import API_KEY, AGENT_MODEL

model_client = OpenAIChatCompletionClient(model=AGENT_MODEL, api_key=API_KEY)

writer = AssistantAgent(
    name="writer",
    model_client=model_client,
    system_message=(
       "You are the Writer agent in a multi-agent recipe retrieval system. " 
       "Your receive structured recipe data from the Researcher agent. " 
       "Your job is to transform that data into a clear, helpful, human-readable answer. " 
       "Do not call tools. " 
       "Do not perform reserach. " 
       "Do not invent details that are not present in the provided data. "
       "Do not critique or evaluate - that is the Critic agent's job" 
    ),
)

# Define task
task = "Write a clear, grounded answer using the retrieved context explicitly"

async def run_writer(message: str):
    return await writer.run(task=message)