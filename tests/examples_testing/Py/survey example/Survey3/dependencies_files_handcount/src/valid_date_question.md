# `src/valid_date_question.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 2
- Call: 22
- Use: 7
- Total: 32

## Extend edges

- src/valid_date_question.py/CLASSES/ValidDateQuestion (Class) -> src/question.py/CLASSES/Question (Class)

## Create edges

- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion (Class)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- src/valid_date_question.py/CLASSES/ValidDateQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/set_response_limit (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display_tabulation (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/_is_valid_date (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/is_valid_answer (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/_is_valid_date (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/question.py/CLASSES/Question/METHODS/set_prompt (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/set_response_limit (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/question.py/CLASSES/Question/METHODS/set_user_response (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method)

## Use edges

- src/valid_date_question.py/CLASSES/ValidDateQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_response_limit (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/set_response_limit (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/tabulate (Method) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
