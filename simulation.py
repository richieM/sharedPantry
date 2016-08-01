import ingredient
import marketplace
import restaurant

# Create market
def basicSimulation():
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", money=100, market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToBuy=True,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6)
	market.restaurants["Sally's"] = sallys

	# Add Rye & Market's restaurant
	rye_n_market = restaurant.Restaurant("Rye & Market", money=100, market=market)
	rye_n_market.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToSell=True,
									sellWeight=10, minSellPrice=1.5) 
	market.restaurants["Rye & Market"] = rye_n_market

	# Set initial ingredient weights
	market.restaurants["Sally's"].updateIngredientWeight("lemon", 10)
	market.restaurants["Rye & Market"].updateIngredientWeight("lemon", 5)

	# Set weights to trigger a buy and sell transaction
	market.restaurants["Sally's"].updateIngredientWeight("lemon", 4)
	market.restaurants["Rye & Market"].updateIngredientWeight("lemon", 20)

	import pdb; pdb.set_trace()

basicSimulation()
