"""
Base abstract class for all people in the system
"""
from abc import ABC, abstractmethod


class Person(ABC):
    """Base abstract class for Person entities"""

    def __init__(self, name: str, person_id: str, email: str, phone: str):
        self.name = name
        self.id = person_id
        self.email = email
        self.phone = phone

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.id

    def get_email(self) -> str:
        return self.email

    def get_phone(self) -> str:
        return self.phone

    def set_name(self, name: str) -> None:
        self.name = name

    def set_email(self, email: str) -> None:
        self.email = email

    def set_phone(self, phone: str) -> None:
        self.phone = phone

    @abstractmethod
    def display_info(self):
        """Display person information"""
        pass
