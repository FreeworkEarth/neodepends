# `tts/station_manager.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 1
- Create: 0
- Call: 2
- Use: 9
- Total: 13

## Import edges

- tts/station_manager.py/module (Module) -> tts/staff.py/module (Module)

## Extend edges

- tts/station_manager.py/CLASSES/StationManager (Class) -> tts/staff.py/CLASSES/Staff (Class)

## Call edges

- tts/station_manager.py/CLASSES/StationManager/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor)
- tts/station_manager.py/CLASSES/StationManager/METHODS/add_train_schedule (Method) -> tts/train.py/CLASSES/Train/METHODS/get_train_number (Method)

## Use edges

- tts/station_manager.py/CLASSES/StationManager/CONSTRUCTORS/__init__ (Constructor) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/managed_station (Field)
- tts/station_manager.py/CLASSES/StationManager/CONSTRUCTORS/__init__ (Constructor) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/scheduled_trains (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/add_train_schedule (Method) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/scheduled_trains (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/person.py/CLASSES/Person/FIELDS/name (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/employee_id (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/display_info (Method) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/scheduled_trains (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/get_scheduled_trains (Method) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/scheduled_trains (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/remove_train_schedule (Method) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/scheduled_trains (Field)
- tts/station_manager.py/CLASSES/StationManager/METHODS/set_managed_station (Method) -> tts/station_manager.py/CLASSES/StationManager/FIELDS/managed_station (Field)
