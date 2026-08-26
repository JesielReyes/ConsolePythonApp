from project1.models.user import User
from project1.models.CheckingAccount import CheckingAccount
from project1.models.SavingsAccount import SavingsAccount


class Customer(User):
    def __init__(self, pin, owner_id=None):
        super().__init__(pin, owner_id)

        self._accounts = {
            "Checking": {},
            "Savings": {}
        }

    def get_role(self):
        return "Customer"

    def create_account(self, pin, account_type, balance=0):
        if not self.check_pin(pin):
            raise ValueError("Invalid PIN")

        if account_type == "Checking":
            account = CheckingAccount(
                balance,
                self._owner_id
            )

        elif account_type == "Savings":
            account = SavingsAccount(
                balance,
                self._owner_id
            )

        else:
            raise ValueError("Invalid account type")

        account_number = account.get_account_number()

        self._accounts[account_type][account_number] = account

        return account

    def get_accounts(self, pin):
        if not self.check_pin(pin):
            raise ValueError("Invalid PIN")

        return self._accounts