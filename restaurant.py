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
		self.market.receiveSellRequest(self, ingr)

	def placeBuyRequest(self, ingr):
		self.market.receiveBuyRequest(self, ingr)

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
		amountOfWastedFood = 0
		hoursWithoutIngredients = 0
		totalFreshness = 0
		totalFoodConsumed = 0
		for ingr in self.ingredients.values():
			ingr.display()
			revenue += ingr.revenueFromThisIngredient
			revenue -= ingr.moneySpentOnThisIngredient
			amountOfWastedFood += ingr.amountOfWastedFood
			hoursWithoutIngredients += ingr.hoursWithoutIngredient
			totalFreshness += ingr.totalFreshness
			totalFoodConsumed += ingr.totalFoodConsumed
		
		if totalFoodConsumed == 0:
			avgFreshness = 0
		else:
			avgFreshness = totalFreshness / totalFoodConsumed

		print "Total revenue %f" % revenue
		print "Wasted Food %f" % amountOfWastedFood
		print "Hours without ingredients %f" % hoursWithoutIngredients
		print "avgFreshness %f" % avgFreshness
		print "totalFoodConsumed %f" % totalFoodConsumed
		print
		print




