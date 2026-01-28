import asyncio
import json
from meal_prep_agent.agents.researcher_agent import run_researcher

async def main():
    query = "Find recipes with strawberry, chicken, blueberries"
    n_recipes = 10

    researcher_input = json.dumps({
        "query": query,
        "n_recipes": n_recipes
    })
    result = await run_researcher(researcher_input)
    print("\n=== Researcher Output ===")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
