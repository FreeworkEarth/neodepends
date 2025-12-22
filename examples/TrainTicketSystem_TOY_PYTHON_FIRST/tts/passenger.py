"""
Passenger entity - COUPLED to Ticket
"""
from typing import List
from tts.person import Person


class Passenger(Person):
    """Passenger entity with direct Ticket object references (COUPLING!)"""

    def __init__(self, name: str, person_id: str, email: str, phone: str, passport_number: str):
        super().__init__(name, person_id, email, phone)
        self.passport_number = passport_number
        self.booked_tickets: List = []  # Will contain Ticket objects - creates coupling!
        self.loyalty_points = 0

    def book_ticket(self, ticket) -> None:
        self.booked_tickets.append(ticket)
        self.loyalty_points += 10
        print(f"Ticket booked successfully for {self.name}")

    def cancel_ticket(self, ticket) -> None:
        if ticket in self.booked_tickets:
            self.booked_tickets.remove(ticket)
            self.loyalty_points = max(0, self.loyalty_points - 5)
            print("Ticket cancelled successfully")

    def add_ticket(self, ticket) -> None:
        self.book_ticket(ticket)

    def get_booked_tickets(self) -> List:
        return self.booked_tickets

    def get_loyalty_points(self) -> int:
        return self.loyalty_points

    def display_info(self):
        print(f"Passenger: {self.name}")
        print(f"ID: {self.id}")
        print(f"Loyalty Points: {self.loyalty_points}")
        print(f"Total Tickets: {len(self.booked_tickets)}")
