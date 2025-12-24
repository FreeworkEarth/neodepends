# `src/essay_question.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 2
- Call: 19
- Use: 7
- Total: 29

## Extend edges

- src/essay_question.py/CLASSES/EssayQuestion (Class) -> src/question.py/CLASSES/Question (Class)

## Create edges

- src/essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> src/essay_question.py/CLASSES/EssayQuestion (Class)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- src/essay_question.py/CLASSES/EssayQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> src/essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/display_tabulation (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/modify_question (Method) -> src/question.py/CLASSES/Question/METHODS/set_prompt (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/question.py/CLASSES/Question/METHODS/set_user_response (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- src/essay_question.py/CLASSES/EssayQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method) -> src/essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/display (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/get_response_limit (Method) -> src/essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/obtain_user_response (Method) -> src/essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/set_response_limit (Method) -> src/essay_question.py/CLASSES/EssayQuestion/FIELDS/response_limit (Field)
- src/essay_question.py/CLASSES/EssayQuestion/METHODS/tabulate (Method) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
