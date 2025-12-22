"""
ReportingService - analytics/reporting layer (extra for dependency experiments)

Keeps the "SECOND" architecture style (repositories + IDs) but adds:
- a reporting service that depends on repositories
- a subclass (AdvancedReportingService) to test Extend dependencies
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from tts.passenger_repository import PassengerRepository
from tts.route_repository import RouteRepository
from tts.ticket_repository import TicketRepository
from tts.train_repository import TrainRepository
from tts.train_station_repository import TrainStationRepository


class ReportingService:
    """Reporting and analytics on top of repositories."""

    def __init__(
        self,
        train_repo: TrainRepository,
        route_repo: RouteRepository,
        ticket_repo: TicketRepository,
        passenger_repo: PassengerRepository,
        station_repo: TrainStationRepository,
    ):
        self.train_repo = train_repo
        self.route_repo = route_repo
        self.ticket_repo = ticket_repo
        self.passenger_repo = passenger_repo
        self.station_repo = station_repo

        self.reports: List[Tuple[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
        self.cached_stats: Optional[Dict[str, Any]] = None

    def generate_station_report(self) -> List[Dict[str, Any]]:
        report: List[Dict[str, Any]] = []
        for station in self.station_repo.get_all_stations():
            station_routes = self.route_repo.get_routes_by_station(station.station_id)
            station_route_ids = {r.route_id for r in station_routes}
            trains_on_station_routes = [
                t for t in self.train_repo.get_all_trains() if t.route_id in station_route_ids
            ]
            report.append(
                {
                    "id": station.station_id,
                    "name": station.station_name,
                    "city": station.city,
                    "routes": len(station_routes),
                    "trains": len(trains_on_station_routes),
                }
            )
        self.reports.append(("station", report))
        return report

    def generate_train_report(self) -> List[Dict[str, Any]]:
        report: List[Dict[str, Any]] = []
        for train in self.train_repo.get_all_trains():
            report.append(
                {
                    "id": train.train_id,
                    "name": train.train_name,
                    "route": train.route_id,
                    "seats_total": train.total_seats,
                    "seats_available": train.available_seats,
                    "departure": train.departure_time,
                    "arrival": train.arrival_time,
                }
            )
        self.reports.append(("train", report))
        return report

    def generate_passenger_report(self) -> List[Dict[str, Any]]:
        report: List[Dict[str, Any]] = []
        for passenger in self.passenger_repo.get_all_passengers():
            report.append(
                {
                    "id": passenger.id,
                    "name": passenger.name,
                    "email": passenger.email,
                    "tickets": len(passenger.ticket_ids),
                }
            )
        self.reports.append(("passenger", report))
        return report

    def calculate_occupancy_rate(self) -> float:
        total_seats = 0
        booked_seats = 0
        for train in self.train_repo.get_all_trains():
            total_seats += train.total_seats
            booked_seats += train.total_seats - train.available_seats
        rate = (booked_seats * 100.0 / total_seats) if total_seats > 0 else 0.0
        self.metrics["occupancy_rate"] = rate
        return rate

    def calculate_revenue(self) -> float:
        total = 0.0
        for ticket in self.ticket_repo.get_all_tickets():
            if ticket.status == "CONFIRMED":
                total += ticket.fare
        self.metrics["total_revenue"] = total
        return total

    def get_popular_routes(self, limit: int) -> List[Tuple[str, int]]:
        route_bookings: Dict[str, int] = {}
        for ticket in self.ticket_repo.get_all_tickets():
            route_bookings[ticket.route_id] = route_bookings.get(ticket.route_id, 0) + 1
        sorted_routes = sorted(route_bookings.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_routes[: min(limit, len(sorted_routes))]

    def get_station_traffic(self) -> Dict[str, int]:
        traffic: Dict[str, int] = {}
        for route in self.route_repo.get_all_routes():
            traffic[route.origin_station_id] = traffic.get(route.origin_station_id, 0) + 1
            traffic[route.destination_station_id] = traffic.get(route.destination_station_id, 0) + 1
        self.cached_stats = traffic
        return traffic

    def generate_summary(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {
            "total_stations": len(self.station_repo.get_all_stations()),
            "total_routes": len(self.route_repo.get_all_routes()),
            "total_trains": len(self.train_repo.get_all_trains()),
            "total_passengers": len(self.passenger_repo.get_all_passengers()),
            "total_tickets": len(self.ticket_repo.get_all_tickets()),
            "occupancy_rate": self.calculate_occupancy_rate(),
            "total_revenue": self.calculate_revenue(),
            "reports_generated": len(self.reports),
        }
        self.metrics.update(summary)
        return summary

    def clear_cache(self) -> None:
        self.cached_stats = None
        self.metrics.clear()

    def export_all_reports(self) -> Dict[str, Any]:
        return {
            "reports": self.reports,
            "metrics": self.metrics,
            "summary": self.generate_summary(),
        }


class AdvancedReportingService(ReportingService):
    """Subclass to test Extend dependencies (service layer)."""

    def generate_executive_summary(self) -> Dict[str, Any]:
        summary = self.generate_summary()
        summary["generated_by"] = "AdvancedReportingService"
        return summary

