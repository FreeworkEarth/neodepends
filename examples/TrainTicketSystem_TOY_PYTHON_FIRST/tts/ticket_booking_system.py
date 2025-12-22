"""
TicketBookingSystem - GOD CLASS (Singleton)
Manages ALL entities - creates massive coupling hub!
This is the central anti-pattern in FIRST version
Extends BaseManagementSystem for logging and statistics

NOTE: This is a PERFECT MIRROR of the Java version for Deicide comparison
"""
from typing import List, Optional
from tts.base_management_system import BaseManagementSystem


class TicketBookingSystem(BaseManagementSystem):
    """
    GOD CLASS - Singleton pattern managing everything
    This creates a central coupling hub - BAD DESIGN!
    Extends BaseManagementSystem (adds Extend dependency)
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # God class manages ALL entities!
        self.stations: List = []
        self.trains: List = []
        self.routes: List = []
        self.passengers: List = []
        self.staff: List = []

    @classmethod
    def get_instance(cls):
        """Singleton access - mirrors Java's getInstance()"""
        return cls()

    # Station management
    def add_station(self, station):
        """Add a station - mirrors Java's addStation()"""
        self.stations.append(station)

    def find_station(self, station_code: str):
        """Find station by code - mirrors Java's findStation()"""
        for station in self.stations:
            if station.station_code == station_code:
                return station
        return None

    # Train management
    def add_train(self, train):
        """Add a train - mirrors Java's addTrain()"""
        self.trains.append(train)

    def find_train(self, train_number: str):
        """Find train by number - mirrors Java's findTrain()"""
        for train in self.trains:
            if train.train_number == train_number:
                return train
        return None

    # Route management
    def add_route(self, route):
        """Add a route - mirrors Java's addRoute()"""
        self.routes.append(route)

    def find_routes(self, origin, destination) -> List:
        """
        Find routes between two stations - mirrors Java's findRoutes()

        Args:
            origin: Origin station object
            destination: Destination station object

        Returns:
            List of matching routes
        """
        matching_routes = []
        for route in self.routes:
            if (route.origin.station_code == origin.station_code and
                route.destination.station_code == destination.station_code):
                matching_routes.append(route)
        return matching_routes

    # Passenger management
    def register_passenger(self, passenger):
        """Register passenger - mirrors Java's registerPassenger()"""
        self.passengers.append(passenger)

    def find_passenger(self, passenger_id: str):
        """Find passenger by ID - mirrors Java's findPassenger()"""
        for passenger in self.passengers:
            if passenger.id == passenger_id:
                return passenger
        return None

    # Staff management
    def add_staff(self, staff_member):
        """Add staff member - mirrors Java's addStaff()"""
        self.staff.append(staff_member)

    # Search operations
    def search_available_trains(self, origin, destination) -> List:
        """
        Search for available trains - mirrors Java's searchAvailableTrains()

        Args:
            origin: Origin station object
            destination: Destination station object

        Returns:
            List of available trains
        """
        available = []
        for train in self.trains:
            if (train.route is not None and
                train.route.origin.station_code == origin.station_code and
                train.route.destination.station_code == destination.station_code and
                train.available_seats > 0):
                available.append(train)
        return available

    # Getters - mirror Java's getters
    def get_stations(self) -> List:
        """Get all stations"""
        return self.stations

    def get_trains(self) -> List:
        """Get all trains"""
        return self.trains

    def get_routes(self) -> List:
        """Get all routes"""
        return self.routes

    def get_passengers(self) -> List:
        """Get all passengers"""
        return self.passengers

    def get_staff(self) -> List:
        """Get all staff"""
        return self.staff

    # Display statistics (override from BaseManagementSystem)
    def display_system_stats(self):
        """Display system statistics - mirrors Java's displaySystemStats()"""
        print("\n═══════ SYSTEM STATISTICS ═══════")
        print(f"Total Stations: {len(self.stations)}")
        print(f"Total Trains: {len(self.trains)}")
        print(f"Total Routes: {len(self.routes)}")
        print(f"Registered Passengers: {len(self.passengers)}")
        print(f"Staff Members: {len(self.staff)}")
        print("════════════════════════════════\n")

    # Analytics - Revenue Analysis (mirrors Java's analyzeRevenue)
    def analyze_revenue(self):
        """Calculate total potential revenue - mirrors Java's analyzeRevenue()"""
        total_revenue = 0.0
        for route in self.routes:
            total_revenue += route.base_fare  # Call dependency
        print(f"Estimated Daily Revenue: ${total_revenue}")
        self.log_action(f"Revenue analysis performed: ${total_revenue}")

    # Analytics - System Capacity (mirrors Java's getTotalCapacity)
    def get_total_capacity(self) -> int:
        """Get total system capacity - mirrors Java's getTotalCapacity()"""
        total = 0
        for train in self.trains:
            total += train.total_seats  # Call dependency
        return total


