# `src/survey.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 2
- Call: 27
- Use: 16
- Total: 45

## Create edges

- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/survey.py/CLASSES/Survey (Class)
- src/survey.py/CLASSES/Survey/METHODS/remove_all_responses (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/question.py/CLASSES/Question/METHODS/create (Method)
- src/survey.py/CLASSES/Survey/METHODS/create (Method) -> src/survey.py/CLASSES/Survey/METHODS/add_question (Method)
- src/survey.py/CLASSES/Survey/METHODS/delete_responses (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/display (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/display (Method) -> src/question.py/CLASSES/Question/METHODS/display (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/question.py/CLASSES/Question/METHODS/create (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/add_question (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/delete_responses (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/modify_question (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/remove_question (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> src/survey.py/CLASSES/Survey/METHODS/get_name (Method)
- src/survey.py/CLASSES/Survey/METHODS/remove_all_responses (Method) -> src/question.py/CLASSES/Question/METHODS/set_user_response (Method)
- src/survey.py/CLASSES/Survey/METHODS/remove_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/take (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/survey.py/CLASSES/Survey/METHODS/take (Method) -> src/question.py/CLASSES/Question/METHODS/obtain_user_response (Method)

## Use edges

- src/survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor) -> src/survey.py/CLASSES/Survey/FIELDS/times_taken (Field)
- src/survey.py/CLASSES/Survey/METHODS/add_question (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/METHODS/display (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/METHODS/display (Method) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/survey.py/CLASSES/Survey/METHODS/get_name (Method) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/survey.py/CLASSES/Survey/METHODS/get_questions (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/METHODS/get_times_taken (Method) -> src/survey.py/CLASSES/Survey/FIELDS/times_taken (Field)
- src/survey.py/CLASSES/Survey/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/survey.py/CLASSES/Survey/METHODS/modify_question (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/survey.py/CLASSES/Survey/METHODS/remove_all_responses (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/METHODS/remove_question (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/survey.py/CLASSES/Survey/METHODS/set_times_taken (Method) -> src/survey.py/CLASSES/Survey/FIELDS/times_taken (Field)
- src/survey.py/CLASSES/Survey/METHODS/take (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
