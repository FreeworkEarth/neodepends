# `src/tabulator.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 1
- Call: 4
- Use: 4
- Total: 9

## Create edges

- src/tabulator.py/CLASSES/Tabulator/CONSTRUCTORS/__init__ (Constructor) -> src/serializer.py/CLASSES/Serializer (Class)

## Call edges

- src/tabulator.py/CLASSES/Tabulator/METHODS/select_item_to_tabulate (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/tabulator.py/CLASSES/Tabulator/METHODS/select_item_to_tabulate (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/tabulator.py/CLASSES/Tabulator/METHODS/select_item_to_tabulate (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/tabulator.py/CLASSES/Tabulator/METHODS/tabulate_survey (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- src/tabulator.py/CLASSES/Tabulator/CONSTRUCTORS/__init__ (Constructor) -> src/tabulator.py/CLASSES/Tabulator/FIELDS/serializer (Field)
- src/tabulator.py/CLASSES/Tabulator/CONSTRUCTORS/__init__ (Constructor) -> src/tabulator.py/CLASSES/Tabulator/FIELDS/survey_responses (Field)
- src/tabulator.py/CLASSES/Tabulator/METHODS/tabulate_survey (Method) -> src/tabulator.py/CLASSES/Tabulator/FIELDS/serializer (Field)
- src/tabulator.py/CLASSES/Tabulator/METHODS/tabulate_survey (Method) -> src/tabulator.py/CLASSES/Tabulator/FIELDS/survey_responses (Field)
