from repositories import user_repository
from repositories import account_repository


def create_account(
    owner_id,
    pin,
    account_type,
    balance
):
    user = user_repository.get_user(owner_id)

    if user is None:
        raise ValueError("User not found")

    if user.get_role() != "Customer":
        raise ValueError(
            "Only customers can create accounts"
        )

    account_number = user.create_account(
        pin,
        account_type,
        balance
    )

    account = user.get_account(
        pin,
        account_type,
        account_number
    )

    account_repository.add_account(account)

    return account


def get_account(account_number):
    account = account_repository.get_account(
        account_number
    )

    if account is None:
        raise ValueError("Account not found")

    return account


def get_accounts(owner_id=None):
    if owner_id is None:
        return account_repository.get_all_accounts()

    return account_repository.get_accounts_by_owner(
        owner_id
    )


def delete_account(account_number):
    account = get_account(account_number)

    if account.get_balance() != 0:
        raise ValueError(
            "Account balance must be zero before deletion"
        )

    if not account_repository.delete_account(
        account_number
    ):
        raise ValueError("Account could not be deleted")

    return True