# `tts/ticket_agent.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 1
- Create: 0
- Call: 1
- Use: 5
- Total: 8

## Import edges

- tts/ticket_agent.py/module (Module) -> tts/staff.py/module (Module)

## Extend edges

- tts/ticket_agent.py/CLASSES/TicketAgent (Class) -> tts/staff.py/CLASSES/Staff (Class)

## Call edges

- tts/ticket_agent.py/CLASSES/TicketAgent/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor)

## Use edges

- tts/ticket_agent.py/CLASSES/TicketAgent/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/assigned_station_id (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/employee_id (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/salary (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/assigned_station_id (Field)
