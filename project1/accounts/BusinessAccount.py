from accounts.Account import Account
class BusinessAccount(Account):
    def __init__(self, balance=0, interest_rate=0.03, minimum_balance=10000, overDraft_fee=150):
        super().__init__("Business", balance)
        self._interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.overDraft_fee = overDraft_fee

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