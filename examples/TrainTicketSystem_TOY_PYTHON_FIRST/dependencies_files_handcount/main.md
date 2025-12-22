# `main.py`

## Totals (unique edges, internal-only)

- Import: 7
- Extend: 0
- Create: 6
- Call: 23
- Use: 0
- Total: 36

## Import edges

- main.py/module (Module) -> tts/passenger.py/module (Module)
- main.py/module (Module) -> tts/route.py/module (Module)
- main.py/module (Module) -> tts/station_manager.py/module (Module)
- main.py/module (Module) -> tts/ticket_agent.py/module (Module)
- main.py/module (Module) -> tts/ticket_booking_system.py/module (Module)
- main.py/module (Module) -> tts/train.py/module (Module)
- main.py/module (Module) -> tts/train_station.py/module (Module)

## Create edges

- main.py/FUNCTIONS/main (Function) -> tts/passenger.py/CLASSES/Passenger (Class)
- main.py/FUNCTIONS/main (Function) -> tts/route.py/CLASSES/Route (Class)
- main.py/FUNCTIONS/main (Function) -> tts/station_manager.py/CLASSES/StationManager (Class)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent (Class)
- main.py/FUNCTIONS/main (Function) -> tts/train.py/CLASSES/Train (Class)
- main.py/FUNCTIONS/main (Function) -> tts/train_station.py/CLASSES/TrainStation (Class)

## Call edges

- main.py/FUNCTIONS/main (Function) -> tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method)
- main.py/FUNCTIONS/main (Function) -> tts/route.py/CLASSES/Route/METHODS/add_intermediate_stop (Method)
- main.py/FUNCTIONS/main (Function) -> tts/route.py/CLASSES/Route/METHODS/get_base_fare (Method)
- main.py/FUNCTIONS/main (Function) -> tts/station_manager.py/CLASSES/StationManager/METHODS/add_train_schedule (Method)
- main.py/FUNCTIONS/main (Function) -> tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method)
- main.py/FUNCTIONS/main (Function) -> tts/station_manager.py/CLASSES/StationManager/METHODS/set_managed_station (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket.py/CLASSES/Ticket/METHODS/display_ticket (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/cancel_ticket (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/issue_ticket (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/set_assigned_station (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_route (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_staff (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_station (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_train (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/display_system_stats (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_instance (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/register_passenger (Method)
- main.py/FUNCTIONS/main (Function) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/search_available_trains (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train.py/CLASSES/Train/METHODS/display_info (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train.py/CLASSES/Train/METHODS/set_route (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train_station.py/CLASSES/TrainStation/METHODS/add_agent (Method)
- main.py/FUNCTIONS/main (Function) -> tts/train_station.py/CLASSES/TrainStation/METHODS/add_train (Method)
