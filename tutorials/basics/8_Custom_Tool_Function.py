import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

# Load API Key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI model client
openai_client = OpenAIChatCompletionClient(model='gpt-4o-mini', api_key=api_key)

# Define custom function to reverse string
# NOTE: Important to define variable types and docstring, as shared with LLM to help figure out best tool
def reverse_string(text: str) -> str:
    """Reverse the given text.
        input: str

        output: str
        The reversed String is returned.
    """
    return text[::-1]


        
# Registor the custom function as a tool
reverse_tool = FunctionTool(reverse_string, description='A tool to reverse a string')

# Create an agent with the custom tool
agent = AssistantAgent(
    name='ReverseAgent',
    model_client=openai_client,
    system_message='You are a helpful assistant that can reverse a text using the reverse_string_tool. Give the result with the summary.',
    tools=[reverse_tool],
    reflect_on_tool_use=True,        # Will look at the output and see if answer needs to be additional wording (doesn't just return function answer)
)

# Define task
task = "Reverse the text 'Hello, how are you?'"

# Run the agent
async def main():
    result = await agent.run(task=task)

    print(result)
    print(f"Agent Response: {result.messages[-1].content}")

if __name__=="__main__":
     asyncio.run(main())

