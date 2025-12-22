# `tts/passenger.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 1
- Create: 0
- Call: 1
- Use: 7
- Total: 10

## Import edges

- tts/passenger.py/module (Module) -> tts/person.py/module (Module)

## Extend edges

- tts/passenger.py/CLASSES/Passenger (Class) -> tts/person.py/CLASSES/Person (Class)

## Call edges

- tts/passenger.py/CLASSES/Passenger/CONSTRUCTORS/__init__ (Constructor) -> tts/person.py/CLASSES/Person/CONSTRUCTORS/__init__ (Constructor)

## Use edges

- tts/passenger.py/CLASSES/Passenger/CONSTRUCTORS/__init__ (Constructor) -> tts/passenger.py/CLASSES/Passenger/FIELDS/ticket_ids (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/add_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/ticket_ids (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/passenger.py/CLASSES/Passenger/FIELDS/ticket_ids (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/email (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/id (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/passenger.py/CLASSES/Passenger/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/phone (Field)
