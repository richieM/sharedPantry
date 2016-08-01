"""
TODO
	- need to add preferredSellWeight?
"""

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
	def __init__(self, name=0, willingToSell=False, willingToBuy=False, buyWeight=0, sellWeight=0, maxBuyPrice=0, minSellPrice=0, preferredPurchaseAmount=0):
		self.name = name
		self.weight = 0

		self.willingToSell = willingToSell
		self.willingToBuy = willingToBuy

		self.buyWeight = buyWeight
		self.maxBuyPrice = maxBuyPrice
		self.preferredPurchaseAmount = preferredPurchaseAmount

		self.sellWeight = sellWeight
		self.minSellPrice = minSellPrice
		

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