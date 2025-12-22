"""
Main entry point - COUPLED to all 11 classes (poor layering!)
"""
from tts.train_station import TrainStation
from tts.train import Train
from tts.route import Route
from tts.passenger import Passenger
from tts.ticket_agent import TicketAgent
from tts.station_manager import StationManager
from tts.ticket_booking_system import TicketBookingSystem


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║   TRAIN TICKET BOOKING SYSTEM - DEMO        ║")
    print("╚══════════════════════════════════════════════╝\n")

    system = TicketBookingSystem.get_instance()

    # Create stations
    newyork = TrainStation("NYC", "New York Penn Station", "New York")
    boston = TrainStation("BOS", "Boston South Station", "Boston")
    philly = TrainStation("PHL", "Philadelphia 30th Street", "Philadelphia")

    system.add_station(newyork)
    system.add_station(boston)
    system.add_station(philly)

    # Create routes
    route1 = Route("R001", newyork, boston, 215.0)
    route1.add_intermediate_stop(philly)
    route2 = Route("R002", newyork, philly, 95.0)

    system.add_route(route1)
    system.add_route(route2)

    # Create trains
    acela = Train("TR001", "Acela Express", 300, "Express")
    acela.set_route(route1)
    northeast = Train("TR002", "Northeast Regional", 400, "Regional")
    northeast.set_route(route2)

    system.add_train(acela)
    system.add_train(northeast)

    newyork.add_train(acela)
    newyork.add_train(northeast)

    # Create staff
    agent1 = TicketAgent("John Smith", "EMP001", "john@railway.com", "555-0100", "AGT001", 45000.0)
    agent1.set_assigned_station(newyork)

    manager1 = StationManager("Mary Johnson", "EMP002", "mary@railway.com", "555-0200", "MGR001", 75000.0)
    manager1.set_managed_station(newyork)
    manager1.add_train_schedule(acela)
    manager1.add_train_schedule(northeast)

    newyork.add_agent(agent1)
    system.add_staff(agent1)
    system.add_staff(manager1)

    # Create passengers
    passenger1 = Passenger("Alice Brown", "P001", "alice@email.com", "555-1000", "P123456")
    passenger2 = Passenger("Bob Wilson", "P002", "bob@email.com", "555-2000", "P789012")

    system.register_passenger(passenger1)
    system.register_passenger(passenger2)

    # Display initial system state
    system.display_system_stats()

    print("\n═══════ DEMONSTRATION ═══════\n")

    # Demo: Search for trains
    print("1. Searching for trains from NYC to Boston...")
    available_trains = system.search_available_trains(newyork, boston)
    for t in available_trains:
        t.display_info()
        print()

    # Demo: Book tickets
    print("\n2. Booking tickets for Alice...")
    ticket1 = agent1.issue_ticket(passenger1, route1, acela, "A1", route1.get_base_fare())
    ticket1.display_ticket()

    print("\n3. Booking tickets for Bob...")
    ticket2 = agent1.issue_ticket(passenger2, route2, northeast, "B5", route2.get_base_fare())
    ticket2.display_ticket()

    # Display passenger info
    print("\n4. Passenger Information:")
    passenger1.display_info()
    print()
    passenger2.display_info()

    # Display staff performance
    print("\n5. Staff Performance:")
    agent1.display_info()
    print()
    manager1.display_info()

    # Demo: Cancel a ticket
    print("\n6. Cancelling Bob's ticket...")
    agent1.cancel_ticket(passenger2, ticket2)
    ticket2.display_ticket()

    # Final system stats
    print("\n7. Final System State:")
    system.display_system_stats()
    acela.display_info()

    print("\n╔══════════════════════════════════════════════╗")
    print("║          DEMO COMPLETE                       ║")
    print("╚══════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
