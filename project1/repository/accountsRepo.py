from sqlmodel import Session, select

def get_user_account_by_number(session: Session, user_id: int, account_num: int):
    statement = select(Account).where(
        Account.account_num == account_num,
        Account.user_id == user_id
    )

    return session.exec(statement).first()

def get_account_by_number(session: Session, account_num: int):
    statement = select(Account).where(
        Account.account_num == account_num
    )
    return session.exec(statement).first()
