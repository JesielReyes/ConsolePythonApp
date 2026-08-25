from users.user import User
from account.CheckingAccount import CheckingAccount
from account.SavingsAccount import SavingsAccount


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

        return account_number

    def get_accounts(self, pin):
        if not self.check_pin(pin):
            raise ValueError("Invalid PIN")

        return self._accounts

    def get_account(
        self,
        pin,
        account_type,
        account_number
    ):
        if not self.check_pin(pin):
            raise ValueError("Invalid PIN")

        if account_type not in self._accounts:
            raise ValueError("Invalid account type")

        if account_number not in self._accounts[account_type]:
            raise ValueError("Account does not exist")

        return self._accounts[account_type][account_number]

    def deposit(
        self,
        pin,
        account_type,
        account_number,
        amount
    ):
        account = self.get_account(
            pin,
            account_type,
            account_number
        )

        if not account.deposit(amount):
            raise ValueError("Deposit failed")

        return True

    def withdraw(
        self,
        pin,
        account_type,
        account_number,
        amount
    ):
        account = self.get_account(
            pin,
            account_type,
            account_number
        )

        if not account.withdraw(amount):
            raise ValueError("Withdrawal failed")

        return True

    def transfer_funds(
        self,
        pin,
        from_account_type,
        from_account_number,
        to_account_type,
        to_account_number,
        amount
    ):
        from_account = self.get_account(
            pin,
            from_account_type,
            from_account_number
        )

        to_account = self.get_account(
            pin,
            to_account_type,
            to_account_number
        )

        if not from_account.withdraw(amount):
            raise ValueError("Transfer failed")

        to_account.deposit(amount)

        return True