class ReportingSystem:
    """
    ReportingSystem - Second God Class for testing multi-class file analysis.
    Handles reporting and analytics on top of TicketBookingSystem.

    This is a Python mirror of the Java version, using snake_case method names.
    """

    def __init__(self, booking_system: TicketBookingSystem):
        self.booking_system = booking_system
        self.reports: List = []
        self.metrics: dict = {}
        self.cached_stats: Optional[dict] = None

    def generate_station_report(self) -> List[dict]:
        report: List[dict] = []
        for station in self.booking_system.get_stations():
            station_data = {
                "code": station.station_code,
                "name": station.name,
                "trains": len(station.available_trains),
            }
            report.append(station_data)
        self.reports.append(("station", report))
        return report

    def generate_train_report(self) -> List[dict]:
        report: List[dict] = []
        for train in self.booking_system.get_trains():
            train_data = {
                "id": train.train_number,
                "name": train.train_name,
                "seats": train.total_seats,
                "available": train.available_seats,
            }
            report.append(train_data)
        self.reports.append(("train", report))
        return report

    def generate_passenger_report(self) -> List[dict]:
        report: List[dict] = []
        for passenger in self.booking_system.get_passengers():
            passenger_data = {
                "id": passenger.passenger_id,
                "name": passenger.name,
                "email": passenger.email,
            }
            report.append(passenger_data)
        self.reports.append(("passenger", report))
        return report

    def calculate_occupancy_rate(self) -> float:
        total_seats = 0
        booked_seats = 0
        for train in self.booking_system.get_trains():
            total_seats += train.total_seats
            booked_seats += (train.total_seats - train.available_seats)
        rate = (booked_seats * 100.0 / total_seats) if total_seats > 0 else 0.0
        self.metrics["occupancy_rate"] = rate
        return rate

    def calculate_revenue(self) -> float:
        total = 0.0
        for train in self.booking_system.get_trains():
            if train.route is not None:
                booked = train.total_seats - train.available_seats
                total += booked * train.route.base_fare
        self.metrics["total_revenue"] = total
        return total

    def get_popular_routes(self, limit: int) -> List:
        route_bookings: dict[str, int] = {}
        for train in self.booking_system.get_trains():
            if train.route is not None:
                route_id = train.route.route_id
                bookings = train.total_seats - train.available_seats
                route_bookings[route_id] = route_bookings.get(route_id, 0) + bookings
        sorted_routes = sorted(route_bookings.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_routes[: min(limit, len(sorted_routes))]

    def get_station_traffic(self) -> dict:
        traffic: dict[str, int] = {}
        for route in self.booking_system.get_routes():
            origin_code = route.origin.station_code
            traffic[origin_code] = traffic.get(origin_code, 0) + 1

            dest_code = route.destination.station_code
            traffic[dest_code] = traffic.get(dest_code, 0) + 1
        self.cached_stats = traffic
        return traffic

    def generate_summary(self) -> dict:
        summary = {
            "total_stations": len(self.booking_system.get_stations()),
            "total_trains": len(self.booking_system.get_trains()),
            "total_routes": len(self.booking_system.get_routes()),
            "total_passengers": len(self.booking_system.get_passengers()),
            "occupancy_rate": self.calculate_occupancy_rate(),
            "total_revenue": self.calculate_revenue(),
            "reports_generated": len(self.reports),
        }
        self.metrics.update(summary)
        return summary

    def clear_cache(self) -> None:
        self.cached_stats = None
        self.metrics.clear()

    def export_all_reports(self) -> dict:
        return {
            "reports": self.reports,
            "metrics": self.metrics,
            "summary": self.generate_summary(),
        }


class AdvancedReportingSystem(ReportingSystem):
    """Subclass to test EXTEND dependencies in multi-class files."""

    def generate_executive_summary(self) -> dict:
        summary = self.generate_summary()
        summary["generated_by"] = "AdvancedReportingSystem"
        return summary
