PLACE_BUY_REQUEST = "PLACE_BUY_REQUEST"
PLACE_SELL_REQUEST = "PLACE_SELL_REQUEST"

class Ingredient:
	"""
	Ingredients that a restaurant has that they can buy or sell.
	Each ingredient at a restaurant has it's own unique instance
	"""
	def __init__(self, name, id=0, weight=0, willingToSell=False, willingToBuy=False, buyWeight=0, sellWeightt=0, maxBuyPrice=0, minBuyPrice=0, preferredPurchaseAmount=0):
		self.name = name
		self.id = 0
		self.weight = 0

		self.willingToSell = willingToSell
		self.willingToBuy = willingToBuy

		self.buyWeight = buyWeight
		self.minBuyPrice = minBuyPrice
		self.preferredPurchaseAmount = preferredPurchaseAmount

		self.sellWeight = sellWeightt
		self.maxBuyPrice = maxBuyPrice
		

	def updateWeight(newWeight):
		# Update weight, and maybe we wanna make a buy or sell request
		oldWeight = self.weight
		self.weight = newWeight

		if self.willingToBuy:
			if oldWeight > self.buyWeight and self.weight < self.buyWeight:
				return PLACE_BUY_REQUEST
		elif self.willingToSell:
			if oldWeight < self.sellWeightt and self.weight > self.buyWeight:
				return PLACE_SELL_REQUEST

class Restaurant:
	"""
	A Restaurant can buy and sell inventory!
	"""
	def __init__(self, name, money=0, marketplace=None):
		self.name = name
		self.money = money
		self.marketplace = marketplace
		self.ingredients = {} # map of ingredient ids to ingredient instances

	def updateIngredientWeight(ingredient, newWeight):
		resp = ingredient.updateWeight(newWeight)
		if resp == PLACE_BUY_REQUEST:
			placeSellRequest(ingredient)
		elif resp == PLACE_SELL_REQUEST:
			placeBuyRequest(ingredient)

	def placeSellRequest(ingredient):
		# gather all the info the market needs for this sell request
		# do remember that the market has some info on the seller already stored
		marketplace.receiveSellRequest()

	def placeBuyRequest(ingredient):
		# gather all the info the market needs for this buy request
		# do remember that the market has some info on the seller already stored
		marketplace.receiveBuyRequest()

