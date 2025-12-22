"""
StationManager - IMPROVED: Reduced to just employee data
Management logic moved to ManagementService
"""
from tts.staff import Staff


class StationManager(Staff):
    """StationManager with minimal coupling"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float, managed_station_id: str):
        super().__init__(name, person_id, email, phone, employee_id, salary)
        self.managed_station_id = managed_station_id  # CHANGED: ID not object!

    def display_info(self):
        print(f"Station Manager: {self.name} (ID: {self.employee_id})")
        print(f"Managed Station: {self.managed_station_id}")
        print(f"Salary: ${self.salary}")
