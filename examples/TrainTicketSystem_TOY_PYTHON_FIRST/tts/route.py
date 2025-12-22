"""
Route entity - COUPLED to TrainStation (creates CYCLE!)
"""
from __future__ import annotations

from typing import List


class Route:
    """Route with TrainStation object references - creates cyclic dependency!"""

    def __init__(self, route_id: str, origin, destination, distance: float):
        self.route_id = route_id
        self.origin = origin  # TrainStation object - creates dependency!
        self.destination = destination  # TrainStation object
        self.intermediate_stops: List = []  # List of TrainStation objects
        self.distance = distance
        self.base_fare = self._calculate_fare()

    def add_intermediate_stop(self, station):
        """Add intermediate stop (TrainStation dependency)"""
        self.intermediate_stops.append(station)

    def _calculate_fare(self) -> float:
        # Simple fare calculation: $0.10 per km
        return self.distance * 0.10

    def get_route_id(self) -> str:
        return self.route_id

    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination

    def get_distance(self) -> float:
        return self.distance

    def get_base_fare(self) -> float:
        return self.base_fare

    def get_intermediate_stops(self) -> List:
        return self.intermediate_stops

    def display_info(self):
        print(f"Route: {self.route_id}")
        print(f"Origin: {self.origin.get_name()}")
        print(f"Destination: {self.destination.get_name()}")
        print(f"Distance: {self.distance} km")
        print(f"Base Fare: ${self.base_fare}")
        if self.intermediate_stops:
            print("Stops: " + " ".join(stop.get_name() for stop in self.intermediate_stops))
