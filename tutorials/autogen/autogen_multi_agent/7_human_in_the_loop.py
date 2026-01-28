"""
Purpose: Utlizes RoundRobinGroupChat and input from user (UserProxyAgent) to interact with a model
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
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who helps on the task given.'
)

user_agent = UserProxyAgent(        # Represents a user, waits for user to terminate (APPROVE) to actually stop
    name="UserProxy",
    description='A proxy agent that represent a user',
    input_func=input        # When run, gives flow to user
)

# Define termination condition
termination_condition = TextMentionTermination(text='APPROVE')

# Define team
team = RoundRobinGroupChat(
    participants=[assistant, user_agent],
    termination_condition=termination_condition
)

# Define Run
stream = team.run_stream(task='Write a nice 4 line poem about India')

async def main():
    await Console(stream)

if(__name__=='__main__'):
    asyncio.run(main())