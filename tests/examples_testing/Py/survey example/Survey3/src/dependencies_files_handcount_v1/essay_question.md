# `essay_question.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 1
- Create: 2
- Call: 19
- Use: 7
- Total: 33

## Import edges

- essay_question.py/module (Module) -> input_handler.py/module (Module)
- essay_question.py/module (Module) -> output_handler.py/module (Module)
- essay_question.py/module (Module) -> question.py/module (Module)
- essay_question.py/module (Module) -> response_correct_answer.py/module (Module)

## Extend edges

- essay_question.py/CLASSES/EssayQuestion (Class) -> question.py/CLASSES/Question (Class)

## Create edges

- essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> essay_question.py/CLASSES/EssayQuestion (Class)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- essay_question.py/CLASSES/EssayQuestion/CONSTRUCTORS/__init__ (Constructor) -> question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/display_tabulation (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> question.py/CLASSES/Question/METHODS/set_prompt (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> question.py/CLASSES/Question/METHODS/set_user_response (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- essay_question.py/CLASSES/EssayQuestion/CONSTRUCTORS/__init__ (Constructor) -> essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method) -> essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- essay_question.py/CLASSES/EssayQuestion/METHODS/get_response_limit (Method) -> essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method) -> essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- essay_question.py/CLASSES/EssayQuestion/METHODS/tabulate (Method) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
