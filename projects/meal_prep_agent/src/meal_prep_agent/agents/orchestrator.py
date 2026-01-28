import asyncio
import json

from meal_prep_agent.agents.researcher_agent import run_researcher
from meal_prep_agent.agents.writer_agent import run_writer
from meal_prep_agent.agents.critic_agent import run_critic

async def run_pipeline(user_query:str, n_recipes: int = 5):
    """
    Full multi-agent RAG workflow:
    1. Retrieve context from user query
    2. Researcher analyzes quesion + context to retrieve relevant recipes
    3. Writer summarizes output from Researcher into human-readable format
    4. Critic evaluates Writer output 
    5. Writer revises
    """

    # Step 1: Researcher retrieves structured data
    researcher_input = json.dumps({
        "query": user_query,
        "n_recipes": n_recipes
    })

    yield f"RESEARCHER INPUT: {researcher_input}"
    researcher_result = await run_researcher(researcher_input)
    researcher_content = researcher_result.messages[-1].content
    yield f"RESEARCHER RAW OUTPUT: {researcher_content}" 

    # Step 2: Writer generates human-readable output
    writer_result = await run_writer(researcher_content)
    writer_content = writer_result.messages[-1].content
    yield f"WRITER OUTPUT: {writer_content}" 

    # Step 3: Critic evalutes grounding (must be str, not dict)
    critic_input = f""" 
    Writer Output: 
    {writer_content} 
    
    Retrieved Data: 
    {researcher_content} 
    """
    critic_result = await run_critic(str(critic_input))
    critic_content = critic_result.messages[-1].content
    yield f"CRITC OUTPUT: {critic_content}"

    # Step 4: Writer takes in Critic feedback
    if "fully grounded" not in critic_content.lower():
        writer_revise_result = await run_writer(
            f"""
            Revise your answer based on this critique: " 
            {critic_content}

            Original answer:
            {writer_content}
            """
        )
        final_answer = writer_revise_result.messages[-1].content
    else:
        final_answer = writer_content

    # Final Output
    yield f"FINAL: {final_answer}"

if __name__ == "__main__":
    async def main():
        async for frame in run_pipeline("Find recipes with chicken and brocoli", n_recipes=5):
            print(frame)

    asyncio.run(main())
