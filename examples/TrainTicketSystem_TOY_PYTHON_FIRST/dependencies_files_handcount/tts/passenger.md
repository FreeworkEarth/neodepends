# `tts/passenger.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 1
- Create: 0
- Call: 2
- Use: 14
- Total: 18

## Import edges

- tts/passenger.py/module (Module) -> tts/person.py/module (Module)

## Extend edges

- tts/passenger.py/CLASSES/Passenger (Class) -> tts/person.py/CLASSES/Person (Class)

## Call edges

- tts/passenger.py/CLASSES/Passenger/CONSTRUCTORS/__init__ (Constructor) -> tts/person.py/CLASSES/Person/CONSTRUCTORS/__init__ (Constructor)
- tts/passenger.py/CLASSES/Passenger/METHODS/add_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/METHODS/book_ticket (Method)

## Use edges

- tts/passenger.py/CLASSES/Passenger/CONSTRUCTORS/__init__ (Constructor) -> tts/passenger.py/CLASSES/Passenger/FIELDS/booked_tickets (Field)
- tts/passenger.py/CLASSES/Passenger/CONSTRUCTORS/__init__ (Constructor) -> tts/passenger.py/CLASSES/Passenger/FIELDS/loyalty_points (Field)
- tts/passenger.py/CLASSES/Passenger/CONSTRUCTORS/__init__ (Constructor) -> tts/passenger.py/CLASSES/Passenger/FIELDS/passport_number (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/book_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/booked_tickets (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/book_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/loyalty_points (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/book_ticket (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/cancel_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/booked_tickets (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/cancel_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/loyalty_points (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/booked_tickets (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/loyalty_points (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/id (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/get_booked_tickets (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/booked_tickets (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/get_loyalty_points (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/loyalty_points (Field)
