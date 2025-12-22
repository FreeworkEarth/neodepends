"""
NEW CLASS: Service layer for booking operations
REPLACES the god class from FIRST version
Uses repositories instead of managing entities directly
"""
from typing import List, Optional
from datetime import datetime
from tts.train_repository import TrainRepository
from tts.route_repository import RouteRepository
from tts.ticket_repository import TicketRepository
from tts.passenger_repository import PassengerRepository
from tts.train_station_repository import TrainStationRepository
from tts.ticket import Ticket


class BookingService:
    """Service layer for booking operations using repositories"""

    def __init__(self, train_repo: TrainRepository, route_repo: RouteRepository,
                 ticket_repo: TicketRepository, passenger_repo: PassengerRepository,
                 station_repo: TrainStationRepository):
        self.train_repo = train_repo
        self.route_repo = route_repo
        self.ticket_repo = ticket_repo
        self.passenger_repo = passenger_repo
        self.station_repo = station_repo

    def book_ticket(self, passenger_id: str, train_id: str, travel_date: str) -> Optional[Ticket]:
        """Book a ticket for a passenger"""
        passenger = self.passenger_repo.get_passenger(passenger_id)
        train = self.train_repo.get_train(train_id)

        if not passenger or not train:
            return None

        if not train.book_seat():
            print("No seats available")
            return None

        ticket_id = f"TKT-{int(datetime.now().timestamp() * 1000)}"
        seat_number = str(train.total_seats - train.available_seats)
        route = self.route_repo.get_route(train.route_id)
        fare = route.base_fare if route else 0.0

        ticket = Ticket(ticket_id, passenger_id, train.route_id,
                       train_id, seat_number, fare, travel_date)

        self.ticket_repo.add_ticket(ticket)
        passenger.add_ticket(ticket_id)

        return ticket

    def cancel_ticket(self, ticket_id: str) -> bool:
        """Cancel a ticket"""
        ticket = self.ticket_repo.get_ticket(ticket_id)
        if not ticket or ticket.status == "CANCELLED":
            return False

        train = self.train_repo.get_train(ticket.train_id)
        if train:
            train.cancel_seat()

        ticket.cancel()
        return True

    def search_trains(self, route_id: str) -> List:
        """Search trains by route"""
        return self.train_repo.get_trains_by_route(route_id)

    def get_passenger_tickets(self, passenger_id: str) -> List[Ticket]:
        """Get all tickets for a passenger"""
        return self.ticket_repo.get_tickets_by_passenger(passenger_id)
