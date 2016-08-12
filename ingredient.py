import random

base_ingredient_prices = {"lemon": (1.2, 1.0)}
bulk_lemon_cost = 1

class Ingredient:
	"""
	Ingredients that a restaurant has that they can buy or sell.
	Each ingredient at a restaurant has it's own unique instance
	"""

	def __init__(self, name=0, expirationTime=48.0, restaurant=None, willingToSell=False, willingToBuy=False, buyWeight=0, sellWeight=0, maxBuyPrice=0, dollarsPerHourFromIngredient=1, avgPoundsConsumedPerHour=.1, randomnessInDemand=.1):
		self.name = name

		self.expirationTime = expirationTime
		self.restaurant = restaurant
		self.ingrChunks = []

		self.willingToSell = willingToSell
		self.willingToBuy = willingToBuy

		self.buyWeight = buyWeight
		self.maxBuyPrice = maxBuyPrice

		self.sellWeight = sellWeight

		self.dollarsPerHourFromIngredient = dollarsPerHourFromIngredient
		self.avgPoundsConsumedPerHour = avgPoundsConsumedPerHour
		self.randomnessInDemand = randomnessInDemand

		self.profit = 0

		## Important Metrics
		self.amountOfWastedFood = 0
		self.hoursWithoutIngredient = 0
		self.totalFreshness = 0
		self.totalFoodConsumed = 0

		self.currentHour = -1

		# Register this ingredient on the Seller marketplace
		self.restaurant.placeSellRequest(self)

		self.setupSimData()

	def setupSimData(self):
		self.simData = {}

		self.simData["profit"] = []
		self.simData["hoursWithout"] = []
		self.simData["waste"] = []
		self.simData["avgFreshness"] = []

	def getSimData(self):
		return self.simData

	def recordSimData(self):
		self.simData["profit"].append(self.profit)
		self.simData["hoursWithout"].append(self.hoursWithoutIngredient)
		self.simData["waste"].append(self.amountOfWastedFood)
		if self.totalFreshness == 0:
			avgFreshness = 0
		else:
			avgFreshness = self.totalFreshness / self.totalFoodConsumed 
		self.simData["avgFreshness"].append(avgFreshness)

	def anHourPassed(self, hour):
		# Eat some food, make some cash, maybe order more...

		# calculate current demand in pounds
		originalWeight = self.getWeight();
		self.currentHour = hour

		self.throwAwayOldFood()
		self.feedCustomers(originalWeight)

		self.recordSimData()

	def restockFood(self, howMuchToRestock, control=False):
		
		restockedFood = IngrChunk(weight=howMuchToRestock, hourCreated=self.currentHour, ingr=self)
		self.ingrChunks.append(restockedFood)

		# subtract the cost of the restock from revenue
		

		if control:
			highPrice, unused = base_ingredient_prices[self.name]
			ingrPrice = highPrice
		else:
			ingrPrice = bulk_lemon_cost

		costOfRestock = howMuchToRestock * ingrPrice # you buy at bulk cost...
		self.profit -= costOfRestock

	def feedCustomers(self, originalWeight):
		howMuchFoodToServe = self.avgPoundsConsumedPerHour * (1 + random.uniform(-1 * self.randomnessInDemand, self.randomnessInDemand))

		howMuchWeServed, totalFreshness = self.consumeFood(howMuchFoodToServe)
		self.totalFoodConsumed += howMuchWeServed
		self.totalFreshness += totalFreshness

		self.profit += howMuchWeServed * self.dollarsPerHourFromIngredient
		if howMuchFoodToServe != 0: # TODO oops hacky
			self.hoursWithoutIngredient += (howMuchFoodToServe - howMuchWeServed) / (howMuchFoodToServe)

		if self.willingToBuy:
			if self.getWeight() < self.buyWeight:
				self.restaurant.placeBuyRequest(self)

	def consumeFood(self, howMuchFood):
		"""
		Go through the IngrChunks and 'eat' the oldest food.
		This method is not called if we have 0 IngrChunks (I hope)

		Returns:
			- (howMuchWeServed, totalFreshness)
		"""
		print "%s CONSUMING FOOD: %f" % (self.restaurant.name, howMuchFood)

		origHowMuchFood = howMuchFood
		totalFreshness = 0
		while howMuchFood > 0 and len(self.ingrChunks) > 0:
			sortedList = sorted(self.ingrChunks, key=lambda ic: ic.hourCreated)
			currChunk = sortedList[0]

			if currChunk.weight > howMuchFood:  # current chunk has more than we need
				currChunk.weight -= howMuchFood
				totalFreshness += howMuchFood * currChunk.getCurrentFreshness(self.currentHour)
				howMuchFood = 0
				break
			else:  # current chunk has less than we need, so eat it all and keep going...
				howMuchFood -= currChunk.weight
				totalFreshness += currChunk.weight * currChunk.getCurrentFreshness(self.currentHour)
				self.ingrChunks.remove(currChunk)

		howMuchWeServed = origHowMuchFood - howMuchFood
		
		return (howMuchWeServed, totalFreshness)

	def display(self):
		print "Item: %s -- Amount: %f" % (self.name, self.getWeight())

	def getWeight(self):
		sum = 0
		for ic in self.ingrChunks:
			sum += ic.weight
		return sum

	def throwAwayOldFood(self):
		for ic in self.ingrChunks:
			if (self.currentHour - ic.hourCreated) > self.expirationTime:
				self.amountOfWastedFood += ic.weight
				self.ingrChunks.remove(ic)

	def getCheapestIngrChunk(self, currHour, br_amount):
		"""
		Returns cheapest price and amount of that value
		"""
		if self.willingToSell:
			if (self.getWeight() - br_amount) > self.sellWeight:
				sortedList = sorted(self.ingrChunks, key=lambda ic: ic.hourCreated, reverse=True)
				currChunk = sortedList[0]

				return currChunk

		return None

	def preferredPurchaseAmount(self):
		return self.avgPoundsConsumedPerHour * 24 - self.getWeight()

	def costToBuyThatMuch(self, howMuch, currHour):
		"""
		Calculate and return the cost to buy 'howMuch' food
		"""
		# TODO should this reverse be false? wtff
		sortedIngrChunks = sorted(self.ingrChunks, key=lambda ic: ic.hourCreated, reverse=False)
		howMuchMoreFood = howMuch
		costSoFar = 0
		for chunk in sortedIngrChunks:
			if chunk.weight > howMuchMoreFood: # buy alot of it
				costSoFar += howMuchMoreFood * chunk.getCurrentPrice(currHour)
				return costSoFar
			else:
				costSoFar += chunk.weight * chunk.getCurrentPrice(currHour)
				howMuchMoreFood -= chunk.weight


class IngrChunk:
	def __init__(self, weight, hourCreated, ingr):
		self.weight = weight
		self.hourCreated = hourCreated
		self.ingr = ingr

	def getCurrentPrice(self, currHour):
		highPrice, lowPrice = base_ingredient_prices[self.ingr.name]

		currPrice = highPrice - ((highPrice - lowPrice) * ((currHour - self.hourCreated) / float(self.ingr.expirationTime)))
		return currPrice

	def getCurrentFreshness(self, currHour):
		currFreshness = 1 - ((currHour - self.hourCreated) / float(self.ingr.expirationTime))
		return currFreshness

	def subtractWeight(self, amountToSubtract):
		# Called by market.makeATransaction to remove a record if we use all the ingredient
		self.weight -= amountToSubtract
		if self.weight <= .05: # fudge factor
			self.ingr.ingrChunks.remove(self)
