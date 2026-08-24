#Points System
from accounts.Account import Account
class CreditAccount(Account):
    def __init__(self, credit_limit=10000, interest=0.35, minimum_payment=0.1):
        super().__init__("Credit", 0)
        self.credit_limit = credit_limit
        self._interest_rate = interest
        self.minimum_payment = minimum_payment
        self.points = 0

    def withdraw(self, amount):
        if amount <= self.credit_limit:
            self.credit_limit -= amount
            self._balance += amount
            self.points += amount * 0.03
            return True
        else:
            return False

    def deposit(self, amount):
        if amount < self._balance * self.minimum_payment:
            return False
        self._balance -= amount
        self.credit_limit += amount
        return True

    def get_balance(self):
        return self._balance

    def get_credit_limit(self):
        return self.credit_limit
    
    def request_credit_increase(self, amount):
        self.credit_limit += amount
        return True
    
    def get_points(self):
        return self.points
    
    def redeem_points(self, points):
        if points <= self.points:
            self.points -= points
            self._balance -= points * 0.01
            self.credit_limit += points * 0.01
            return True
        else:
            return False