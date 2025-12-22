# `tts/ticket_booking_system.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 2
- Create: 0
- Call: 5
- Use: 52
- Total: 60

## Import edges

- tts/ticket_booking_system.py/module (Module) -> tts/base_management_system.py/module (Module)

## Extend edges

- tts/ticket_booking_system.py/CLASSES/AdvancedReportingSystem (Class) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem (Class)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem (Class) -> tts/base_management_system.py/CLASSES/BaseManagementSystem (Class)

## Call edges

- tts/ticket_booking_system.py/CLASSES/AdvancedReportingSystem/METHODS/generate_executive_summary (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/export_all_reports (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/calculate_occupancy_rate (Method)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/calculate_revenue (Method)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/analyze_revenue (Method) -> tts/base_management_system.py/CLASSES/BaseManagementSystem/METHODS/log_action (Method)

## Use edges

- tts/ticket_booking_system.py/CLASSES/ReportingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/cached_stats (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/metrics (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/reports (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/calculate_occupancy_rate (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/calculate_occupancy_rate (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/metrics (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/calculate_revenue (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/calculate_revenue (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/metrics (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/clear_cache (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/cached_stats (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/clear_cache (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/metrics (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/export_all_reports (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/metrics (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/export_all_reports (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/reports (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_passenger_report (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_passenger_report (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/reports (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_station_report (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_station_report (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/reports (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/metrics (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_summary (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/reports (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_train_report (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/generate_train_report (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/reports (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/get_popular_routes (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/get_station_traffic (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/booking_system (Field)
- tts/ticket_booking_system.py/CLASSES/ReportingSystem/METHODS/get_station_traffic (Method) -> tts/ticket_booking_system.py/CLASSES/ReportingSystem/FIELDS/cached_stats (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/_initialized (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/passengers (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/routes (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/staff (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/stations (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/CONSTRUCTORS/__init__ (Constructor) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_route (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/routes (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_staff (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/staff (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_station (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/stations (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/add_train (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/analyze_revenue (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/routes (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/display_system_stats (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/passengers (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/display_system_stats (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/routes (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/display_system_stats (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/staff (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/display_system_stats (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/stations (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/display_system_stats (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/find_passenger (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/passengers (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/find_routes (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/routes (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/find_station (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/stations (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/find_train (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_passengers (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/passengers (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_routes (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/routes (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_staff (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/staff (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_stations (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/stations (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_total_capacity (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/get_trains (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/register_passenger (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/passengers (Field)
- tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/METHODS/search_available_trains (Method) -> tts/ticket_booking_system.py/CLASSES/TicketBookingSystem/FIELDS/trains (Field)
