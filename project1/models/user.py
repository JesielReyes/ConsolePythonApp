from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, pin, owner_id=None):
        self._pin = pin
        self._owner_id = owner_id

    def check_pin(self, pin):
        return self._pin == pin

    def change_pin(self, old_pin, new_pin):
        if not self.check_pin(old_pin):
            raise ValueError("Invalid PIN")

        self._pin = new_pin
        return True

    def get_owner_id(self):
        return self._owner_id

    @abstractmethod
    def get_role(self):
        pass