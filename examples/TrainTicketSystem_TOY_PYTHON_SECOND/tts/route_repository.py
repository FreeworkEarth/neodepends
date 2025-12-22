"""
NEW CLASS: Repository pattern
Manages Route entities separately
"""
from typing import Dict, List, Optional
from tts.route import Route


class RouteRepository:
    """Repository for Route entities"""

    def __init__(self):
        self.routes: Dict[str, Route] = {}

    def add_route(self, route: Route):
        """Add a route to the repository"""
        self.routes[route.route_id] = route

    def get_route(self, route_id: str) -> Optional[Route]:
        """Get route by ID"""
        return self.routes.get(route_id)

    def get_all_routes(self) -> List[Route]:
        """Get all routes"""
        return list(self.routes.values())

    def get_routes_by_station(self, station_id: str) -> List[Route]:
        """Get routes that include a station"""
        result = []
        for route in self.routes.values():
            if (route.origin_station_id == station_id or
                route.destination_station_id == station_id or
                station_id in route.intermediate_stop_ids):
                result.append(route)
        return result
