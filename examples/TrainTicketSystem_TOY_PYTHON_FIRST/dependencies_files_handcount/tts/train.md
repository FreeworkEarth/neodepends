# `tts/train.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 0
- Call: 3
- Use: 21
- Total: 24

## Call edges

- tts/train.py/CLASSES/Train/METHODS/available_seats (Method) -> tts/train.py/CLASSES/Train/METHODS/get_available_seats (Method)
- tts/train.py/CLASSES/Train/METHODS/book_seat (Method) -> tts/train.py/CLASSES/Train/METHODS/is_seat_available (Method)
- tts/train.py/CLASSES/Train/METHODS/display_info (Method) -> tts/train.py/CLASSES/Train/METHODS/get_available_seats (Method)

## Use edges

- tts/train.py/CLASSES/Train/CONSTRUCTORS/__init__ (Constructor) -> tts/train.py/CLASSES/Train/FIELDS/booked_seats (Field)
- tts/train.py/CLASSES/Train/CONSTRUCTORS/__init__ (Constructor) -> tts/train.py/CLASSES/Train/FIELDS/route (Field)
- tts/train.py/CLASSES/Train/CONSTRUCTORS/__init__ (Constructor) -> tts/train.py/CLASSES/Train/FIELDS/total_seats (Field)
- tts/train.py/CLASSES/Train/CONSTRUCTORS/__init__ (Constructor) -> tts/train.py/CLASSES/Train/FIELDS/train_name (Field)
- tts/train.py/CLASSES/Train/CONSTRUCTORS/__init__ (Constructor) -> tts/train.py/CLASSES/Train/FIELDS/train_number (Field)
- tts/train.py/CLASSES/Train/CONSTRUCTORS/__init__ (Constructor) -> tts/train.py/CLASSES/Train/FIELDS/type (Field)
- tts/train.py/CLASSES/Train/METHODS/book_seat (Method) -> tts/train.py/CLASSES/Train/FIELDS/booked_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/display_info (Method) -> tts/train.py/CLASSES/Train/FIELDS/route (Field)
- tts/train.py/CLASSES/Train/METHODS/display_info (Method) -> tts/train.py/CLASSES/Train/FIELDS/total_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/display_info (Method) -> tts/train.py/CLASSES/Train/FIELDS/train_name (Field)
- tts/train.py/CLASSES/Train/METHODS/display_info (Method) -> tts/train.py/CLASSES/Train/FIELDS/train_number (Field)
- tts/train.py/CLASSES/Train/METHODS/display_info (Method) -> tts/train.py/CLASSES/Train/FIELDS/type (Field)
- tts/train.py/CLASSES/Train/METHODS/get_available_seats (Method) -> tts/train.py/CLASSES/Train/FIELDS/booked_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/get_available_seats (Method) -> tts/train.py/CLASSES/Train/FIELDS/total_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/get_route (Method) -> tts/train.py/CLASSES/Train/FIELDS/route (Field)
- tts/train.py/CLASSES/Train/METHODS/get_total_seats (Method) -> tts/train.py/CLASSES/Train/FIELDS/total_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/get_train_name (Method) -> tts/train.py/CLASSES/Train/FIELDS/train_name (Field)
- tts/train.py/CLASSES/Train/METHODS/get_train_number (Method) -> tts/train.py/CLASSES/Train/FIELDS/train_number (Field)
- tts/train.py/CLASSES/Train/METHODS/is_seat_available (Method) -> tts/train.py/CLASSES/Train/FIELDS/booked_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/release_seat (Method) -> tts/train.py/CLASSES/Train/FIELDS/booked_seats (Field)
- tts/train.py/CLASSES/Train/METHODS/set_route (Method) -> tts/train.py/CLASSES/Train/FIELDS/route (Field)
