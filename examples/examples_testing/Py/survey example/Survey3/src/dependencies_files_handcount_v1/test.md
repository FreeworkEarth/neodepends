# `test.py`

## Totals (unique edges, internal-only)

- Import: 9
- Extend: 1
- Create: 2
- Call: 36
- Use: 15
- Total: 63

## Import edges

- test.py/module (Module) -> input_handler.py/module (Module)
- test.py/module (Module) -> matching_question.py/module (Module)
- test.py/module (Module) -> multiple_choice_question.py/module (Module)
- test.py/module (Module) -> output_handler.py/module (Module)
- test.py/module (Module) -> question.py/module (Module)
- test.py/module (Module) -> response_correct_answer.py/module (Module)
- test.py/module (Module) -> short_answer_question.py/module (Module)
- test.py/module (Module) -> survey.py/module (Module)
- test.py/module (Module) -> valid_date_question.py/module (Module)

## Extend edges

- test.py/CLASSES/Test (Class) -> survey.py/CLASSES/Survey (Class)

## Create edges

- test.py/CLASSES/Test/METHODS/add_question (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)
- test.py/CLASSES/Test/METHODS/create (Method) -> test.py/CLASSES/Test (Class)

## Call edges

- test.py/CLASSES/Test/CONSTRUCTORS/__init__ (Constructor) -> survey.py/CLASSES/Survey/CONSTRUCTORS/__init__ (Constructor)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> question.py/CLASSES/Question/METHODS/display (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> question.py/CLASSES/Question/METHODS/is_valid_answer (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/set_responses (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> survey.py/CLASSES/Survey/METHODS/add_question (Method)
- test.py/CLASSES/Test/METHODS/add_question (Method) -> test.py/CLASSES/Test/METHODS/add_correct_answer (Method)
- test.py/CLASSES/Test/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- test.py/CLASSES/Test/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- test.py/CLASSES/Test/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- test.py/CLASSES/Test/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/create (Method) -> question.py/CLASSES/Question/METHODS/create (Method)
- test.py/CLASSES/Test/METHODS/create (Method) -> test.py/CLASSES/Test/METHODS/add_question (Method)
- test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> question.py/CLASSES/Question/METHODS/display (Method)
- test.py/CLASSES/Test/METHODS/grade (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/grade (Method) -> question.py/CLASSES/Question/METHODS/get_user_response (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> question.py/CLASSES/Question/METHODS/create (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/delete_responses (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/modify_question (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> survey.py/CLASSES/Survey/METHODS/modify_survey_name (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> test.py/CLASSES/Test/METHODS/add_question (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> test.py/CLASSES/Test/METHODS/modify_correct_answer (Method)
- test.py/CLASSES/Test/METHODS/modify (Method) -> test.py/CLASSES/Test/METHODS/remove_question (Method)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/get_responses (Method)
- test.py/CLASSES/Test/METHODS/remove_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- test.py/CLASSES/Test/METHODS/remove_question (Method) -> survey.py/CLASSES/Survey/METHODS/remove_question (Method)

## Use edges

- test.py/CLASSES/Test/CONSTRUCTORS/__init__ (Constructor) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/add_correct_answer (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- test.py/CLASSES/Test/METHODS/display_with_correct_answers (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/get_correct_answers (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/grade (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- test.py/CLASSES/Test/METHODS/grade (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/modify (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- test.py/CLASSES/Test/METHODS/modify (Method) -> survey.py/CLASSES/Survey/FIELDS/survey_name (Field)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- test.py/CLASSES/Test/METHODS/modify_correct_answer (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/remove_question (Method) -> survey.py/CLASSES/Survey/FIELDS/questions (Field)
- test.py/CLASSES/Test/METHODS/remove_question (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
- test.py/CLASSES/Test/METHODS/set_correct_answers (Method) -> test.py/CLASSES/Test/FIELDS/correct_answers (Field)
