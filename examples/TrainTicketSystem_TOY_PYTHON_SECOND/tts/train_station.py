"""
TrainStation entity - MAJOR IMPROVEMENT: Pure entity, no collections
Removed all bidirectional dependencies
"""


class TrainStation:
    """TrainStation as pure entity - NO dependencies on other entities!"""

    def __init__(self, station_id: str, station_name: str, city: str, state: str):
        self.station_id = station_id
        self.station_name = station_name
        self.city = city
        self.state = state
        # REMOVED: agents list, available_trains list
        # These are now managed by repositories!

    def display_info(self):
        print(f"Station: {self.station_name} ({self.station_id})")
        print(f"Location: {self.city}, {self.state}")
