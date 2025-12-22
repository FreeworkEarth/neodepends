# `tts/route.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 0
- Call: 1
- Use: 20
- Total: 21

## Call edges

- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/METHODS/_calculate_fare (Method)

## Use edges

- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/FIELDS/base_fare (Field)
- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/FIELDS/destination (Field)
- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/FIELDS/distance (Field)
- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/FIELDS/intermediate_stops (Field)
- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/FIELDS/origin (Field)
- tts/route.py/CLASSES/Route/CONSTRUCTORS/__init__ (Constructor) -> tts/route.py/CLASSES/Route/FIELDS/route_id (Field)
- tts/route.py/CLASSES/Route/METHODS/_calculate_fare (Method) -> tts/route.py/CLASSES/Route/FIELDS/distance (Field)
- tts/route.py/CLASSES/Route/METHODS/add_intermediate_stop (Method) -> tts/route.py/CLASSES/Route/FIELDS/intermediate_stops (Field)
- tts/route.py/CLASSES/Route/METHODS/display_info (Method) -> tts/route.py/CLASSES/Route/FIELDS/base_fare (Field)
- tts/route.py/CLASSES/Route/METHODS/display_info (Method) -> tts/route.py/CLASSES/Route/FIELDS/destination (Field)
- tts/route.py/CLASSES/Route/METHODS/display_info (Method) -> tts/route.py/CLASSES/Route/FIELDS/distance (Field)
- tts/route.py/CLASSES/Route/METHODS/display_info (Method) -> tts/route.py/CLASSES/Route/FIELDS/intermediate_stops (Field)
- tts/route.py/CLASSES/Route/METHODS/display_info (Method) -> tts/route.py/CLASSES/Route/FIELDS/origin (Field)
- tts/route.py/CLASSES/Route/METHODS/display_info (Method) -> tts/route.py/CLASSES/Route/FIELDS/route_id (Field)
- tts/route.py/CLASSES/Route/METHODS/get_base_fare (Method) -> tts/route.py/CLASSES/Route/FIELDS/base_fare (Field)
- tts/route.py/CLASSES/Route/METHODS/get_destination (Method) -> tts/route.py/CLASSES/Route/FIELDS/destination (Field)
- tts/route.py/CLASSES/Route/METHODS/get_distance (Method) -> tts/route.py/CLASSES/Route/FIELDS/distance (Field)
- tts/route.py/CLASSES/Route/METHODS/get_intermediate_stops (Method) -> tts/route.py/CLASSES/Route/FIELDS/intermediate_stops (Field)
- tts/route.py/CLASSES/Route/METHODS/get_origin (Method) -> tts/route.py/CLASSES/Route/FIELDS/origin (Field)
- tts/route.py/CLASSES/Route/METHODS/get_route_id (Method) -> tts/route.py/CLASSES/Route/FIELDS/route_id (Field)
