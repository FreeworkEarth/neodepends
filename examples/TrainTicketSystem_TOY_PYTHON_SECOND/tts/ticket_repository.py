"""
NEW CLASS: Repository pattern
Manages Ticket entities separately
"""
from typing import Dict, List, Optional
from tts.ticket import Ticket


class TicketRepository:
    """Repository for Ticket entities"""

    def __init__(self):
        self.tickets: Dict[str, Ticket] = {}

    def add_ticket(self, ticket: Ticket):
        """Add a ticket to the repository"""
        self.tickets[ticket.ticket_id] = ticket

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get ticket by ID"""
        return self.tickets.get(ticket_id)

    def get_all_tickets(self) -> List[Ticket]:
        """Get all tickets"""
        return list(self.tickets.values())

    def get_tickets_by_passenger(self, passenger_id: str) -> List[Ticket]:
        """Get tickets for a specific passenger"""
        result = []
        for ticket in self.tickets.values():
            if ticket.passenger_id == passenger_id:
                result.append(ticket)
        return result
