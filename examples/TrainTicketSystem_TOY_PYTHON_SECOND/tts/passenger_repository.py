"""
NEW CLASS: Repository pattern
Manages Passenger entities separately
"""
from typing import Dict, List, Optional
from tts.passenger import Passenger


class PassengerRepository:
    """Repository for Passenger entities"""

    def __init__(self):
        self.passengers: Dict[str, Passenger] = {}

    def add_passenger(self, passenger: Passenger):
        """Add a passenger to the repository"""
        self.passengers[passenger.id] = passenger

    def get_passenger(self, passenger_id: str) -> Optional[Passenger]:
        """Get passenger by ID"""
        return self.passengers.get(passenger_id)

    def get_all_passengers(self) -> List[Passenger]:
        """Get all passengers"""
        return list(self.passengers.values())
