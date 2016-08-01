import marketplace
import ingredient

class Restaurant:
	"""
	A Restaurant can buy and sell inventory!
	"""
	def __init__(self, name, money=0, market=None):
		self.name = name
		self.money = money
		self.market = market
		self.ingredients = {} # ingredient_name -> Ingredient

	def updateIngredientWeight(self, ingredientName, newWeight):
		ingred = self.ingredients[ingredientName]
		if not ingred:
			raise Exception("Ingredient %s doesn't exist, dudebro" % ingredientName)

		resp = ingred.updateWeight(newWeight)
		if resp == ingredient.PLACE_BUY_REQUEST:
			self.placeBuyRequest(ingred)
		elif resp == ingredient.PLACE_SELL_REQUEST:
			self.placeSellRequest(ingred)

	def placeSellRequest(self, ingr):
		# gather all the info the market needs for this sell request
		# do remember that the market has some info on the seller already stored
		self.market.receiveSellRequest(self, ingr.name, amount=(ingr.weight - ingr.sellWeight), minPrice=ingr.minSellPrice)

	def placeBuyRequest(self, ingr):
		# gather all the info the market needs for this buy request
		# do remember that the market has some info on the seller already stored
		self.market.receiveBuyRequest(self, ingr.name, amount=ingr.preferredPurchaseAmount, maxPrice=ingr.maxBuyPrice)

