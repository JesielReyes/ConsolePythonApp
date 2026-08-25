from account.account import Account
class CheckingAccount(Account):
    def __init__(self, balance=0, owner_id=None):
        super().__init__("Checking", balance, owner_id)
        self.minimum_balance = 500
        self.overDraft_fee = 75

    def withdraw(self, amount):
        return super().withdraw(amount)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False