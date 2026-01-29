# `test_menu.py`

## Totals (unique edges, internal-only)

- Import: 7
- Extend: 1
- Create: 3
- Call: 19
- Use: 15
- Total: 45

## Import edges

- test_menu.py/module (Module) -> grader.py/module (Module)
- test_menu.py/module (Module) -> input_handler.py/module (Module)
- test_menu.py/module (Module) -> menu.py/module (Module)
- test_menu.py/module (Module) -> output_handler.py/module (Module)
- test_menu.py/module (Module) -> serializer.py/module (Module)
- test_menu.py/module (Module) -> tabulator.py/module (Module)
- test_menu.py/module (Module) -> test.py/module (Module)

## Extend edges

- test_menu.py/CLASSES/TestMenu (Class) -> menu.py/CLASSES/Menu (Class)

## Create edges

- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> grader.py/CLASSES/Grader (Class)
- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> serializer.py/CLASSES/Serializer (Class)
- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> tabulator.py/CLASSES/Tabulator (Class)

## Call edges

- test_menu.py/CLASSES/TestMenu/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/create (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/create (Method) -> test.py/CLASSES/Test/METHODS/create (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/display_with_correct_answers (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/modify (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> menu.py/CLASSES/Menu/METHODS/display (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/create (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/display_with_correct_answers (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/grade (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/load (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/modify (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/save (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/tabulate (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/METHODS/take (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/save (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/tabulate (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test_menu.py/CLASSES/TestMenu/METHODS/take (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> test_menu.py/CLASSES/TestMenu/FIELDS/grader (Field)
- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> test_menu.py/CLASSES/TestMenu/FIELDS/tabulator (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/display_with_correct_answers (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/grade (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/grader (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/grade (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/load (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/modify (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/save (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/save (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/tabulate (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/tabulator (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/take (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- test_menu.py/CLASSES/TestMenu/METHODS/take (Method) -> test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
