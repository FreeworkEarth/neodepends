# `src/test.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 2
- Call: 36
- Use: 15
- Total: 54

## Extend edges

- src/test.py/CLASSES/Test (Class) -> src/survey.py/CLASSES/Survey (Class)

## Create edges

- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/test.py/CLASSES/Test (Class)

## Call edges

- src/test.py/CLASSES/Test/CONSTRUCTORS/__init__ (Constructor) -> src/survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/question.py/CLASSES/Question/METHODS/display (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/question.py/CLASSES/Question/METHODS/is_valid_answer (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/set_responses (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/survey.py/CLASSES/Survey/METHODS/add_question (Method)
- src/test.py/CLASSES/Test/METHODS/add_question (Method) -> src/test.py/CLASSES/Test/METHODS/add_correct_answer (Method)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/question.py/CLASSES/Question/METHODS/create (Method)
- src/test.py/CLASSES/Test/METHODS/create (Method) -> src/test.py/CLASSES/Test/METHODS/add_question (Method)
- src/test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> src/question.py/CLASSES/Question/METHODS/display (Method)
- src/test.py/CLASSES/Test/METHODS/grade (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/grade (Method) -> src/question.py/CLASSES/Question/METHODS/get_user_response (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/question.py/CLASSES/Question/METHODS/create (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/delete_responses (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/modify_question (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/test.py/CLASSES/Test/METHODS/add_question (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/test.py/CLASSES/Test/METHODS/remove_question (Method)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/get_responses (Method)
- src/test.py/CLASSES/Test/METHODS/remove_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/test.py/CLASSES/Test/METHODS/remove_question (Method) -> src/survey.py/CLASSES/Survey/METHODS/remove_question (Method)

## Use edges

- src/test.py/CLASSES/Test/CONSTRUCTORS/__init__ (Constructor) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/add_correct_answer (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/get_correct_answers (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/grade (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/test.py/CLASSES/Test/METHODS/grade (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/test.py/CLASSES/Test/METHODS/modify (Method) -> src/survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/remove_question (Method) -> src/survey.py/CLASSES/Survey/FIELDS/questions (Field)
- src/test.py/CLASSES/Test/METHODS/remove_question (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- src/test.py/CLASSES/Test/METHODS/set_correct_answers (Method) -> src/test.py/CLASSES/Test/FIELDS/correct_answers (Field)
