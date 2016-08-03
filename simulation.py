import ingredient
import marketplace
import restaurant

# Create market
def basicSimulation():
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", initialWeight=10, 
									willingToBuy=True, willingToSell=True,
									sellWeight=20, minSellPrice=1.5,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6,
									avgPoundsConsumedPerHour=1.2, dollarsPerHourFromIngredient=1.75)
	sallys.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour=0, howMuchToRestockPounds=48)
	market.restaurants["Sally's"] = sallys

	# Add Rye & Market's restaurant
	rye_n_market = restaurant.Restaurant("Rye & Market", market=market)
	rye_n_market.ingredients["lemon"] = ingredient.Ingredient(name="lemon", initialWeight=10,
									willingToBuy=True, willingToSell=True,
									sellWeight=20, minSellPrice=1.5,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6,
									avgPoundsConsumedPerHour=1.2, dollarsPerHourFromIngredient=1.75) 
	rye_n_market.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour=24, howMuchToRestockPounds=48)
	market.restaurants["Rye & Market"] = rye_n_market

	for hour in xrange(48):
		print "*** HOUR %d" % hour
		for r in market.restaurants.values():
			r.anHourPassed(hour)
			if (hour % 1) == 0:
				r.display()

			market.matchBuyersAndSellers()
		#import pdb; pdb.set_trace()
		


basicSimulation()
