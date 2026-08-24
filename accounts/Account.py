import random
class Account:
    def __init__(self, account_type, balance=0):
        self._balance = balance
        self._account_type = account_type
        self._interest_rate = 0.01  # Default interest rate
        self._account_number = random.randint(10000000, 99999999)


    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self):
        return self._balance
    
    def get_account_number(self):
        return self._account_number