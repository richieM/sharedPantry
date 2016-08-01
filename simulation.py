import ingredient
import marketplace
import restaurant

# Create market
def basicSimulation():
	market = marketplace.Marketplace()

	# Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", money=100, market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToBuy=True,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=5)
	market.restaurants["Sally's"] = sallys

	# Rye & Market's restaurant
	rye_n_market = restaurant.Restaurant("Rye & Market", money=100, market=market)
	rye_n_market.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToSell=True,
									sellWeight=10, minSellPrice=1.5) 
	market.restaurants["Rye & Market"] = rye_n_market

	import pdb; pdb.set_trace()

basicSimulation()
