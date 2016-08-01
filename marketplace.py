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

		#self.matchBuyersAndSellers()

	def receiveBuyRequest(self, restaurant, ingrName, amount, maxPrice):
		print "Buy request received"
		buyRequest = BuyRequest(restaurant, ingrName, amount, maxPrice)
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
		buyer = buyReq.restaurant
		seller = sellReq.restaurant
		itemName = buyReq.ingredientName

		amountOfGoods = self.calculateHowMuchToTransact(sellReq, buyReq)
		pricePerUnit = self.calculatePriceForTransaction(sellReq, buyReq)
		totalPrice = pricePerUnit * amountOfGoods

		if buyReq.restaurant.money >= totalPrice:
			escrowMoney = 0
			escrowGoods = 0


			##### Put money and goods in escrow, simulating delivery pickup
			# Pull funds from buyer
			buyer.money -= totalPrice
			escrowMoney = totalPrice
			# Pull goods from seller
			seller.ingredients[itemName].weight -= amountOfGoods
			escrowGoods = amountOfGoods


			##### Deliver money and goods to appropriate parties, simulating delivery complete
			# Deliver goods to buyer
			buyer.ingredients[itemName].weight += amountOfGoods
			escrowGoods = 0
			# Deliver funds to seller
			seller.money += totalPrice
			escrowMoney = 0


			###### Transaction complete, update the BuyRequest and SellRequest
			sellReq.amountAvailable -= amountOfGoods
			buyReq.amountFulfilled = amountOfGoods


			# Remove buy and sell requests if they're fulfilled
			if sellReq.amountAvailable <= 0:
				self.sellRequests.remove(sellReq)

			if buyReq.amountFulfilled == buyReq.preferredPurchaseAmount:
				self.buyRequests.remove(buyReq)
		else:
			print "ERROR: Restaurant %s doesn't have the funds %d to buy %s from %s" % (buyReq.restaurant.name, totalPrice, buyReq.ingredientName, sellReq.restaurant.name)


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
	def __init__(self, restaurant, ingredientName, amount, maxPrice):
		self.restaurant = restaurant
		self.ingredientName = ingredientName
		self.preferredPurchaseAmount = amount
		self.amountFulfilled = 0
		self.maxPrice = maxPrice
		# TODO other stuff here, like preferred sellers or something...


# TODO amountAvailable should be dynamicly calculated, maybe, because the value could change...
class SellRequest:
	def __init__(self, restaurant, ingredientName, amount, minPrice):
		self.restaurant = restaurant
		self.ingredientName = ingredientName
		self.amountAvailable = amount
		self.minPrice = minPrice
		# TODO other stuff here, like preferred buyers or something...