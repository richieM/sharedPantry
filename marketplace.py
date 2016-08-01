"""
Open Questions
- How much knowledge of the ingredients and restaurants should the Market have?
	Maybe the market knows nothing about the ingredients and restaurants, and it just gets buy and sell requests in...
- Should the wallet info be stored here on the market side? Probably...
	But then it like debits the payment on the seller side?
- How do we do security? how does the market know that it's actually a certain restaurant that is making a buy or sell request??
    This influences how I store restaurants here, whether it's by name or ingredient or private public key pair or whatever
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

	def receiveSellRequest(self, restaurant, ingrName, amount, minPrice):
		print "Sell request received"
		sellRequest = SellRequest(restaurant, ingrName, amount, minPrice)
		self.sellRequests.append(sellRequest)

		self.transact()

	def receiveBuyRequest(self, restaurant, ingrName, amount, maxPrice):
		print "Buy request received"
		buyRequest = BuyRequest(restaurant, ingrName, amount, maxPrice)
		self.buyRequests.append(buyRequest)

		self.transact()

	def transact(self):
		# match buyers n sellers, ya'll
		pass

class BuyRequest:
	def __init__(self, restaurant, ingredientName, amount, maxPrice):
		self.restaurant = restaurant
		self.ingredientName = ingredientName
		self.preferredPurchaseAmount = amount
		self.maxPrice = maxPrice
		# TODO other stuff here, like preferred sellers or something...

class SellRequest:
	def __init__(self, restaurant, ingredientName, amount, minPrice):
		self.restaurant = restaurant
		self.ingredientName = ingredientName
		self.amountAvailable = amount
		self.minPrice = minPrice
		# TODO other stuff here, like preferred buyers or something...









