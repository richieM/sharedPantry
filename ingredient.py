"""
TODO
	- need to add preferredSellWeight?
"""

import random

PLACE_BUY_REQUEST = "PLACE_BUY_REQUEST"
PLACE_SELL_REQUEST = "PLACE_SELL_REQUEST"

# ingredient id -> ingredient name
# TODO not used right now, but maybe later
ingredients = {0: "lemon",
			   1: "apple",
			   2: "rice"}

class Ingredient:
	"""
	Ingredients that a restaurant has that they can buy or sell.
	Each ingredient at a restaurant has it's own unique instance
	"""
	def __init__(self, name=0, willingToSell=False, willingToBuy=False, buyWeight=0, sellWeight=0, maxBuyPrice=0, minSellPrice=0, preferredPurchaseAmount=0, dollarsPerHourFromIngredient=10, avgPoundsConsumedPerHour=24.0/168.0, randomnessInDemand=.2):
		self.name = name
		self.weight = 0

		self.willingToSell = willingToSell
		self.willingToBuy = willingToBuy

		self.buyWeight = buyWeight
		self.maxBuyPrice = maxBuyPrice
		self.preferredPurchaseAmount = preferredPurchaseAmount

		self.sellWeight = sellWeight
		self.minSellPrice = minSellPrice

		self.dollarsPerHourFromIngredient = dollarsPerHourFromIngredient
		self.avgPoundsConsumedPerHour = avgPoundsConsumedPerHour
		self.randomnessInDemand = randomnessInDemand

		self.revenueFromThisIngredient = 0
		self.moneySpentOnThisIngredient = 0

	def setRestockParams(self, restockEveryHours=24*7, restockOnHour=0, howMuchToRestockPounds=50):
		self.restockEveryHours = restockEveryHours
		self.restockOnHour = restockOnHour
		self.howMuchToRestockPounds = howMuchToRestockPounds

	def anHourPassed(self, hour):
		currDemandInPounds = self.avgPoundsConsumedPerHour * (1 + self.randomnessInDemand * random.random())
		if self.isItTimeToRestock(hour):
			self.restock()
	
		if self.weight >= 0:
			if currDemandInPounds > self.weight:
				self.revenueFromThisIngredient += currDemandInPounds * self.dollarsPerHourFromIngredient
				newWeight = self.weight - currDemandInPounds
				return self.updateWeight(newWeight)
			elif currDemandInPounds < self.weight and currDemandInPounds > 0:
				currDemandInPounds = self.weight
				self.revenueFromThisIngredient += currDemandInPounds * self.dollarsPerHourFromIngredient
				newWeight = 0
				return self.updateWeight(newWeight)

	def isItTimeToRestock(self, hour):
		if ((hour % self.restockEveryHours) - self.restockOnHour) == 0:
			return True
		else:
			return False

	def restock(self):
		self.weight = self.weight + self.howMuchToRestockPounds
		
	def updateWeight(self, newWeight):
		# Update weight, and maybe we wanna make a buy or sell request
		oldWeight = self.weight
		self.weight = newWeight

		if self.willingToBuy:
			if oldWeight > self.buyWeight and self.weight < self.buyWeight:
				return PLACE_BUY_REQUEST
		elif self.willingToSell:
			if oldWeight < self.sellWeight and self.weight > self.sellWeight:
				return PLACE_SELL_REQUEST

	def display(self):
		print "Item: %s -- Amount: %f" % (self.name, self.weight)
