# `survey.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 0
- Create: 2
- Call: 27
- Use: 16
- Total: 49

## Import edges

- survey.py/module (Module) -> input_handler.py/module (Module)
- survey.py/module (Module) -> output_handler.py/module (Module)
- survey.py/module (Module) -> question.py/module (Module)
- survey.py/module (Module) -> response_correct_answer.py/module (Module)

## Create edges

- survey.py/CLASSES/Survey/METHODS/create (Method) -> survey.py/CLASSES/Survey (Class)
- survey.py/CLASSES/Survey/METHODS/remove_all_responses (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- survey.py/CLASSES/Survey/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- survey.py/CLASSES/Survey/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- survey.py/CLASSES/Survey/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- survey.py/CLASSES/Survey/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/create (Method) -> question.py/CLASSES/Question/METHODS/create (Method)
- survey.py/CLASSES/Survey/METHODS/create (Method) -> survey.py/CLASSES/Survey/METHODS/add_question (Method)
- survey.py/CLASSES/Survey/METHODS/delete_responses (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/display (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/display (Method) -> question.py/CLASSES/Question/METHODS/display (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> question.py/CLASSES/Question/METHODS/create (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/add_question (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/delete_responses (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/modify_question (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/remove_question (Method)
- survey.py/CLASSES/Survey/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- survey.py/CLASSES/Survey/METHODS/remove_all_responses (Method) -> question.py/CLASSES/Question/METHODS/set_user_response (Method)
- survey.py/CLASSES/Survey/METHODS/remove_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/take (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- survey.py/CLASSES/Survey/METHODS/take (Method) -> question.py/CLASSES/Question/METHODS/obtain_user_response (Method)

## Use edges

- survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor) -> survey.py/CLASSES/Survey/FIELDS/times_taken (Field)
- survey.py/CLASSES/Survey/METHODS/add_question (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/METHODS/display (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/METHODS/display (Method) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- survey.py/CLASSES/Survey/METHODS/get_name (Method) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- survey.py/CLASSES/Survey/METHODS/get_questions (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/METHODS/get_times_taken (Method) -> survey.py/CLASSES/Survey/FIELDS/times_taken (Field)
- survey.py/CLASSES/Survey/METHODS/modify (Method) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- survey.py/CLASSES/Survey/METHODS/modify_question (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- survey.py/CLASSES/Survey/METHODS/remove_all_responses (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/METHODS/remove_question (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- survey.py/CLASSES/Survey/METHODS/set_times_taken (Method) -> survey.py/CLASSES/Survey/FIELDS/times_taken (Field)
- survey.py/CLASSES/Survey/METHODS/take (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
