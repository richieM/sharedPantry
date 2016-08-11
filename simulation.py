import ingredient
import marketplace
import restaurant
import random
import math

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


	simData = market.gatherSimData();

	return simData


def experiment1():
	"""
	Medium size market -- 7 players
	Restaurant only orders what they need for the day
	Lots of trading...

	Outcomes:
	Freshness!
	Always have what you need
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

	simData = market.gatherSimData();

	return simData

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

def dynamicSim(params, ingrName):
	"""
	Take in params from the frontEnd and passes them to a sim :)
	"""
	bulkResupplyChunkSize = 100

	market = marketplace.Marketplace(bulkResupplySize=bulkResupplyChunkSize)

	ingredientName = ingrName
	howManyRestaurants = int(params["participants"])
	duration = int(params["duration"])
	unpredictability = float(params["unpredictability"]) / 100
	expirationTime = int(params["expirationTime"]) * 24 # expirationTime is in days on the graph
	consumptionRate = int(params["consumptionRate"])
	unitPrice = int(params["unitPrice"])

	totalAmountOfFoodPerDay = consumptionRate * howManyRestaurants

	percentageOfRestaurantsWithStorageSpace = .3
	numLargeRestaurants = math.ceil(howManyRestaurants * .3)
	numSmallRestaurants = howManyRestaurants - numLargeRestaurants
	
	for n in xrange(howManyRestaurants):
		currRestaurant = restaurant.Restaurant(n, market=market)
		randomConsumptionRateHourly = randomVal(consumptionRate)
		sellWeight = randomConsumptionRateHourly * 12 # TODO
		buyWeight = randomConsumptionRateHourly * 3
		currRestaurant.ingredients[ingredientName] = ingredient.Ingredient(name=ingredientName, expirationTime=randomVal(expirationTime), restaurant=currRestaurant,
										willingToBuy=True, willingToSell=True,
										sellWeight=sellWeight, buyWeight=buyWeight,
										avgPoundsConsumedPerHour=randomConsumptionRateHourly, dollarsPerHourFromIngredient=unitPrice, randomnessInDemand=randomVal(unpredictability))
		
		#TODO fix this to be smarter. probably put all the restock logic in the marketplace and not in the ingredients...
		if n < numLargeRestaurants:
			currRestaurant.restockable = True
		
		market.restaurants[currRestaurant.name] = currRestaurant

	for hour in xrange(duration):
		market.anHourPassed(hour)

	simData = market.gatherSimData();

	return simData

def randomVal(val):
	stDev = val/4.0
	return int(random.gauss(val, stDev))
	


#experiment1()
#controlExactNeeds()
#basicSimulation()
#superHighTechSim()
