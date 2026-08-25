from abc import ABC
from models.AccountOperations import AccountOperations


class Account(AccountOperations, ABC):

    def __init__(self, account_number, customer_id, balance=0):
        self._account_number = account_number
        self._customer_id = customer_id
        self._balance = balance

    def get_account_number(self):
        return self._account_number

    def get_customer_id(self):
        return self._customer_id

    def get_balance(self):
        return self._balance