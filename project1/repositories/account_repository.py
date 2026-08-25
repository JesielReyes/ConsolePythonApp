accounts = {}


def add_account(account):
    account_number = account.get_account_number()

    accounts[account_number] = account

    return account


def get_account(account_number):
    return accounts.get(account_number)


def get_all_accounts():
    return list(accounts.values())


def get_accounts_by_owner(owner_id):
    result = []

    for account in accounts.values():
        if account.get_owner_id() == owner_id:
            result.append(account)

    return result


def delete_account(account_number):
    if account_number not in accounts:
        return False

    del accounts[account_number]

    return True