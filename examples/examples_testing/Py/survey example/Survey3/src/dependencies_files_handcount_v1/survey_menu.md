# `survey_menu.py`

## Totals (unique edges, internal-only)

- Import: 6
- Extend: 1
- Create: 2
- Call: 16
- Use: 11
- Total: 36

## Import edges

- survey_menu.py/module (Module) -> input_handler.py/module (Module)
- survey_menu.py/module (Module) -> menu.py/module (Module)
- survey_menu.py/module (Module) -> output_handler.py/module (Module)
- survey_menu.py/module (Module) -> serializer.py/module (Module)
- survey_menu.py/module (Module) -> survey.py/module (Module)
- survey_menu.py/module (Module) -> tabulator.py/module (Module)

## Extend edges

- survey_menu.py/CLASSES/SurveyMenu (Class) -> menu.py/CLASSES/Menu (Class)

## Create edges

- survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> serializer.py/CLASSES/Serializer (Class)
- survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> tabulator.py/CLASSES/Tabulator (Class)

## Call edges

- survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method) -> survey.py/CLASSES/Survey/METHODS/create (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/modify (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> menu.py/CLASSES/Menu/METHODS/display (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/create (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/load (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/modify (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/tabulate (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/tabulate (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
- survey_menu.py/CLASSES/SurveyMenu/CONSTRUCTORS/__init__ (Constructor) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/tabulator (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/load (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/modify (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/present_menu (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/save (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/tabulate (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/tabulator (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/current_survey (Field)
- survey_menu.py/CLASSES/SurveyMenu/METHODS/take (Method) -> survey_menu.py/CLASSES/SurveyMenu/FIELDS/serializer (Field)
