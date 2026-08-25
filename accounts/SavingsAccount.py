from datetime import datetime
from accounts.Account import Account
class SavingsAccount(Account):

    def __init__(self, balance=0, saving_period=1, interest_rate=0.02, minimum_balance=2000):
        super().__init__("Savings", balance)
        self._interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.start_timer = None
        self.saving_period = saving_period #Saving time in minutes

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.start_timer = datetime.now()
            return True
        return False
    
    def withdraw(self, amount):
        dif = datetime.now() - self.start_timer
        if dif.minutes > self.saving_period:
            return False
        if self._balance - amount < self.minimum_balance:
            return False
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest
        return interest
    