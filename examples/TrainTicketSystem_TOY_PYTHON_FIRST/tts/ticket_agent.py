"""
TicketAgent - COUPLED to TrainStation, Passenger, Route, Train, Ticket
Creates bidirectional dependency with TrainStation

NOTE: HAND COUNT BELOW CODE: The hand-count for the 4 dependency types in your TicketAgent snippet, using the usual “one dependency edge per (source method → target thing)” interpretation.

"""

from tts.staff import Staff


class TicketAgent(Staff):
    """TicketAgent with high coupling - BAD DESIGN!"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float):
        super().__init__(name, person_id, email, phone, employee_id, salary, "Ticketing")
        self.tickets_processed = 0
        self.assigned_station = None

    def set_assigned_station(self, station) -> None:
        self.assigned_station = station

    def issue_ticket(self, passenger, route, train, seat_number: str, price: float):
        from tts.ticket import Ticket

        ticket = Ticket(passenger, route, train, seat_number, price)
        passenger.book_ticket(ticket)
        self.tickets_processed += 1
        return ticket

    def cancel_ticket(self, passenger, ticket) -> None:
        passenger.cancel_ticket(ticket)
        ticket.cancel()
        self.tickets_processed += 1

    def get_tickets_processed(self) -> int:
        return self.tickets_processed

    def perform_duties(self) -> None:
        print("Processing ticket bookings and cancellations")

    def display_info(self):
        print(f"Ticket Agent: {self.name}")
        print(f"Employee ID: {self.employee_id}")
        print(f"Tickets Processed: {self.tickets_processed}")




"""
TicketAgent dependency inventory (manual, “keep everything”)

A) Imports / module coupling
- ticket_agent.py -> tts.staff (via `from tts.staff import Staff`)
- TicketAgent.issue_ticket -> tts.ticket (via `from tts.ticket import Ticket` inside the method)

Imports specifically:
NeoDepends can represent Import (DepKind::Import exists), but in your TicketAgent runs imports often show up indirectly as Extend/Use/Call to Staf

B) Inheritance
- TicketAgent -> Staff  (Extend)

C) Object creation
- TicketAgent.issue_ticket -> Ticket  (Create)  # `Ticket(...)`

D) Calls (method/function calls)
Domain/object calls (4):
- TicketAgent.__init__ -> Staff.__init__        # `super().__init__(...)`
- TicketAgent.issue_ticket -> Passenger.book_ticket
- TicketAgent.cancel_ticket -> Passenger.cancel_ticket
- TicketAgent.cancel_ticket -> Ticket.cancel

Builtin calls (4):
- TicketAgent.perform_duties -> print
- TicketAgent.display_info -> print  (3 call sites)

Total call sites = 8 (domain-only = 4)

E) Field reads/writes (self.<field> accesses)
Fields declared in TicketAgent (7 “method -> field” edges):
- __init__ -> tickets_processed (write)
- __init__ -> assigned_station (write)
- set_assigned_station -> assigned_station (write)
- issue_ticket -> tickets_processed (write via +=)
- cancel_ticket -> tickets_processed (write via +=)
- get_tickets_processed -> tickets_processed (read)
- display_info -> tickets_processed (read)

Inherited fields (2 “method -> field” edges; these live in base classes):
- display_info -> name (read)
- display_info -> employee_id (read)

Total field-use edges = 9 (7 local + 2 inherited)

Notes:
- Parameters imply type coupling (Passenger/Route/Train/Ticket/TrainStation), but in dynamic Python
  those types may not resolve unless the analyzer chooses to model “type-use” edges.


  Which NeoDepends flags include these (or not)?

Entity extraction (Class/Method/Field spans): built-in per-language.

Uses languages/python/tags.scm (you now have this in neodepends).
--file-level turns this OFF (everything collapses to one File entity).
Dependency resolution source:

-D/--depends: this is what can produce Call/Create/Extend/... style edges.
-S/--stackgraphs: in this codebase it effectively emits Use-style reference→definition edges (not Call/Create/Extend).
If you pass both, order matters (the one that appears first on the command line wins for that language).

Imports specifically:

NeoDepends can represent Import (DepKind::Import exists), but in your TicketAgent runs imports often show up indirectly as Extend/Use/Call to Staff/Ticket rather than explicit Import edges.
Method→Field edges (self.tickets_processed, etc.):

Still mainly come from your postprocessing script enhance_python_deps.py (the wrapper runs it as “Python enhancement”), even with the new tags.scm.
tags.scm helps by ensuring the Field entities exist; the enhancement creates the Use edges and fixes Field parenting/dedup.
print(...) calls:

Not reliably produced by current NeoDepends resolvers; so they’re in the manual “max” count, but may not appear in the DB without adding a new extraction rule.
"""