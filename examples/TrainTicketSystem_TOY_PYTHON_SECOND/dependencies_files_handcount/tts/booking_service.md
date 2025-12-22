# `tts/booking_service.py`

## Totals (unique edges, internal-only)

- Import: 6
- Extend: 0
- Create: 1
- Call: 4
- Use: 13
- Total: 24

## Import edges

- tts/booking_service.py/module (Module) -> tts/passenger_repository.py/module (Module)
- tts/booking_service.py/module (Module) -> tts/route_repository.py/module (Module)
- tts/booking_service.py/module (Module) -> tts/ticket.py/module (Module)
- tts/booking_service.py/module (Module) -> tts/ticket_repository.py/module (Module)
- tts/booking_service.py/module (Module) -> tts/train_repository.py/module (Module)
- tts/booking_service.py/module (Module) -> tts/train_station_repository.py/module (Module)

## Create edges

- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/ticket.py/CLASSES/Ticket (Class)

## Call edges

- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/METHODS/add_ticket (Method)
- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/train.py/CLASSES/Train/METHODS/book_seat (Method)
- tts/booking_service.py/CLASSES/BookingService/METHODS/cancel_ticket (Method) -> tts/ticket.py/CLASSES/Ticket/METHODS/cancel (Method)
- tts/booking_service.py/CLASSES/BookingService/METHODS/cancel_ticket (Method) -> tts/train.py/CLASSES/Train/METHODS/cancel_seat (Method)

## Use edges

- tts/booking_service.py/CLASSES/BookingService/CONSTRUCTORS/__init__ (Constructor) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/passenger_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/CONSTRUCTORS/__init__ (Constructor) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/route_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/CONSTRUCTORS/__init__ (Constructor) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/station_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/CONSTRUCTORS/__init__ (Constructor) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/ticket_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/CONSTRUCTORS/__init__ (Constructor) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/train_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/passenger_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/route_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/ticket_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/book_ticket (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/train_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/cancel_ticket (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/ticket_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/cancel_ticket (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/train_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/get_passenger_tickets (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/ticket_repo (Field)
- tts/booking_service.py/CLASSES/BookingService/METHODS/search_trains (Method) -> tts/booking_service.py/CLASSES/BookingService/FIELDS/train_repo (Field)
