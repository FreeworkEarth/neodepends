# `main.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 0
- Create: 2
- Call: 4
- Use: 0
- Total: 10

## Import edges

- main.py/module (Module) -> input_handler.py/module (Module)
- main.py/module (Module) -> output_handler.py/module (Module)
- main.py/module (Module) -> survey_menu.py/module (Module)
- main.py/module (Module) -> test_menu.py/module (Module)

## Create edges

- main.py/FUNCTIONS/main (Function) -> survey_menu.py/CLASSES/SurveyMenu (Class)
- main.py/FUNCTIONS/main (Function) -> test_menu.py/CLASSES/TestMenu (Class)

## Call edges

- main.py/FUNCTIONS/main (Function) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- main.py/FUNCTIONS/main (Function) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- main.py/FUNCTIONS/main (Function) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method)
- main.py/FUNCTIONS/main (Function) -> test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method)
