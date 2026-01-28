import asyncio
from meal_prep_rag.agents.researcher_agent import run_researcher

async def main():
    query = "Find strawberry recipes"
    result = await run_researcher(query)
    print("\n=== Researcher Output ===")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
