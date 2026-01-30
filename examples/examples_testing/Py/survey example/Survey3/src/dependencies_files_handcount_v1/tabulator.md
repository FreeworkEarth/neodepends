# `tabulator.py`

## Totals (unique edges, internal-only)

- Import: 3
- Extend: 0
- Create: 1
- Call: 4
- Use: 4
- Total: 12

## Import edges

- tabulator.py/module (Module) -> input_handler.py/module (Module)
- tabulator.py/module (Module) -> output_handler.py/module (Module)
- tabulator.py/module (Module) -> serializer.py/module (Module)

## Create edges

- tabulator.py/CLASSES/Tabulator/CONSTRUCTORS/__init__ (Constructor) -> serializer.py/CLASSES/Serializer (Class)

## Call edges

- tabulator.py/CLASSES/Tabulator/METHODS/select_item_to_tabulate (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- tabulator.py/CLASSES/Tabulator/METHODS/select_item_to_tabulate (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- tabulator.py/CLASSES/Tabulator/METHODS/select_item_to_tabulate (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- tabulator.py/CLASSES/Tabulator/METHODS/tabulate_survey (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- tabulator.py/CLASSES/Tabulator/CONSTRUCTORS/__init__ (Constructor) -> tabulator.py/CLASSES/Tabulator/FIELDS/serializer (Field)
- tabulator.py/CLASSES/Tabulator/CONSTRUCTORS/__init__ (Constructor) -> tabulator.py/CLASSES/Tabulator/FIELDS/survey_responses (Field)
- tabulator.py/CLASSES/Tabulator/METHODS/tabulate_survey (Method) -> tabulator.py/CLASSES/Tabulator/FIELDS/serializer (Field)
- tabulator.py/CLASSES/Tabulator/METHODS/tabulate_survey (Method) -> tabulator.py/CLASSES/Tabulator/FIELDS/survey_responses (Field)
