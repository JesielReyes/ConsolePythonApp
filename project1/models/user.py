from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID


class User(ABC):
    def __init__(self, email, owner_id, birthday, phone_number, first_name, last_name):
        self.email = email
        self.birthday = birthday
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self._owner_id = owner_id

    def get_owner_id(self) -> UUID:
        return self._owner_id

    @abstractmethod
    def get_role(self):
        pass