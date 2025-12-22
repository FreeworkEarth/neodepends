# `tts/reporting_service.py`

## Totals (unique edges, internal-only)

- Import: 5
- Extend: 1
- Create: 0
- Call: 4
- Use: 34
- Total: 44

## Import edges

- tts/reporting_service.py/module (Module) -> tts/passenger_repository.py/module (Module)
- tts/reporting_service.py/module (Module) -> tts/route_repository.py/module (Module)
- tts/reporting_service.py/module (Module) -> tts/ticket_repository.py/module (Module)
- tts/reporting_service.py/module (Module) -> tts/train_repository.py/module (Module)
- tts/reporting_service.py/module (Module) -> tts/train_station_repository.py/module (Module)

## Extend edges

- tts/reporting_service.py/CLASSES/AdvancedReportingService (Class) -> tts/reporting_service.py/CLASSES/ReportingService (Class)

## Call edges

- tts/reporting_service.py/CLASSES/AdvancedReportingService/METHODS/generate_executive_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/export_all_reports (Method) -> tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/METHODS/calculate_occupancy_rate (Method)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/METHODS/calculate_revenue (Method)

## Use edges

- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/cached_stats (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/metrics (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/passenger_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/reports (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/route_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/station_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/ticket_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/CONSTRUCTORS/__init__ (Constructor) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/train_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/calculate_occupancy_rate (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/metrics (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/calculate_occupancy_rate (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/train_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/calculate_revenue (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/metrics (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/calculate_revenue (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/ticket_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/clear_cache (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/cached_stats (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/clear_cache (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/metrics (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/export_all_reports (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/metrics (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/export_all_reports (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/reports (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_passenger_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/passenger_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_passenger_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/reports (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_station_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/reports (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_station_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/route_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_station_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/station_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_station_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/train_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/metrics (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/passenger_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/reports (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/route_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/station_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/ticket_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_summary (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/train_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_train_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/reports (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/generate_train_report (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/train_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/get_popular_routes (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/ticket_repo (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/get_station_traffic (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/cached_stats (Field)
- tts/reporting_service.py/CLASSES/ReportingService/METHODS/get_station_traffic (Method) -> tts/reporting_service.py/CLASSES/ReportingService/FIELDS/route_repo (Field)
