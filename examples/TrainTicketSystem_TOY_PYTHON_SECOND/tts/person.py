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

    @abstractmethod
    def display_info(self):
        """Display person information"""
        pass
