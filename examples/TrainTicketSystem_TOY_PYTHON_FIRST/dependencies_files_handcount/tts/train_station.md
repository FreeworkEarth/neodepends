# `tts/train_station.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 0
- Call: 1
- Use: 20
- Total: 21

## Call edges

- tts/train_station.py/CLASSES/TrainStation/METHODS/add_agent (Method) -> tts/ticket_agent.py/CLASSES/TicketAgent/METHODS/set_assigned_station (Method)

## Use edges

- tts/train_station.py/CLASSES/TrainStation/CONSTRUCTORS/__init__ (Constructor) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/agents (Field)
- tts/train_station.py/CLASSES/TrainStation/CONSTRUCTORS/__init__ (Constructor) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/available_trains (Field)
- tts/train_station.py/CLASSES/TrainStation/CONSTRUCTORS/__init__ (Constructor) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/city (Field)
- tts/train_station.py/CLASSES/TrainStation/CONSTRUCTORS/__init__ (Constructor) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/name (Field)
- tts/train_station.py/CLASSES/TrainStation/CONSTRUCTORS/__init__ (Constructor) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/station_code (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/__eq__ (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/station_code (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/__hash__ (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/station_code (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/add_agent (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/agents (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/add_train (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/available_trains (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/display_info (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/agents (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/display_info (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/available_trains (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/display_info (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/city (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/display_info (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/name (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/display_info (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/station_code (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/get_agents (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/agents (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/get_city (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/city (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/get_name (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/name (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/get_station_code (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/station_code (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/remove_train (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/available_trains (Field)
- tts/train_station.py/CLASSES/TrainStation/METHODS/search_trains (Method) -> tts/train_station.py/CLASSES/TrainStation/FIELDS/available_trains (Field)
