# `src/survey_menu.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 2
- Call: 16
- Use: 11
- Total: 30

## Extend edges

- src/survey_menu.py/CLASSES/SurveyMenu (Class) -> src/menu.py/CLASSES/Menu (Class)

## Create edges

- src/survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> src/serializer.py/CLASSES/Serializer (Class)
- src/survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> src/tabulator.py/CLASSES/Tabulator (Class)

## Call edges

- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method) -> src/survey.py/CLASSES/Survey/METHODS/create (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method) -> src/survey.py/CLASSES/Survey/METHODS/get_name (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/modify (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/menu.py/CLASSES/Menu/METHODS/display (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/METHODS/load (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/METHODS/modify (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/METHODS/tabulate (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/tabulate (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- src/survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/tabulator (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/load (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/modify (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/tabulate (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/tabulator (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- src/survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method) -> src/survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
