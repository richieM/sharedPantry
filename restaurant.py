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

	def updateIngredientWeight(ingredient, newWeight):
		resp = ingredient.updateWeight(newWeight)
		if resp == PLACE_BUY_REQUEST:
			placeSellRequest(ingredient)
		elif resp == PLACE_SELL_REQUEST:
			placeBuyRequest(ingredient)

	def placeSellRequest(ingredient):
		# gather all the info the market needs for this sell request
		# do remember that the market has some info on the seller already stored
		market.receiveSellRequest()

	def placeBuyRequest(ingredient):
		# gather all the info the market needs for this buy request
		# do remember that the market has some info on the seller already stored
		market.receiveBuyRequest()

