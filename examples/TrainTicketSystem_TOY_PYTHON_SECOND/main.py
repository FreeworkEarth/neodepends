"""
Main entry point - PROPER LAYERING
Only uses service layer and repositories
"""
from tts.train_station import TrainStation
from tts.route import Route
from tts.train import Train
from tts.passenger import Passenger
from tts.train_station_repository import TrainStationRepository
from tts.train_repository import TrainRepository
from tts.route_repository import RouteRepository
from tts.passenger_repository import PassengerRepository
from tts.ticket_repository import TicketRepository
from tts.booking_service import BookingService
from tts.ticket_agent import TicketAgent
from tts.station_manager import StationManager
from tts.reporting_service import AdvancedReportingService


def main():
    print("=== Train Ticket Booking System (SECOND - Refactored) ===\n")

    # Initialize repositories
    station_repo = TrainStationRepository()
    train_repo = TrainRepository()
    route_repo = RouteRepository()
    passenger_repo = PassengerRepository()
    ticket_repo = TicketRepository()

    # Initialize service
    booking_service = BookingService(train_repo, route_repo, ticket_repo,
                                    passenger_repo, station_repo)

    # Create staff roles (minimal coupling: IDs only)
    agent1 = TicketAgent("John Smith", "EMP001", "john@railway.com", "555-0100", "AGT001", 45000.0, "NYC-001")
    manager1 = StationManager("Mary Johnson", "EMP002", "mary@railway.com", "555-0200", "MGR001", 75000.0, "NYC-001")

    # Create stations (via repository)
    nyc_station = TrainStation("NYC-001", "Penn Station", "New York", "NY")
    boston_station = TrainStation("BOS-001", "South Station", "Boston", "MA")
    station_repo.add_station(nyc_station)
    station_repo.add_station(boston_station)

    # Create routes (uses station IDs, not objects!)
    route1 = Route("R-001", "NYC-001", "BOS-001", 350.0, 89.99)
    route_repo.add_route(route1)

    # Create trains (uses route IDs, not objects!)
    train1 = Train("T-001", "Northeast Express", "R-001", 200, "08:00", "12:30")
    train2 = Train("T-002", "Boston Flyer", "R-001", 150, "14:00", "18:30")
    train_repo.add_train(train1)
    train_repo.add_train(train2)

    # Create passengers
    passenger1 = Passenger("John Doe", "P-001", "john@email.com", "555-1234")
    passenger2 = Passenger("Jane Smith", "P-002", "jane@email.com", "555-5678")
    passenger_repo.add_passenger(passenger1)
    passenger_repo.add_passenger(passenger2)

    print("--- Initial System State ---")
    print(f"Stations: {len(station_repo.get_all_stations())}")
    print(f"Routes: {len(route_repo.get_all_routes())}")
    print(f"Trains: {len(train_repo.get_all_trains())}")
    print(f"Passengers: {len(passenger_repo.get_all_passengers())}")
    print()

    # Book tickets through service
    print("--- Booking Tickets ---")
    ticket1 = booking_service.book_ticket("P-001", "T-001", "2025-12-20")
    if ticket1:
        print(f"✓ Booked: {ticket1.ticket_id}")
        ticket1.display_info()
        print()

    ticket2 = booking_service.book_ticket("P-002", "T-002", "2025-12-21")
    if ticket2:
        print(f"✓ Booked: {ticket2.ticket_id}")
        ticket2.display_info()
        print()

    # Search trains through service
    print("--- Searching Trains on Route R-001 ---")
    trains_on_route = booking_service.search_trains("R-001")
    print(f"Found {len(trains_on_route)} trains:")
    for t in trains_on_route:
        t.display_info()
        print()

    # View passenger tickets through service
    print("--- Passenger Bookings ---")
    p1_tickets = booking_service.get_passenger_tickets("P-001")
    print(f"Passenger P-001 has {len(p1_tickets)} ticket(s)")

    # Cancel ticket through service
    print("\n--- Cancelling Ticket ---")
    if ticket1 and booking_service.cancel_ticket(ticket1.ticket_id):
        print(f"✓ Cancelled: {ticket1.ticket_id}")
        ticket1.display_info()

    # Reporting layer (extra for dependency experiments)
    reporting = AdvancedReportingService(train_repo, route_repo, ticket_repo, passenger_repo, station_repo)
    summary = reporting.generate_executive_summary()
    print("\n--- Executive Summary ---")
    print(f"Stations: {summary['total_stations']}, Trains: {summary['total_trains']}, Tickets: {summary['total_tickets']}")

    # Display staff info (for demo parity with FIRST)
    print("\n--- Staff ---")
    agent1.display_info()
    print()
    manager1.display_info()

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
