"""
Ticket entity - HIGHLY COUPLED to Passenger, Route, Train
"""
from datetime import datetime


class Ticket:
    """Ticket with multiple object dependencies - high coupling!"""

    ticket_counter = 1000

    def __init__(self, passenger, route, train, seat_number: str, price: float):
        self.ticket_id = f"TKT{Ticket.ticket_counter}"
        Ticket.ticket_counter += 1
        self.passenger = passenger  # Passenger object - creates dependency!
        self.route = route  # Route object - creates dependency!
        self.train = train  # Train object - creates dependency!
        self.seat_number = seat_number
        self.price = price
        self.booking_time = datetime.now()
        self.status = "BOOKED"

    def cancel(self):
        """Cancel this ticket"""
        self.status = "CANCELLED"
        self.train.release_seat(self.seat_number)

    def complete(self):
        self.status = "COMPLETED"

    def get_ticket_id(self) -> str:
        return self.ticket_id

    def get_passenger(self):
        return self.passenger

    def get_seat_number(self) -> str:
        return self.seat_number

    def get_price(self) -> float:
        return self.price

    def get_status(self) -> str:
        return self.status

    def display_info(self):
        self.display_ticket()

    def display_ticket(self):
        booked = self.booking_time.strftime("%Y-%m-%d %H:%M")
        print("╔══════════════ TRAIN TICKET ══════════════╗")
        print(f"  Ticket ID: {self.ticket_id}")
        print(f"  Passenger: {self.passenger.get_name() if hasattr(self.passenger, 'get_name') else self.passenger.name}")
        print(f"  Train: {self.train.get_train_name()} ({self.train.get_train_number()})")
        print(f"  Route: {self.route.get_origin().get_name()} → {self.route.get_destination().get_name()}")
        print(f"  Seat: {self.seat_number}")
        print(f"  Price: ${self.price:.2f}")
        print(f"  Booked: {booked}")
        print(f"  Status: {self.status}")
        print("╚══════════════════════════════════════════╝")
