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

Revenue -- revenue += ingr.profit
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
	def __init__(self):
		self.restaurants = {} # name -> Restaurant
		self.buyRequests = []
		self.sellRequests = []
		self.purchaseRecords = []
		self.currentHour = -1

	def anHourPassed(self, hour):
		self.currentHour = hour
		print "HOUR %d" % self.currentHour
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
		print "** BUY REQUEST RECEIVED -- %s wants to buy %d lbs of %s" % (restaurant.name, ingredient.preferredPurchaseAmount, ingredient.name)
		print
		buyRequest = BuyRequest(restaurant, ingredient)
		self.buyRequests.append(buyRequest)

	def matchBuyersAndSellers(self):
		"""
		Matching buyers n sellerz, ya'll

		Version 2.0:
		Find the cheapest possible ingredient.
		Loop over all the SellRequests and get a IngrChunk from each if possible...
		"""
		random.shuffle(self.buyRequests) # shuffle buyRequests for fairness

		for br in self.buyRequests:
			while (br.preferredPurchaseAmount - br.amountFulfilled) > .05:
				cheapestIngrChunk = self.getCheapestIngrChunk(br)
				if cheapestIngrChunk is not None:
					self.makeATransaction(cheapestIngrChunk, br)
				else:
					break

		for br in self.buyRequests:
			if (br.preferredPurchaseAmount - br.amountFulfilled) <= .05:
				self.buyRequests.remove(br)

	def getCheapestIngrChunk(self, br):
		sellRequestsWithIngredient = [sr for sr in self.sellRequests if sr.ingredient.name == br.ingredient.name and sr.restaurant.name != br.restaurant.name]

		currCheapestIngrChunk = None
		for sr in sellRequestsWithIngredient:
			currIngrChunk = sr.ingredient.getCheapestIngrChunk(self.currentHour, br.preferredPurchaseAmount)
			if currIngrChunk is None:
				continue
			if currCheapestIngrChunk is None:
				currCheapestIngrChunk = currIngrChunk
			else:
				if currIngrChunk.getCurrentPrice(self.currentHour) < currCheapestIngrChunk.getCurrentPrice(self.currentHour):
					currCheapestIngrChunk = currIngrChunk

		return currCheapestIngrChunk



	def makeATransaction(self, ingrChunk, buyReq):
		buyerIngr = buyReq.ingredient
		sellerIngr = ingrChunk.ingr

		amountOfGoods = self.calculateHowMuchToTransact(ingrChunk, buyReq)
		pricePerUnit = self.calculatePriceForTransaction(ingrChunk, buyReq)
		totalPrice = pricePerUnit * amountOfGoods

		print " ** Transaction occuring **"
		print "Buyer: %s   -- Seller: %s" % (buyReq.restaurant.name, sellerIngr.restaurant.name)
		print "Amount of goods: %f -- Price per unit: %f -- Total price: $ %f" % (amountOfGoods, pricePerUnit, totalPrice)
		print

		escrowMoney = 0
		escrowGoods = 0


		##### Put money and goods in escrow, simulating delivery pickup
		# Pull funds from buyer
		buyerIngr.profit -= totalPrice
		escrowMoney = totalPrice
		# Pull goods from seller
		ingrChunk.weight -= amountOfGoods
		escrowGoods = amountOfGoods


		##### Deliver money and goods to appropriate parties, simulating delivery complete
		# Deliver goods to buyer
		newChunk = ingredient.IngrChunk(weight=amountOfGoods, hourCreated=ingrChunk.hourCreated, ingr=buyerIngr)
		buyerIngr.ingrChunks.append(newChunk)
		escrowGoods = 0
		# Deliver funds to seller
		sellerIngr.profit += totalPrice
		escrowMoney = 0


		###### Transaction complete, update the BuyRequest and SellRequest
		buyReq.amountFulfilled += amountOfGoods

		# Remove ingrChunk if it's spent
		if ingrChunk.weight < .01:
			ingrChunk.ingr.ingrChunks.remove(ingrChunk)

	def calculateHowMuchToTransact(self, ingrChunk, buyReq):
		howMuchToBuy = buyReq.preferredPurchaseAmount - buyReq.amountFulfilled

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

class BuyRequest:
	def __init__(self, restaurant, ingredient):
		self.restaurant = restaurant
		self.ingredient = ingredient
		self.preferredPurchaseAmount = ingredient.preferredPurchaseAmount
		self.amountFulfilled = 0
		self.maxPrice = ingredient.maxBuyPrice
		# TODO other stuff here, like preferred sellers or something...


class SellRequest:
	def __init__(self, restaurant, ingredient):
		self.restaurant = restaurant
		self.ingredient = ingredient
		# TODO other stuff here, like preferred buyers or something...

	def amountAvailable(self):
		return self.ingredient.weight - self.ingredient.sellWeight