# `src/test_menu.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 3
- Call: 19
- Use: 15
- Total: 38

## Extend edges

- src/test_menu.py/CLASSES/TestMenu (Class) -> src/menu.py/CLASSES/Menu (Class)

## Create edges

- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/grader.py/CLASSES/Grader (Class)
- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/serializer.py/CLASSES/Serializer (Class)
- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/tabulator.py/CLASSES/Tabulator (Class)

## Call edges

- src/test_menu.py/CLASSES/TestMenu/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/create (Method) -> src/survey.py/CLASSES/Survey/METHODS/get_name (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/create (Method) -> src/test.py/CLASSES/Test/METHODS/create (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/display_with_correct_answers (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/modify (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/menu.py/CLASSES/Menu/METHODS/display (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/create (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/display_with_correct_answers (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/grade (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/load (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/modify (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/save (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/tabulate (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/METHODS/take (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/save (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/tabulate (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test_menu.py/CLASSES/TestMenu/METHODS/take (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/grader (Field)
- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- src/test_menu.py/CLASSES/TestMenu/CONSTRUCTORS/__init__ (Constructor) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/tabulator (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/display_with_correct_answers (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/grade (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/grader (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/grade (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/load (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/modify (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/present_menu (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/save (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/save (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/tabulate (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/tabulator (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/take (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/current_test (Field)
- src/test_menu.py/CLASSES/TestMenu/METHODS/take (Method) -> src/test_menu.py/CLASSES/TestMenu/FIELDS/serializer (Field)
