from models.user import User


class Admin(User):
    def __init__(self, pin, owner_id=None):
        super().__init__(pin, owner_id)

    def get_role(self):
        return "Admin"