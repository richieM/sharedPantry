import ingredient
import marketplace
import restaurant

# Create market
def basicSimulation():
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", money=100.0, market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToBuy=True,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6)
	market.restaurants["Sally's"] = sallys

	# Add Rye & Market's restaurant
	rye_n_market = restaurant.Restaurant("Rye & Market", money=100, market=market)
	rye_n_market.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToSell=True,
									sellWeight=10, minSellPrice=1.5) 
	market.restaurants["Rye & Market"] = rye_n_market

	# Set initial ingredient weights
	print "** Initial setup **"
	market.restaurants["Sally's"].updateIngredientWeight("lemon", 10)
	market.restaurants["Rye & Market"].updateIngredientWeight("lemon", 5)

	for r in market.restaurants.values():
		r.display()

	print "** Buy and sell transactions are added **"
	# Set weights to trigger a buy and sell transaction
	market.restaurants["Sally's"].updateIngredientWeight("lemon", 4)
	market.restaurants["Rye & Market"].updateIngredientWeight("lemon", 20)

	for r in market.restaurants.values():
		r.display()

	market.matchBuyersAndSellers()

	print
	print
	print "** After Transaction! **"
	for r in market.restaurants.values():
		r.display()

basicSimulation()
