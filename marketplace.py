"""
TODO:


Pricing Models:
- dynamic but trivial: find middle ground between buyer and seller
- static: set by supermarkets / Instacart / doesnt fluctuate
- dynamic based on supply and demand
- Dutch auction -- starts high and lowers as time goes on

Matching Models:
- item
- time
- proximity
- price
- preferred vendors

Liquidity:
- Test: When do we order more from supplier?
- Test: Is it acceptable to not be able to fill a demand?

Delivery:
- sunk cost...
- dont include it now

Goals of the market:
Metrics for the restaurants
- Saving money for restaurants --- I'll have to simulate out them buying food from vertical, wasting some of it, and then sporadically buying extra supply from Whole Foods when they run out
- Time saved?
- Extra freshness -- but how do you meausure that quanitatively?
- delivery cost
- For each restaurant:
 	- $$Revenue$$ -- you paid This / you usually pay THISSSS
 	- Stress -- Running out incidents of running out (low stock incidents) -- amount of time when you can't feed demand
 	- Waste -- how much waste
 	- Freshness / Food Quality -- based on freshness  Average Freshness of ingredients (in days...)

TODO:
- ingredients turning into revenue through time so that the values drop (in)consistently
	- each restaurant has a different rate at which they churn thru stuff
	- larger randomness value for larger restaurants
- each restaurant gets a dump of item 1x a week probably...
- delay in delivery...

Experiment
7 restaurants, 1 ingredient, 1 shipment each week

Pretty much all the metrics are at the Ingredient level, so just keep it there, and roll it up later.

Profit -- revenue += ingr.profit
Stress -- hoursWithoutIngredients += ingr.hoursWithoutIngredient
Waste -- amountOfWastedFood += ingr.amountOfWastedFood
Freshness -- totalFreshness += ingr.totalFreshness; avgFreshness = totalFreshness / totalFoodConsumed
	Total Food Consumed -- totalFoodConsumed += ingr.totalFoodConsumed

market
	restaurant
		ingredient
			ingr.profit
			ingr.hoursWithoutIngredient
			ingr.amountOfWastedFood
			ingr.totalFreshness
			ingr.totalFoodConsumed
"""


import restaurant
import random
import ingredient

