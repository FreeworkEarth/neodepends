"""
NEW CLASS: Repository pattern
Manages TrainStation entities separately
Breaks up the god class from FIRST version
"""
from typing import Dict, List, Optional
from tts.train_station import TrainStation


class TrainStationRepository:
    """Repository for TrainStation entities"""

    def __init__(self):
        self.stations: Dict[str, TrainStation] = {}

    def add_station(self, station: TrainStation):
        """Add a station to the repository"""
        self.stations[station.station_id] = station

    def get_station(self, station_id: str) -> Optional[TrainStation]:
        """Get station by ID"""
        return self.stations.get(station_id)

    def get_all_stations(self) -> List[TrainStation]:
        """Get all stations"""
        return list(self.stations.values())

    def find_by_name(self, name: str) -> Optional[TrainStation]:
        """Find station by name"""
        for station in self.stations.values():
            if station.station_name.lower() == name.lower():
                return station
        return None
