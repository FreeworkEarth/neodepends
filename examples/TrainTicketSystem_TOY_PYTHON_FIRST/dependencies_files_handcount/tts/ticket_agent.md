# `tts/ticket_agent.py`

## Totals (unique edges, internal-only)

- Import: 2
- Extend: 1
- Create: 1
- Call: 4
- Use: 9
- Total: 17

## Import edges

- tts/ticket_agent.py/module (Module) -> tts/staff.py/module (Module)
- tts/ticket_agent.py/module (Module) -> tts/ticket.py/module (Module)

## Extend edges

- tts/ticket_agent.py/CLASSES/TicketAgent (Class) -> tts/staff.py/CLASSES/Staff (Class)

## Create edges

- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/issue_ticket (Method) -> tts/ticket.py/CLASSES/Ticket (Class)

## Call edges

- tts/ticket_agent.py/CLASSES/TicketAgent/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/cancel_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/METHODS/cancel_ticket (Method)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/cancel_ticket (Method) -> tts/ticket.py/CLASSES/Ticket/METHODS/cancel (Method)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/issue_ticket (Method) -> tts/passenger.py/CLASSES/Passenger/METHODS/book_ticket (Method)

## Use edges

- tts/ticket_agent.py/CLASSES/TicketAgent/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/assigned_station (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/tickets_processed (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/cancel_ticket (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/tickets_processed (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/employee_id (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/display_info (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/tickets_processed (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/get_tickets_processed (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/tickets_processed (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/issue_ticket (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/tickets_processed (Field)
- tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/set_assigned_station (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/FIELDS/assigned_station (Field)
