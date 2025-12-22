"""
Train entity - COUPLED to Route (completes the CYCLE!)
Route → TrainStation → Train → Route (3-way cycle)
"""
from __future__ import annotations


class Train:
    """Train with Route object reference - completes cyclic dependency!"""

    def __init__(self, train_number: str, train_name: str, total_seats: int, train_type: str):
        self.train_number = train_number
        self.train_name = train_name
        self.total_seats = total_seats
        self.booked_seats = []
        self.route = None
        self.type = train_type  # Express, Local, etc.

    def set_route(self, route) -> None:
        self.route = route

    def get_route(self):
        return self.route

    def get_train_number(self) -> str:
        return self.train_number

    def get_train_name(self) -> str:
        return self.train_name

    def get_total_seats(self) -> int:
        return self.total_seats

    def get_available_seats(self) -> int:
        return self.total_seats - len(self.booked_seats)

    @property
    def available_seats(self) -> int:
        return self.get_available_seats()

    def is_seat_available(self, seat_number: str) -> bool:
        return seat_number not in self.booked_seats

    def book_seat(self, seat_number: str) -> bool:
        if self.is_seat_available(seat_number):
            self.booked_seats.append(seat_number)
            return True
        return False

    def release_seat(self, seat_number: str) -> None:
        if seat_number in self.booked_seats:
            self.booked_seats.remove(seat_number)

    def display_info(self):
        print(f"Train: {self.train_name} ({self.train_number})")
        print(f"Type: {self.type}")
        print(f"Available Seats: {self.get_available_seats()}/{self.total_seats}")
        if self.route is not None:
            print(f"Route: {self.route.get_origin().get_name()} → {self.route.get_destination().get_name()}")
