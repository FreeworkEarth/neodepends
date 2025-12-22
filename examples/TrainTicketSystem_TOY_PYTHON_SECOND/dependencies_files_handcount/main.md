# `main.py`

## Totals (unique edges, internal-only)

- Import: 13
- Extend: 0
- Create: 13
- Call: 15
- Use: 0
- Total: 41

## Import edges

- main.py/module (Module) -> tts/booking_service.py/module (Module)
- main.py/module (Module) -> tts/passenger.py/module (Module)
- main.py/module (Module) -> tts/passenger_repository.py/module (Module)
- main.py/module (Module) -> tts/reporting_service.py/module (Module)
- main.py/module (Module) -> tts/route.py/module (Module)
- main.py/module (Module) -> tts/route_repository.py/module (Module)
- main.py/module (Module) -> tts/station_manager.py/module (Module)
- main.py/module (Module) -> tts/ticket_agent.py/module (Module)
- main.py/module (Module) -> tts/ticket_repository.py/module (Module)
- main.py/module (Module) -> tts/train.py/module (Module)
- main.py/module (Module) -> tts/train_repository.py/module (Module)
- main.py/module (Module) -> tts/train_station.py/module (Module)
- main.py/module (Module) -> tts/train_station_repository.py/module (Module)

## Create edges

- main.py/FUNCTIONS/main (Function) -> tts/booking_service.py/CLASSES/BookingService (Class)
- main.py/FUNCTIONS/main (Function) -> tts/passenger.py/CLASSES/Passenger (Class)
- main.py/FUNCTIONS/main (Function) -> tts/passenger_repository.py/CLASSES/PassengerRepository (Class)
- main.py/FUNCTIONS/main (Function) -> tts/reporting_service.py/CLASSES/AdvancedReportingService (Class)
- main.py/FUNCTIONS/main (Function) -> tts/route.py/CLASSES/Route (Class)
- main.py/FUNCTIONS/main (Function) -> tts/route_repository.py/CLASSES/RouteRepository (Class)
- main.py/FUNCTIONS/main (Function) -> tts/station_manager.py/CLASSES/StationManager (Class)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent (Class)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_repository.py/CLASSES/TicketRepository (Class)
- main.py/FUNCTIONS/main (Function) -> tts/train.py/CLASSES/Train (Class)
- main.py/FUNCTIONS/main (Function) -> tts/train_repository.py/CLASSES/TrainRepository (Class)
- main.py/FUNCTIONS/main (Function) -> tts/train_station.py/CLASSES/TrainStation (Class)
- main.py/FUNCTIONS/main (Function) -> tts/train_station_repository.py/CLASSES/TrainStationRepository (Class)

## Call edges

- main.py/FUNCTIONS/main (Function) -> tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method)
- main.py/FUNCTIONS/main (Function) -> tts/booking_service.py/CLASSES/BookingService/METHODS/cancel_ticket (Method)
- main.py/FUNCTIONS/main (Function) -> tts/booking_service.py/CLASSES/BookingService/METHODS/get_passenger_tickets (Method)
- main.py/FUNCTIONS/main (Function) -> tts/booking_service.py/CLASSES/BookingService/METHODS/search_trains (Method)
- main.py/FUNCTIONS/main (Function) -> tts/passenger_repository.py/CLASSES/PassengerRepository/METHODS/add_passenger (Method)
- main.py/FUNCTIONS/main (Function) -> tts/passenger_repository.py/CLASSES/PassengerRepository/METHODS/get_all_passengers (Method)
- main.py/FUNCTIONS/main (Function) -> tts/reporting_service.py/CLASSES/AdvancedReportingService/METHODS/generate_executive_summary (Method)
- main.py/FUNCTIONS/main (Function) -> tts/route_repository.py/CLASSES/RouteRepository/METHODS/add_route (Method)
- main.py/FUNCTIONS/main (Function) -> tts/route_repository.py/CLASSES/RouteRepository/METHODS/get_all_routes (Method)
- main.py/FUNCTIONS/main (Function) -> tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train_repository.py/CLASSES/TrainRepository/METHODS/add_train (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train_repository.py/CLASSES/TrainRepository/METHODS/get_all_trains (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train_station_repository.py/CLASSES/TrainStationRepository/METHODS/add_station (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train_station_repository.py/CLASSES/TrainStationRepository/METHODS/get_all_stations (Method)
