from sqlmodel import Session, select

from project1.dto.user_db import UserDB
from project1.models.admin import Admin
from project1.models.customer import Customer


def db_user_to_domain(db_user):
    if db_user.role == "Admin":
        return Admin(
            pin=db_user.pin,
            owner_id=db_user.id
        )

    return Customer(
        pin=db_user.pin,
        owner_id=db_user.id
    )


def get_all_users(session: Session):
    statement = select(UserDB)

    db_users = session.exec(statement).all()

    return [
        db_user_to_domain(user)
        for user in db_users
    ]


def get_user(
    session: Session,
    user_id: int
):
    db_user = session.get(
        UserDB,
        user_id
    )

    if db_user is None:
        raise ValueError("User not found")

    return db_user_to_domain(db_user)


def create_user(
    session: Session,
    pin: int,
    is_admin: bool
):
    role = (
        "Admin"
        if is_admin
        else "Customer"
    )

    db_user = UserDB(
        pin=pin,
        role=role
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user_to_domain(db_user)


def delete_user(
    session: Session,
    user_id: int
):
    db_user = session.get(
        UserDB,
        user_id
    )

    if db_user is None:
        raise ValueError("User not found")

    session.delete(db_user)
    session.commit()

    return True