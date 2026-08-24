from accounts.CheckingAccount import CheckingAccount
from accounts.InvestmentAccount import InvestmentAccount
from accounts.SavingsAccount import SavingsAccount
from accounts.BusinessAccount import BusinessAccount
from accounts.CreditAccount import CreditAccount
class User:
    def __init__(self, pin):
        self._accounts = {"Checking": {}, "Savings": {}, "Credit": {}, "Business": {}, "Investment": {}}
        self._pin = pin

    def create_account(self, pin, account_type, balance=0):
        if not self.check_pin(pin):
            raise ValueError("Invalid PIN")
        if account_type == "Checking":
            account = CheckingAccount(balance)
        elif account_type == "Savings":
            account = SavingsAccount(balance)
        elif account_type == "Business":
            account = BusinessAccount(balance)
        elif account_type == "Investment":
            account = InvestmentAccount(balance)
        elif account_type == "Credit":
            account = CreditAccount()
        else:
            raise ValueError("Invalid account type")
        if account.get_account_number() in self._accounts[account_type]:
            raise ValueError("Account number already exists")
        self._accounts[account_type][account.get_account_number()] = account
        return account.get_account_number()

    def check_pin(self, pin):
        return pin == self._pin
    
    def can_make_purchase(self, pin, account_type):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if not self._accounts[account_type]:
            raise ValueError("No accounts of this type exist")
        if account_type in ["Investment", "Savings"]:
            raise ValueError(f"Purchases from Investment or Savings accounts are not allowed")
    
    def change_pin(self, old_pin, new_pin):
        if self.check_pin(old_pin) is False:
            raise ValueError("Invalid old PIN")
        self._pin = new_pin
        print("PIN changed successfully!")

    def get_accounts(self, pin, account_type):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if account_type not in self._accounts:
            raise ValueError("Invalid account type")
        return self._accounts[account_type]

    def get_account(self, pin, account_type, account_number):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if account_type not in self._accounts:
            raise ValueError("Invalid account type")
        if account_number not in self._accounts[account_type]:
            raise ValueError("Account number does not exist")
        return self._accounts[account_type][account_number]
    
    def get_minimum_balance(self, account_type):
        if account_type == "Checking":
            return 500
        elif account_type == "Savings":
            return 2000
        elif account_type == "Business":
            return 10000
        elif account_type == "Investment":
            return 1000
        elif account_type == "Credit":
            return 0
        else:
            raise ValueError("Invalid account type")
    
    def get_all_accounts(self, pin):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if not any(self._accounts.values()):
            raise ValueError("No accounts exist for this user")
        for account_type, accounts in self._accounts.items():
            for account_number, account in accounts.items():
                print(f"Account Type: {account_type}, Balance: {account.get_balance()}")
        return self._accounts
    
    def make_purchase(self, pin, account_type, account_number, amount):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if account_type not in self._accounts:
            raise ValueError("Invalid account type")
        if account_number not in self._accounts[account_type]:
            raise ValueError("Account number does not exist")
        account = self._accounts[account_type][account_number]
        account.withdraw(amount)
        return True

    def make_payment(self, pin, account_type, account_number, amount):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if account_type not in self._accounts:
            raise ValueError("Invalid account type")
        if account_number not in self._accounts[account_type]:
            raise ValueError("Account number does not exist")
        account = self._accounts[account_type][account_number]
        account.deposit(amount)
        return True
    
    def transfer_funds(self, pin, from_account_type, from_account_number, to_account_type, to_account_number, amount):
        if self.check_pin(pin) is False:
            raise ValueError("Invalid PIN")
        if from_account_type == "Credit":
            raise ValueError("Transfers from Credit accounts are not allowed")
        if from_account_type not in self._accounts or to_account_type not in self._accounts:
            raise ValueError("Invalid account type")
        if from_account_number not in self._accounts[from_account_type] or to_account_number not in self._accounts[to_account_type]:
            raise ValueError("Account number does not exist")
        from_account = self._accounts[from_account_type][from_account_number]
        to_account = self._accounts[to_account_type][to_account_number]
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            return True
        else:
            raise ValueError("Insufficient funds for transfer")
        
        
    