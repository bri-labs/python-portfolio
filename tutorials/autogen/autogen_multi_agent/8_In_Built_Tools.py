import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv
from autogen_core import CancellationToken
from autogen_ext.tools.http import HttpTool
import os

# Load API Key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


# Initialize OpenAI model client
openai_client = OpenAIChatCompletionClient(model='gpt-4o-mini', api_key=api_key)

# Specifies schema expect request response to come back as
schema = {
    "type": "object",
    "properties" : {
        "fact" : {
            "type":"string",
            "description": "A random cat fact"
        },
        "length": {
            "type":"integer",
            "description": "Length of the cat fact"
        }
    },
    "required": ["fact", "length"]
    
    }

# Url: https://catfact.ninja/fact
http_tool = HttpTool(
    name='cat_facts_api',
    description='Fetch random cat facts from the Cat Facts API',
    scheme='https',
    host = 'catfact.ninja',
    port=443,
    path='/fact',
    method='GET',
    return_type='json',
    json_schema=schema)

# Define a custome function to reverse a string
def reverse_string(text: str) -> str:
    """Reverse the given text.
        input: str

        output: str
        The reversed String is returned.
    """
    return text[::-1]

async def main():
    # Create an assistant with the base64 tool
    assistant = AssistantAgent(
        name="cat_fact_agent",
        model_client=openai_client,
        tools=[http_tool, reverse_string],
        system_message='You are a helpful assistant that can fetch random cats and reverse strings using Tools.'
    )

    # The assistant can now use base64 tool to decode the string
    response = await assistant.on_messages(
        [TextMessage(content='can you please get a random cat fact.', source='user')],
        CancellationToken(),
    )
    print(response.chat_message)

if __name__=="__main__":
     asyncio.run(main())



