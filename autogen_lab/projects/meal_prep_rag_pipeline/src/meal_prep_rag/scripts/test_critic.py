import asyncio
from meal_prep_rag.agents.critic_agent import run_critic

# Simulated strcutred data from the Researcher
mock_data = """
=== Writer Output ===
Here are three delicious strawberry recipes you can try:

1. **Strawberry, Lemon and Basil**: A refreshing beverage or dessert topping made with:
   - 2 tablespoons fresh lemon juice
   - 1 tablespoon raw sugar
   - 6 fresh basil leaves
   - 5 small strawberries (or 3 large strawberries, quartered), plus 1 thin slice for garnish
   - 1 pinch kosher salt
   - 3/4 cup soda water

2. **Strawberry Coulis**: A simple and sweet sauce perfect for drizzling over desserts, made with:
   - 1 cup frozen unsweetened strawberries
   - 1/2 cup sugar
   - 1 tablespoon lemon juice

3. **Strawberries with Chocolate Caramel Sauce**: An indulgent treat featuring:
   - 1/4 cup sugar
   - 1/2 cup heavy cream
   - 2 oz fine-quality bittersweet chocolate (not unsweetened; no more than 60% cacao), coarsely chopped
   - 1/8 teaspoon salt
   - 1 tablespoon unsalted butter
   - 1 lb strawberries, halved if large
   - Accompaniment: lightly sweetened whipped cream

Enjoy experimenting with these recipes, whether you’re looking for a refreshing drink, a sauce, or a decadent dessert!
"""

async def main():
      
    message = (
        "Here is the human-readable summarized recipe data: \n"
        f"{mock_data}\n\n"
        "Check for any discrepancies"
    )

    result = await run_critic(message)
    print("\n=== Critic Output ===")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
