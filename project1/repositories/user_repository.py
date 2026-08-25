from users.admin import Admin
from users.customer import Customer


# Dummy data
users = {
    1: Admin(
        pin=1111,
        owner_id=1
    ),

    2: Customer(
        pin=2222,
        owner_id=2
    ),

    3: Customer(
        pin=3333,
        owner_id=3
    )
}


def get_all_users():
    return list(users.values())


def get_user(user_id):
    return users.get(user_id)


def add_user(user):
    users[user.get_owner_id()] = user
    return user


def delete_user(user_id):
    if user_id not in users:
        return False

    del users[user_id]
    return True


def get_next_user_id():
    return max(users.keys(), default=0) + 1