"""
Base class for staff members
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from tts.person import Person


class Staff(Person, ABC):
    """Base class for all staff members"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float, department: str):
        super().__init__(name, person_id, email, phone)
        self.employee_id = employee_id
        self.salary = salary
        self.department = department

    def get_employee_id(self) -> str:
        return self.employee_id

    def get_salary(self) -> float:
        return self.salary

    def get_department(self) -> str:
        return self.department

    @abstractmethod
    def perform_duties(self) -> None:
        raise NotImplementedError
