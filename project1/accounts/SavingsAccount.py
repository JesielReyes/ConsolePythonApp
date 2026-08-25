from accounts.account import Account


class SavingsAccount(Account):

    def __init__(self, balance=0, owner_id=None, saving_period=1, interest_rate=0.02, minimum_balance=2000):
        super().__init__("Savings", balance, owner_id)
        self._interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.saving_period = saving_period #Saving time in minutes

    def deposit(self, amount):
        return super().deposit(amount)
    
    def withdraw(self, amount):
        return super().withdraw(amount)

    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest
        return interest
    
