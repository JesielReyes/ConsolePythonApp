USERS = [
    {"id": 1, "name": "Alice", "is_admin": True},
    {"id": 2, "name": "Bob", "is_admin": False},
    {"id": 3, "name": "Casey", "is_admin": False},
]

ACCOUNTS = [
    {
        "id": 1,
        "owner_id": 1,
        "account_number": "123456789",
        "balance": 1000.0,
        "account_type": "checking",
    },
    {
        "id": 2,
        "owner_id": 2,
        "account_number": "987654321",
        "balance": 500.0,
        "account_type": "savings",
    },
    {
        "id": 3,
        "owner_id": 3,
        "account_number": "555555555",
        "balance": 0.0,
        "account_type": "checking",
    },
]

TRANSACTION_HISTORY = []
