from repositories import user_repository
from users.admin import Admin
from users.customer import Customer


def get_all_users():
    return user_repository.get_all_users()


def get_user(user_id):
    user = user_repository.get_user(user_id)

    if user is None:
        raise ValueError("User not found")

    return user


def create_user(pin, is_admin):
    user_id = user_repository.get_next_user_id()

    if is_admin:
        user = Admin(
            pin=pin,
            owner_id=user_id
        )
    else:
        user = Customer(
            pin=pin,
            owner_id=user_id
        )

    return user_repository.add_user(user)


def delete_user(user_id):
    user = user_repository.get_user(user_id)

    if user is None:
        raise ValueError("User not found")

    if not user_repository.delete_user(user_id):
        raise ValueError("User could not be deleted")

    return True