class Marketplace:
	"""
	MarketPlace where restaurants can buy and sell stuff!

	Seller posts a Sell Request
	Buyer posts a Buy Request
	"""
	def __init__(self, bulkResupplySize, control=False):
		self.restaurants = {} # name -> Restaurant
		self.buyRequests = []
		self.sellRequests = []
		self.purchaseRecords = []
		self.currentHour = -1
		self.control = control

		self.bulkResupplySize = bulkResupplySize

	def anHourPassed(self, hour):
		self.currentHour = hour
		print "==================================================================="
		print "HOUR %d" % self.currentHour
		print "==================================================================="

		self.restockIfNecessary()

		for r in self.restaurants.values():
			r.anHourPassed(self.currentHour)
			if (self.currentHour % 1) == 0:
				r.display()
		self.matchBuyersAndSellers()

	def receiveSellRequest(self, restaurant, ingredient):
		print "** ADDING SELLER REQUEST -- %s wants to sell %s" % (restaurant.name,ingredient.name)
		print
		sellRequest = SellRequest(restaurant, ingredient)
		self.sellRequests.append(sellRequest)

	def receiveBuyRequest(self, restaurant, ingredient):
		print "** BUY REQUEST RECEIVED -- %s wants to buy %d lbs of %s" % (restaurant.name, ingredient.preferredPurchaseAmount(), ingredient.name)
		print
		for br in self.buyRequests:
			if br.restaurant == restaurant:
				return

		buyRequest = BuyRequest(restaurant, ingredient, self.currentHour)
		self.buyRequests.append(buyRequest)

	def matchBuyersAndSellers(self):
		"""
		Matching buyers n sellerz, ya'll

		Version 3.0
		-- first try to find seller with all your ingredient at lowest price
		- else, try to find highest amount
		"""
		# shuffle buyRequests for fairness
		random.shuffle(self.buyRequests)
		buyRequestsThatWillStay = [] # Delete fulfilled buy requests...

		for br in self.buyRequests:
			myPreferredSellRequest, howMuchFood, cost = self.getPreferredSellRequest(br)
			if myPreferredSellRequest is not None:
				amountsOfGoodsTransacted = self.makeATransaction(myPreferredSellRequest, howMuchFood, cost, br)
				br.ingredient.sellWeight += amountsOfGoodsTransacted
				print "ADDING sell weight due to transaction by %f" % amountsOfGoodsTransacted
			else:
				if howMuchFood == "NO_MATCH":
					buyRequestsThatWillStay.append(br)

		self.buyRequests = buyRequestsThatWillStay

	def getPreferredSellRequest(self, br):
		"""
		Finds a preferred seller, by
		- 1. Amount
		- 2. Price

		Returns (sellRequest, howMuchFood, cost)
		"""
		howMuchFoodToBuy = br.ingredient.preferredPurchaseAmount()

		if howMuchFoodToBuy <= .1:
			return (None, "NO_NEED", None)

		preferredSellerWithEnough = None
		preferredSellerWithEnoughCost = 0

		preferredSellerNotEnough = None
		preferredSellNotEnoughHowMuchWilling = 0
		preferredSellerNotEnoughCost = 0

		for sr in self.sellRequests:
			howMuchWillingToSell = sr.ingredient.getWeight() - sr.ingredient.sellWeight
			if (howMuchWillingToSell < 1):
				continue

			# They have enough...
			if howMuchWillingToSell > howMuchFoodToBuy:
				costToBuyThatMuch = sr.ingredient.costToBuyThatMuch(howMuchFoodToBuy, self.currentHour)
				if preferredSellerWithEnough is None: # first time thru
					preferredSellerWithEnough = sr
					preferredSellerWithEnoughCost = costToBuyThatMuch
				else: # who's better on price?
					if costToBuyThatMuch < preferredSellerWithEnoughCost:
						preferredSellerWithEnough = sr
						preferredSellerWithEnoughCost = costToBuyThatMuch
			else:
				# They have some amount
				costToBuyThatMuch = sr.ingredient.costToBuyThatMuch(howMuchWillingToSell, self.currentHour)
				if preferredSellerNotEnough is None: # first time thru
					preferredSellerNotEnough = sr
					preferredSellNotEnoughHowMuchWilling = howMuchWillingToSell
					preferredSellerNotEnoughCost = costToBuyThatMuch
				else: # who's better on price?
					if howMuchWillingToSell > preferredSellNotEnoughHowMuchWilling:
						preferredSellerNotEnough = sr
						preferredSellNotEnoughHowMuchWilling = howMuchWillingToSell
						preferredSellerNotEnoughCost = costToBuyThatMuch

		if preferredSellerWithEnough:
			return (preferredSellerWithEnough, howMuchFoodToBuy, preferredSellerWithEnoughCost)
		elif preferredSellerNotEnough:
			return (preferredSellerNotEnough, preferredSellNotEnoughHowMuchWilling, preferredSellerNotEnoughCost)
		else:
			return (None, "NO_MATCH", None)


	def getCheapestIngrChunk(self, br):
		# TODO delete this code
		sellRequestsWithIngredient = [sr for sr in self.sellRequests if sr.ingredient.name == br.ingredient.name and sr.restaurant.name != br.restaurant.name]

		currCheapestIngrChunk = None
		for sr in sellRequestsWithIngredient:
			currIngrChunk = sr.ingredient.getCheapestIngrChunk(self.currentHour, br.ingredient.preferredPurchaseAmount())
			if currIngrChunk is None:
				continue
			if currCheapestIngrChunk is None:
				currCheapestIngrChunk = currIngrChunk
			else:
				if currIngrChunk.getCurrentPrice(self.currentHour) < currCheapestIngrChunk.getCurrentPrice(self.currentHour):
					currCheapestIngrChunk = currIngrChunk

		return currCheapestIngrChunk


	def makeATransaction(self, sellReq, amountOfGoods, totalPrice, buyReq):
		buyerIngr = buyReq.ingredient
		sellerIngr = sellReq.ingredient

		print " ** Transaction occuring **"
		print "Buyer: %s   -- Seller: %s" % (buyReq.restaurant.name, sellerIngr.restaurant.name)
		print "Amount of goods: %f -- Total price: $ %f" % (amountOfGoods, totalPrice)
		print

		## Transact Money
		deliveryCost = 2.5 + 0.1 * amountOfGoods
		buyerIngr.profit -= totalPrice
		buyerIngr.profit -= deliveryCost
		sellerIngr.profit += totalPrice

		## Transact Goods
		howMuchGoodsSoFar = 0
		sortedChunks = sorted(sellerIngr.ingrChunks, key=lambda ic: ic.hourCreated)
		#import pdb; pdb.set_trace()
		for chunk in sortedChunks:
			howMuchIWant = amountOfGoods - howMuchGoodsSoFar

			if chunk.weight >= howMuchIWant:
				howMuchToTransact = howMuchIWant
			else:
				howMuchToTransact = chunk.weight

			chunk.subtractWeight(howMuchToTransact)
			newBuyerChunk = ingredient.IngrChunk(weight=howMuchToTransact, hourCreated=chunk.hourCreated, ingr=buyerIngr)
			buyerIngr.ingrChunks.append(newBuyerChunk)
			howMuchGoodsSoFar += howMuchToTransact

			if howMuchGoodsSoFar >= amountOfGoods:
				break

		#return amount of goods transacted
		return howMuchGoodsSoFar

	def calculateHowMuchToTransact(self, sellReq, buyReq):
		howMuchToBuy = buyReq.ingredient.preferredPurchaseAmount()
		howMuchWillingToSell = sellReq.ingredient.getWeight() - sellReq.ingredient.sellWeight

		if ingrChunk.weight >= howMuchToBuy:
			return howMuchToBuy
		else:
			return ingrChunk.weight

	def calculatePriceForTransaction(self, ingrChunk, buyReq):
		return ingrChunk.getCurrentPrice(self.currentHour)

	def gatherSimData(self):
		self.simData = {}
		self.simData["market"] = {}
		for r in self.restaurants.values():
			currRestData = {}
			for ingr in r.ingredients.values():
				currIngrData = ingr.getSimData()
				currRestData[ingr.name] = currIngrData
			self.simData["market"][r.name] = currRestData

		return self.simData

	def restockIfNecessary(self):
		"""
		Restock one of the bigger restaurants if a buy Request hasn't been satisfied
		in like 2 hours...
		"""

		if self.control:
			hoursInAWeek = 168
			if self.currentHour % hoursInAWeek == 0:
				for r in self.restaurants.values():
					for i in r.ingredients.values():
						howMuchFood = i.avgPoundsConsumedPerHour * hoursInAWeek
						i.restockFood(howMuchFood, control=self.control)
		else:
			if self.currentHour == 0:  # introduce some food off the bat...
				self.restockABigSupplier();
			else:
				for br in self.buyRequests:
					if self.currentHour > br.hourCreated:
						self.restockABigSupplier();
						return


	def calcHowMuchFoodToRestock(self):

		foodShouldLastHowManyHours = 24;
		totalFoodPerHourNeeded = 0

		for r in self.restaurants.values():
			for i in r.ingredients.values():
				totalFoodPerHourNeeded += i.avgPoundsConsumedPerHour


		totalFoodNeeded = int(totalFoodPerHourNeeded * foodShouldLastHowManyHours)

		howManyChunksToOrder = int((totalFoodNeeded / self.bulkResupplySize) + 1)

		howMuchFood = howManyChunksToOrder * self.bulkResupplySize

		return howMuchFood


	def restockABigSupplier(self):
		"""
		Gather closely children, the time to restock is upon us.


		- Determine how much we wanna order
		- Dump that food on the next large restaurant...
		"""
		howMuchFoodToOrder = self.calcHowMuchFoodToRestock()

		print "********** REORDERING FOOD %d lbs" % howMuchFoodToOrder

		restaurantToRestock = None
		for currRest in self.restaurants.values():
			if currRest.restockable:
				if not restaurantToRestock:
					restaurantToRestock = currRest
				else:
					if currRest.lastRestockTime < restaurantToRestock.lastRestockTime:
						restaurantToRestock = currRest

		for i in restaurantToRestock.ingredients.values():
			i.restockFood(howMuchFoodToOrder, control=self.control)
			restaurantToRestock.lastRestockTime = self.currentHour
			i.sellWeight = i.avgPoundsConsumedPerHour * 12
			print "RESETTING sell weight to %f" % i.sellWeight

class BuyRequest:
	def __init__(self, restaurant, ingredient, hourCreated):
		self.restaurant = restaurant
		self.ingredient = ingredient
		self.maxPrice = ingredient.maxBuyPrice
		self.hourCreated = hourCreated
		# TODO other stuff here, like preferred sellers or something...


class SellRequest:
	def __init__(self, restaurant, ingredient):
		self.restaurant = restaurant
		self.ingredient = ingredient
		# TODO other stuff here, like preferred buyers or something...

	def amountAvailable(self):
		return self.ingredient.weight - self.ingredient.sellWeight
