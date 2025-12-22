"""
Passenger entity - IMPROVED: Uses ticket IDs instead of Ticket objects
"""
from typing import List
from tts.person import Person


class Passenger(Person):
    """Passenger entity with ticket IDs (decoupled from Ticket class)"""

    def __init__(self, name: str, person_id: str, email: str, phone: str):
        super().__init__(name, person_id, email, phone)
        self.ticket_ids: List[str] = []  # CHANGED: Just IDs, not objects!

    def add_ticket(self, ticket_id: str):
        """Add a ticket ID (no dependency on Ticket class)"""
        self.ticket_ids.append(ticket_id)

    def display_info(self):
        print(f"Passenger: {self.name} (ID: {self.id})")
        print(f"Email: {self.email}, Phone: {self.phone}")
        print(f"Tickets: {len(self.ticket_ids)}")
