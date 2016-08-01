"""
Open Questions
- How much knowledge of the ingredients and restaurants should the Market have?
	Maybe the market knows nothing about the ingredients and restaurants, and it just gets buy and sell requests in...
- Should the wallet info be stored here on the market side? Probably...
	But then it like debits the payment on the seller side?
- How do we do security? how does the market know that it's actually a certain restaurant that is making a buy or sell request??
    This influences how I store restaurants here, whether it's by name or ingredient or private public key pair or whatever
"""
from restaurant import Ingredient, Restaurant


class Market:
	"""
	MarketPlace where restaurants can buy and sell stuff!

	Seller posts a Sell Request
	Buyer posts a Buy Request
	"""
	def __init__(self):
		self.restaurants = {}
		self.buyRequests = []
		self.sellRequests = []
		self.purchaseRecords = []

	def receiveSellRequest(restaurant, ingredient, weight, minPrice):
		pass

	def receiveBuyRequest(restaurant, ingredient, weight, maxPrice):
		pass









