from abc import ABC, abstractmethod


class User(ABC):

    def __init__(self, user_id, name, username, password):
        self._user_id = user_id
        self._name = name
        self._username = username
        self._password = password

    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_username(self):
        return self._username

    def check_password(self, password):
        return self._password == password

    @abstractmethod
    def get_role(self):
        pass