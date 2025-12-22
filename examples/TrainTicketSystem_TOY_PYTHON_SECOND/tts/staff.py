"""
Base class for staff members
"""
from tts.person import Person


class Staff(Person):
    """Base class for all staff members"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float):
        super().__init__(name, person_id, email, phone)
        self.employee_id = employee_id
        self.salary = salary
