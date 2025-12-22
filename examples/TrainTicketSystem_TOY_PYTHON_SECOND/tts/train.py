"""
Train entity - MAJOR IMPROVEMENT: Uses route ID instead of Route object
This breaks the cyclic dependency!
"""


class Train:
    """Train with route ID (decoupled from Route)"""

    def __init__(self, train_id: str, train_name: str, route_id: str, total_seats: int,
                 departure_time: str, arrival_time: str):
        self.train_id = train_id
        self.train_name = train_name
        self.route_id = route_id  # CHANGED: ID not object!
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def book_seat(self) -> bool:
        """Book a seat if available"""
        if self.available_seats > 0:
            self.available_seats -= 1
            return True
        return False

    def cancel_seat(self):
        """Cancel a seat booking"""
        if self.available_seats < self.total_seats:
            self.available_seats += 1

    def display_info(self):
        print(f"Train: {self.train_name} ({self.train_id})")
        print(f"Route: {self.route_id}")
        print(f"Schedule: {self.departure_time} - {self.arrival_time}")
        print(f"Seats: {self.available_seats}/{self.total_seats}")
