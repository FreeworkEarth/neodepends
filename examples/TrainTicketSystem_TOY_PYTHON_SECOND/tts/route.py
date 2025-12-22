"""
Route entity - MAJOR IMPROVEMENT: Uses station IDs instead of TrainStation objects
This breaks the cyclic dependency!
"""
from typing import List


class Route:
    """Route with station IDs (decoupled from TrainStation)"""

    def __init__(self, route_id: str, origin_station_id: str, destination_station_id: str,
                 distance: float, base_fare: float):
        self.route_id = route_id
        self.origin_station_id = origin_station_id  # CHANGED: ID not object!
        self.destination_station_id = destination_station_id  # CHANGED: ID not object!
        self.intermediate_stop_ids: List[str] = []  # CHANGED: List of IDs
        self.distance = distance
        self.base_fare = base_fare

    def add_intermediate_stop(self, station_id: str):
        """Add intermediate stop ID"""
        self.intermediate_stop_ids.append(station_id)

    def display_info(self):
        print(f"Route: {self.route_id}")
        print(f"From: {self.origin_station_id} To: {self.destination_station_id}")
        print(f"Distance: {self.distance} km, Fare: ${self.base_fare}")
        print(f"Stops: {len(self.intermediate_stop_ids)}")
