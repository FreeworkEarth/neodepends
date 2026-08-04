"""
TicketAgent - IMPROVED: Reduced to just employee data
Business logic moved to BookingService
"""
from tts.staff import Staff


class TicketAgent(Staff):
    """TicketAgent with minimal coupling"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float, assigned_station_id: str):
        super().__init__(name, person_id, email, phone, employee_id, salary)
        self.assigned_station_id = assigned_station_id  # CHANGED: ID not object!

    def display_info(self):
        print(f"Ticket Agent: {self.name} (ID: {self.employee_id})")
        print(f"Assigned Station: {self.assigned_station_id}")
        print(f"Salary: ${self.salary}")

    def get_assigned_station_id(self) -> str:
        return self.assigned_station_id
