"""
TrainStation entity - COUPLED to Train and TicketAgent (BIDIRECTIONAL!)
This creates the cyclic dependency chain
"""
from __future__ import annotations

from typing import List


class TrainStation:
    """TrainStation with bidirectional dependencies - BAD DESIGN!"""

    def __init__(self, station_code: str, name: str, city: str):
        self.station_code = station_code
        self.name = name
        self.city = city
        self.agents: List = []  # Will contain TicketAgent objects
        self.available_trains: List = []  # Will contain Train objects - creates cycle!

    def add_agent(self, agent):
        """Add ticket agent (bidirectional dependency)"""
        self.agents.append(agent)
        if hasattr(agent, "set_assigned_station"):
            agent.set_assigned_station(self)

    def add_train(self, train):
        """Add train (creates dependency, part of cycle)"""
        if train not in self.available_trains:
            self.available_trains.append(train)

    def remove_train(self, train):
        """Remove train from station"""
        if train in self.available_trains:
            self.available_trains.remove(train)

    def search_trains(self, destination: "TrainStation") -> List:
        """Search for trains going to the given destination"""
        matching_trains = []
        for train in self.available_trains:
            if train.route is not None and train.route.destination == destination:
                matching_trains.append(train)
        return matching_trains

    def get_station_code(self) -> str:
        return self.station_code

    def get_name(self) -> str:
        return self.name

    def get_city(self) -> str:
        return self.city

    def get_agents(self) -> List:
        return self.agents

    def display_info(self):
        print(f"Station: {self.name} ({self.station_code})")
        print(f"City: {self.city}")
        print(f"Agents: {len(self.agents)}, Trains: {len(self.available_trains)}")

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, TrainStation):
            return False
        return self.station_code == other.station_code

    def __hash__(self) -> int:
        return hash(self.station_code)
