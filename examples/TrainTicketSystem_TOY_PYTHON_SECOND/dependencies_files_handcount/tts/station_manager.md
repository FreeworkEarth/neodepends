# `tts/station_manager.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 1
- Create: 0
- Call: 1
- Use: 5
- Total: 8

## Import edges

- tts/station_manager.py/module (Module) -> tts/staff.py/module (Module)

## Extend edges

- tts/station_manager.py/CLASSES/StationManager (Class) -> tts/staff.py/CLASSES/Staff (Class)

## Call edges

- tts/station_manager.py/CLASSES/StationManager/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor)

## Use edges

- tts/station_manager.py/CLASSES/StationManager/CONSTRUCTORS/__init__ (Constructor) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/managed_station_id (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/employee_id (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/salary (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/managed_station_id (Field)
