import ingredient
import marketplace
import restaurant

# Create market
def basicSimulation():
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToBuy=True,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6, avgPoundsConsumedPerHour=24.0/48)
	sallys.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour=0)
	market.restaurants["Sally's"] = sallys

	# Add Rye & Market's restaurant
	rye_n_market = restaurant.Restaurant("Rye & Market", market=market)
	rye_n_market.ingredients["lemon"] = ingredient.Ingredient(name="lemon", willingToSell=True,
									sellWeight=10, minSellPrice=1.5, avgPoundsConsumedPerHour=24.0/48) 
	rye_n_market.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour=24)
	market.restaurants["Rye & Market"] = rye_n_market

	# Set initial ingredient weights
	print "** Initial setup **"
	market.restaurants["Sally's"].updateIngredientWeight("lemon", 10)
	market.restaurants["Rye & Market"].updateIngredientWeight("lemon", 5)

	for hour in xrange(96):
		for r in market.restaurants.values():
			r.anHourPassed(hour)
			market.matchBuyersAndSellers()
			if (hour % 20) == 0:
				print "*** HOUR %d" % hour
				r.display()


basicSimulation()
