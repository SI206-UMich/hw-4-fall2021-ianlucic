# Your name: Ian Lucic
# Your student id: 6721 2860
# Your email: ianlucic@umich.edu
# List who you have worked with on this homework: Umang Bhojani

import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)
        pass

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    
    def __init__(self, name, inventory, earnings = 0 , cost = 7):
        self.name = name
        self.inventory = inventory
        self.earnings = earnings
        self.cost = cost

    def process_order(self, name, quantity):
        if self.has_item(name, quantity):
            self.inventory[name] = self.inventory[name] - quantity
            self.earnings = self.cost * quantity
        else:
            print("Sorry we are all out!")

    def has_item(self, food_name, quantity):
        if food_name in self.inventory.keys():
            if self.inventory[food_name] >= quantity:
                return True
            else:
                return False
        else:
            return False

    def stock_up(self, food_name, quantity):
        if food_name in self.inventory.keys():
            self.inventory[food_name] = self.inventory[food_name] + quantity
        else: 
            self.inventory[food_name] = quantity #Changed from = to +

    def compute_cost(self, quantity):
        return quantity * self.cost

    def __str__(self):
        menu_key = self.inventory,keys()
        return ("Hello, we are " + self.name + ". This is the current menu " + str(self.inventory.keys()) + ". We charge $" + str(self.cost) + " per item. We have $" + str(self.earnings) + "in total.")



class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.f3 = Customer("Rob", 14)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertFalse(self.s1.has_item("Milkshake", 10))
        
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(self.s1.has_item("Burger", 70))

        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s1.has_item("Burger", 5))
        pass

	# Test validate order
    def test_validate_order(self):
        intialwallet = self.f3.wallet
		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.f3.validate_order(self.c1, self.s1, "Burger", 3)
        self.assertEqual(intialwallet, self.f3.wallet) 
		# case 2: test if the stall doesn't have enough food left in stock
        self.f3.validate_order(self.c1, self.s1, "Burger", 200)
        self.assertEqual(intialwallet, self.f3.wallet)
		# case 3: check if the cashier can order item from that stall
        self.f3.validate_order(self.c1, self.s1, "Burger", 1)
        self.assertEqual(self.f3.wallet, 4)


    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        wallet = self.f1.wallet
        self.f1.reload_money(20)
        self.assertEqual(wallet + 20, self.f1.wallet)
    
### Write main function
def main():
    inventory_american = { "Burger": 35, "Mac and Cheese": 10, "Tomato Soup": 25}
    inventory_british = {"Jammy Dodger": 50, "Tea": 15, "Scones": 10}
    
    f1 = Customer("Mary", 30)
    f2 = Customer("Bob", 60)
    f3 = Customer("Jane", 10)
    
    s1 = Stall("Terry's Turf Club", inventory_american, cost = 5)
    s2 = Stall("Queen Elizabeth's Bakery", inventory_british, cost = 8)

    c1 = Cashier("South", [s1])
    c2 = Cashier("North", [s2])

    f1.validate_order(c1, s2, "Tea", 15)
    f2.validate_order(c2, s1, "Burger", 40)
    f3.validate_order(c1, s2, "Scones", 5)

    f1.validate_order(c1, s1,"Burger", 40)
    f2.validate_order(c1, s1,"Tomato Soup", 30)
    f3.validate_order(c2, s2,"Tea", 20)

    f1.validate_order(c1, s1, "Burger", 10)
    f2.validate_order(c2, s2, "Scones", 10)
    f3.validate_order(c2, s2, "Jammy Dodger", 2)

    f1.validate_order(c1, s1, "Burger", 2)
    f2.validate_order(c1, s1, "Mac and Cheese", 2)
    f3.validate_order(c2, s2, "Scones", 1)


if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
