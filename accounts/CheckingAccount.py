from accounts.Account import Account
class CheckingAccount(Account):
    def __init__(self, balance=0):
        super().__init__("Checking", balance)
        self.minimum_balance = 500
        self.overDraft_fee = 75

    def withdraw(self, amount):
        if self._balance - amount < self.minimum_balance:
            self._balance -= self.overDraft_fee
        self._balance -= amount
        return True

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False