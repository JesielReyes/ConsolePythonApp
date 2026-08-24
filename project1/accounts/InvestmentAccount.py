from accounts.Account import Account
import random
class InvestmentAccount(Account):
    def __init__(self, risk_level="Low", balance=0, interest_rate=0.075):
        super().__init__("Investment", balance)
        self._interest_rate = interest_rate
        self.minimum_balance = 1000
        self.available_cash = 0
        self.risk_level = self.set_risk_level(risk_level)

    def withdraw(self, amount):
        if self._balance - amount < self.minimum_balance:
            return False
        self._balance -= amount
        return True

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest
        return interest
    
    def set_risk_level(self, risk_level):
        self.risk_level = risk_level
        if risk_level == "High":
            self._interest_rate = random.uniform(-1, 1)
        elif risk_level == "Medium":
            self._interest_rate = random.uniform(-0.5, 0.5)
        else:
            self._interest_rate = random.uniform(-0.1, 0.1)