# `valid_date_question.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 1
- Create: 2
- Call: 22
- Use: 7
- Total: 36

## Import edges

- valid_date_question.py/module (Module) -> input_handler.py/module (Module)
- valid_date_question.py/module (Module) -> output_handler.py/module (Module)
- valid_date_question.py/module (Module) -> question.py/module (Module)
- valid_date_question.py/module (Module) -> response_correct_answer.py/module (Module)

## Extend edges

- valid_date_question.py/CLASSES/ValidDateQuestion (Class) -> question.py/CLASSES/Question (Class)

## Create edges

- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion (Class)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- valid_date_question.py/CLASSES/ValidDateQuestion/CONSTRUCTORS/__init__ (Constructor) -> question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/set_response_limit (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display_tabulation (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/_is_valid_date (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/is_valid_answer (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/_is_valid_date (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> question.py/CLASSES/Question/METHODS/set_prompt (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/modify_question (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/set_response_limit (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> question.py/CLASSES/Question/METHODS/set_user_response (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_valid_date_input (Method)

## Use edges

- valid_date_question.py/CLASSES/ValidDateQuestion/CONSTRUCTORS/__init__ (Constructor) -> valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/display (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/get_response_limit (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/obtain_user_response (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/set_response_limit (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/FIELDS/response_limit (Field)
- valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/tabulate (Method) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
