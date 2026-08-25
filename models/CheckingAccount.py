from models.Account import Account


class CheckingAccount(Account):

    def __init__(self, account_number, customer_id, balance=0):
        super().__init__(
            account_number,
            customer_id,
            balance
        )

    def deposit(self, amount):
        if amount <= 0:
            return False

        self._balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0:
            return False

        # Checking accounts allow overdraft
        self._balance -= amount
        return True