"""
Purpose: Utlizes RoundRobinGroupChat 
"""

import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Define model client (brain)
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

# Define Agents
assistant = AssistantAgent(
    name='Writer',
    description='you are a great writer',
    model_client=model_client,
    system_message='You are a really helpful writer who writes in less than 30 words.'
)

assistant2 = AssistantAgent(
    name='Reviewer',
    description='you are a great reviewer',
    model_client=model_client,
    system_message='You are a really helpful reviewer who writes in less than 30 words...'
)

assistant3 = AssistantAgent(
    name='Editor',
    description='you are a great editor',
    model_client=model_client,
    system_message='You are a really helpful editor who writes in less than 30 words...'
)

# Define team & ttermination condition
team = RoundRobinGroupChat(
    participants=[assistant, assistant2, assistant3],
    max_turns=3
)

# Define Run
async def main():
    task = 'Write a 3 line poem about the sky'

    while True:
        stream = team.run_stream(task=task)     # Keeps context, as once finished, updated task loaded and stored
        await Console(stream)  

        feedback = input('Please provide your feedback (type "exit" to stop): ')
        if(feedback.lower().strip()=='exit'):
            break

        task = feedback

if(__name__=='__main__'):
    asyncio.run(main())