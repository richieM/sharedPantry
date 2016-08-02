"""
Open Questions
- How much knowledge of the ingredients and restaurants should the Market have?
	Maybe the market knows nothing about the ingredients and restaurants, and it just gets buy and sell requests in...
- Should the wallet info be stored here on the market side? Probably...
	But then it like debits the payment on the seller side?
- How do we do security? how does the market know that it's actually a certain restaurant that is making a buy or sell request??
    This influences how I store restaurants here, whether it's by name or ingredient or private public key pair or whatever

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
 	- $$ -- you paid This / you usually pay THISSSS
 	- Stress -- Running out incidents of running out (low stock incidents)
 	- Waste -- how much waste
 	- Food Quality -- based on freshness  Average Freshness of ingredients (in days...)

TODO:
- ingredients turning into revenue through time so that the values drop (in)consistently
	- each restaurant has a different rate at which they churn thru stuff
	- larger randomness value for larger restaurants
- each restaurant gets a dump of item 1x a week probably...
- delay in delivery...

Experiment 
7 restaurants, 1 ingredient, 1 shipment each week

"""


import restaurant

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

	def anHourPassed(self, hour):
		for r in self.restaurants:
			r.anHourPassed()

	def receiveSellRequest(self, restaurant, ingredient, amount, minPrice):
		print "Sell request received"
		sellRequest = SellRequest(restaurant, ingredient, amount, minPrice)
		self.sellRequests.append(sellRequest)

		#self.matchBuyersAndSellers()

	def receiveBuyRequest(self, restaurant, ingredient, amount, maxPrice):
		print "Buy request received"
		buyRequest = BuyRequest(restaurant, ingredient, amount, maxPrice)
		self.buyRequests.append(buyRequest)

		#self.matchBuyersAndSellers()

	def matchBuyersAndSellers(self):
		"""
		Matching buyers n sellerz, ya'll

		Version 1.0, transactions are trivial.  Simply loop over each buy request and see if there is a sell request to match.  Then make it rain...
		"""
		for br in self.buyRequests:
			matchingSellReqs = [sr for sr in self.sellRequests if sr.ingredientName == br.ingredientName and sr.minPrice < br.maxPrice]
			for sr in matchingSellReqs:
				self.makeATransaction(sr, br)
				if br.amountFulfilled <= 0:
					self.buyRequests.remove(br)
					break

	def makeATransaction(self, sellReq, buyReq):
		buyerIngr = buyReq.ingredient
		sellerIngr = sellReq.ingredient

		amountOfGoods = self.calculateHowMuchToTransact(sellReq, buyReq)
		pricePerUnit = self.calculatePriceForTransaction(sellReq, buyReq)
		totalPrice = pricePerUnit * amountOfGoods

		print " ** Transaction occuring **"
		print "Buyer: %s   -- Seller: %s" % (buyReq.restaurant.name, sellReq.restaurant.name)
		print "Amount of goods: %f -- Price per unit: %f -- Total price: $ %f" % (amountOfGoods, pricePerUnit, totalPrice)
		escrowMoney = 0
		escrowGoods = 0


		##### Put money and goods in escrow, simulating delivery pickup
		# Pull funds from buyer
		buyerIngr.moneySpentOnThisIngredient -= totalPrice
		escrowMoney = totalPrice
		# Pull goods from seller
		sellerIngr.weight -= amountOfGoods
		escrowGoods = amountOfGoods


		##### Deliver money and goods to appropriate parties, simulating delivery complete
		# Deliver goods to buyer
		buyerIngr.weight += amountOfGoods
		escrowGoods = 0
		# Deliver funds to seller
		sellerIngr.moneySpentOnThisIngredient += totalPrice
		escrowMoney = 0


		###### Transaction complete, update the BuyRequest and SellRequest
		sellReq.amountAvailable -= amountOfGoods
		buyReq.amountFulfilled = amountOfGoods


		# Remove buy and sell requests if they're fulfilled
		if sellReq.amountAvailable <= 0:
			self.sellRequests.remove(sellReq)

		if buyReq.amountFulfilled == buyReq.preferredPurchaseAmount:
			self.buyRequests.remove(buyReq)
		

	def calculateHowMuchToTransact(self, sellReq, buyReq):
		howMuchToBuy = buyReq.preferredPurchaseAmount - buyReq.amountFulfilled

		if sellReq.amountAvailable >= howMuchToBuy:
			return howMuchToBuy
		else:
			return sellReq.amountAvailable

	def calculatePriceForTransaction(self, sellReq, buyReq):
		# first pass -- price is set by finding the middle between min and max prices.
		price = sellReq.minPrice + (buyReq.maxPrice - sellReq.minPrice) / 2
		return price


class BuyRequest:
	def __init__(self, restaurant, ingredient, amount, maxPrice):
		self.restaurant = restaurant
		self.ingredient = ingredient
		self.preferredPurchaseAmount = amount
		self.amountFulfilled = 0
		self.maxPrice = maxPrice
		# TODO other stuff here, like preferred sellers or something...


# TODO amountAvailable should be dynamicly calculated, maybe, because the value could change...
class SellRequest:
	def __init__(self, restaurant, ingredient, amount, minPrice):
		self.restaurant = restaurant
		self.ingredient = ingredient
		self.amountAvailable = amount
		self.minPrice = minPrice
		# TODO other stuff here, like preferred buyers or something...