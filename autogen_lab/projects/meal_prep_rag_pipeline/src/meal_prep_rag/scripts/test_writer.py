import asyncio
from meal_prep_rag.agents.writer_agent import run_writer

# Simulated strcutred data from the Researcher
mock_data = {
    "recipes": [
        {
        "title": "Strawberry, Lemon and Basil",
        "ingredients": [
            "2 tablespoons fresh lemon juice",
            "1 tablespoon raw sugar",
            "6 fresh basil leaves",
            "5 small strawberries (or 3 large strawberries, quartered) plus 1 thin slice for garnish",
            "1 pinch kosher salt",
            "3/4 cup soda water"
        ]
        },
        {
        "title": "Strawberry Coulis",
        "ingredients": [
            "1 cup frozen unsweetened strawberries",
            "1/2 cup sugar",
            "1 tablespoon lemon juice"
        ]
        },
        {
        "title": "Strawberries with Chocolate Caramel Sauce",
        "ingredients": [
            "1/4 cup sugar",
            "1/2 cup heavy cream",
            "2 oz fine-quality bittersweet chocolate (not unsweetened; no more than 60% cacao if labeled), coarsely chopped",
            "1/8 teaspoon salt",
            "1 tablespoon unsalted butter",
            "1 lb strawberries, halved if large",
            "Accompaniment: lightly sweetened whipped cream"
        ]
        }
    ]
    }

async def main():
      
    message = (
        "Here is the retrieved recipe data: \n"
        f"{mock_data}\n\n"
        "Write a helpful explanation for the user"
    )

    result = await run_writer(message)
    print("\n=== Writer Output ===")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
