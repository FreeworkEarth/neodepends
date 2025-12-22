"""
Ticket entity - IMPROVED: Uses IDs instead of object references
"""
from datetime import datetime


class Ticket:
    """Ticket with IDs (decoupled from Passenger, Route, Train)"""

    def __init__(self, ticket_id: str, passenger_id: str, route_id: str, train_id: str,
                 seat_number: str, fare: float, travel_date: str):
        self.ticket_id = ticket_id
        self.passenger_id = passenger_id  # CHANGED: ID not object!
        self.route_id = route_id  # CHANGED: ID not object!
        self.train_id = train_id  # CHANGED: ID not object!
        self.seat_number = seat_number
        self.fare = fare
        self.booking_date = datetime.now().isoformat()
        self.travel_date = travel_date
        self.status = "CONFIRMED"

    def cancel(self):
        """Cancel this ticket"""
        self.status = "CANCELLED"

    def display_info(self):
        print(f"Ticket: {self.ticket_id} [{self.status}]")
        print(f"Passenger: {self.passenger_id}")
        print(f"Train: {self.train_id} on Route: {self.route_id}")
        print(f"Seat: {self.seat_number}, Fare: ${self.fare}")
        print(f"Travel Date: {self.travel_date}")
