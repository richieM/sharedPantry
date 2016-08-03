import ingredient
import marketplace
import restaurant
import random

# Create market
def basicSimulation():
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", expirationTime=48, restaurant=sallys,
									willingToBuy=True, willingToSell=True,
									sellWeight=20,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6,
									avgPoundsConsumedPerHour=1, dollarsPerHourFromIngredient=1.75)
	sallys.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour=0, howMuchToRestockPounds=48)
	market.restaurants["Sally's"] = sallys

	# Add Rye & Market's restaurant
	rye_n_market = restaurant.Restaurant("Rye & Market", market=market)
	rye_n_market.ingredients["lemon"] = ingredient.Ingredient(name="lemon", expirationTime=48, restaurant=rye_n_market,
									willingToBuy=True, willingToSell=True,
									sellWeight=20,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6,
									avgPoundsConsumedPerHour=1, dollarsPerHourFromIngredient=1.75) 
	rye_n_market.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour=24, howMuchToRestockPounds=48)
	market.restaurants["Rye & Market"] = rye_n_market

	for hour in xrange(48):
		market.anHourPassed(hour)

def superHighTechSim():
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	for n in xrange(10):
		currRestaurant = restaurant.Restaurant(n, market=market)
		currRestaurant.ingredients["lemon"] = ingredient.Ingredient(name="lemon", expirationTime=48, restaurant=currRestaurant,
										willingToBuy=True, willingToSell=True,
										sellWeight=20,
										buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=10,
										avgPoundsConsumedPerHour=1, dollarsPerHourFromIngredient=1)
		currRestaurant.ingredients["lemon"].setRestockParams(restockEveryHours=48, restockOnHour= (int) (random.random() * 48), howMuchToRestockPounds=48)
		market.restaurants[currRestaurant.name] = currRestaurant

	for hour in xrange(1000):
		market.anHourPassed(hour)



superHighTechSim()
