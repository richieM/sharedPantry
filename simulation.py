import ingredient
import marketplace
import restaurant
import random
import math

def dynamicSim(params, ingrName, randomConsumptionRates, control=False):
	"""
	Take in params from the frontEnd and passes them to a sim :)
	"""
	bulkResupplyChunkSize = 100

	ingredientName = ingrName
	howManyRestaurants = int(params["participants"])
	duration = int(params["duration"]) * 24 # duration is in days, so convert to hours
	unpredictability = float(params["unpredictability"]) / 100
	expirationTime = int(params["expirationTime"]) * 24 # expirationTime is in days on the graph
	avgConsumptionRate = float(params["consumptionRate"])
	unitPrice = float(params["unitPrice"])

	totalAmountOfFoodPerDay = avgConsumptionRate * howManyRestaurants

	percentageOfRestaurantsWithStorageSpace = .3
	numLargeRestaurants = math.ceil(howManyRestaurants * .3)
	numSmallRestaurants = howManyRestaurants - numLargeRestaurants

	market = marketplace.Marketplace(bulkResupplySize=bulkResupplyChunkSize,
										expirationTime = expirationTime,
										control=control)
	
	for n in xrange(howManyRestaurants):
		currRestaurant = restaurant.Restaurant(n, market=market)
		randomConsumptionRateHourly = randomConsumptionRates[n]

		if control:
			sellWeight = 9999999.99 # impossibly high number
		else:
			sellWeight = randomConsumptionRateHourly * 12 # TODO

		buyWeight = randomConsumptionRateHourly * 3
		currRestaurant.ingredients[ingredientName] = ingredient.Ingredient(name=ingredientName, expirationTime=expirationTime, restaurant=currRestaurant,
										willingToBuy=True, willingToSell=True,
										sellWeight=sellWeight, buyWeight=buyWeight,
										avgPoundsConsumedPerHour=randomConsumptionRateHourly, dollarsPerHourFromIngredient=unitPrice, randomnessInDemand=unpredictability)
		
		#TODO fix this to be smarter. probably put all the restock logic in the marketplace and not in the ingredients...
		if n < numLargeRestaurants:
			currRestaurant.restockable = True
		
		market.restaurants[currRestaurant.name] = currRestaurant

	for hour in xrange(duration):
		market.anHourPassed(hour)

	simData = market.gatherSimData();

	return simData

def runSims(params, ingrName):
	consumpRate = float(params["consumptionRate"])
	howManyRestaurants = int(params["participants"])
	randomConsumptionRates = []

	while len(randomConsumptionRates) < howManyRestaurants:
		randomConsumptionRates.append(random.gauss(consumpRate, consumpRate/4.0))

	simData = dynamicSim(params, ingrName, randomConsumptionRates)
	controlData = dynamicSim(params, ingrName, randomConsumptionRates, control=True)

	return (simData, controlData)

#experiment1()
#controlExactNeeds()
#basicSimulation()
#superHighTechSim()
