from models.user import User


class Admin(User):
    def __init__(self, email, owner_id, birthday, phone_number, first_name, last_name):
        super().__init__(email, owner_id, birthday, phone_number, first_name, last_name)

    def get_role(self):
        return "Admin"