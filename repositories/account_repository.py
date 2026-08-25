from models.CheckingAccount import CheckingAccount
from models.SavingsAccount import SavingsAccount


# --------------------------------
# Dummy Data
# --------------------------------

accounts = {
    1001: CheckingAccount(1001, 2, 1500),
    2001: SavingsAccount(2001, 2, 5000),
    1002: CheckingAccount(1002, 3, 800)
}


# --------------------------------
# Repository Functions
# --------------------------------

def get_all_accounts():
    return list(accounts.values())


def get_account(account_number):
    return accounts.get(account_number)


def get_accounts_by_customer(customer_id):
    result = []

    for account in accounts.values():
        if account.get_customer_id() == customer_id:
            result.append(account)

    return result


def add_account(account):
    account_number = account.get_account_number()

    accounts[account_number] = account

    return account


def delete_account(account_number):
    if account_number not in accounts:
        return False

    del accounts[account_number]

    return True