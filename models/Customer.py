from models.User import User


class Admin(User):

    def __init__(
        self,
        user_id,
        name,
        username,
        password
    ):
        super().__init__(
            user_id,
            name,
            username,
            password
        )

    def get_role(self):
        return "Admin"