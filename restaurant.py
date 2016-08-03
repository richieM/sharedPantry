import marketplace
import ingredient

class Restaurant:
	"""
	A Restaurant can buy and sell inventory!
	"""
	def __init__(self, name, market=None):
		self.name = name
		self.market = market
		# TODO add location and do streetwalk distance...
		self.ingredients = {} # ingredient_name -> Ingredient

	def placeSellRequest(self, ingr):
		# gather all the info the market needs for this sell request
		# do remember that the market has some info on the seller already stored
		self.market.receiveSellRequest(self, ingr, minPrice=ingr.minSellPrice)

	def placeBuyRequest(self, ingr):
		# gather all the info the market needs for this buy request
		# do remember that the market has some info on the seller already stored
		self.market.receiveBuyRequest(self, ingr, amount=ingr.preferredPurchaseAmount, maxPrice=ingr.maxBuyPrice)

	def anHourPassed(self, hour):
		# An hour passed, so we'll have to ask each ingredient to change, as well as 
		# generate a flow up in revenue from the ingredients
		for currIngr in self.ingredients.values():
			resp = currIngr.anHourPassed(hour)

			if resp == ingredient.PLACE_BUY_REQUEST:
				self.placeBuyRequest(currIngr)
			elif resp == ingredient.PLACE_SELL_REQUEST:
				self.placeSellRequest(currIngr)


	def display(self):
		print self.name
		revenue = 0
		for ingr in self.ingredients.values():
			ingr.display()
			revenue += ingr.revenueFromThisIngredient
			revenue -= ingr.moneySpentOnThisIngredient
		print "Total revenue %f" % revenue
		print
		print




