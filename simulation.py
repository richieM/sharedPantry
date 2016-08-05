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

	simData = market.gatherSimData();

	return simData

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

def experiment1():
	"""
	Medium size market -- 7 players
	Restaurant only orders what they need for the day
	Lots of trading...
	Everyone's reorders are synchronized

	Outcomes:
	Freshness!
	Always have what you need?
	"""
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	for n in xrange(7):
		currRestaurant = restaurant.Restaurant(n, market=market)
		currRestaurant.ingredients["lemon"] = ingredient.Ingredient(name="lemon", expirationTime=168, restaurant=currRestaurant,
										willingToBuy=True, willingToSell=True,
										sellWeight=3,
										buyWeight=2, maxBuyPrice=3, preferredPurchaseAmount=4,
										avgPoundsConsumedPerHour=1, dollarsPerHourFromIngredient=4, randomnessInDemand=.3)
		currRestaurant.ingredients["lemon"].setRestockParams(restockEveryHours=168, restockOnHour= n * 24, howMuchToRestockPounds=168)
		market.restaurants[currRestaurant.name] = currRestaurant

	for hour in xrange(168):
		market.anHourPassed(hour)

def controlExactNeeds():
	"""
	Control experiment

	Only one user
	No trading
	Buys a little less than they need

	Outcomes:
	A few disappointed customers
	.5 shitty quality
	"""
	print "** Create a market **"
	market = marketplace.Marketplace()

	# Add Sally's restaurant
	sallys = restaurant.Restaurant("Sally's", market=market)
	sallys.ingredients["lemon"] = ingredient.Ingredient(name="lemon", expirationTime=168, restaurant=sallys,
									willingToBuy=True, willingToSell=True,
									sellWeight=20,
									buyWeight=5, maxBuyPrice=2, preferredPurchaseAmount=6,
									avgPoundsConsumedPerHour=1, dollarsPerHourFromIngredient=4, randomnessInDemand=.3)
	sallys.ingredients["lemon"].setRestockParams(restockEveryHours=168, restockOnHour=0, howMuchToRestockPounds=168)
	market.restaurants["Sally's"] = sallys

	for hour in xrange(168):
		market.anHourPassed(hour)

	simData = market.gatherSimData();

	return simData

#experiment1()
#controlExactNeeds()
#basicSimulation()
#superHighTechSim()
