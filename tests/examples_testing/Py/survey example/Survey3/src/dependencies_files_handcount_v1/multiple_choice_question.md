# `multiple_choice_question.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 1
- Create: 2
- Call: 24
- Use: 17
- Total: 48

## Import edges

- multiple_choice_question.py/module (Module) -> input_handler.py/module (Module)
- multiple_choice_question.py/module (Module) -> output_handler.py/module (Module)
- multiple_choice_question.py/module (Module) -> question.py/module (Module)
- multiple_choice_question.py/module (Module) -> response_correct_answer.py/module (Module)

## Extend edges

- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion (Class) -> question.py/CLASSES/Question (Class)

## Create edges

- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion (Class)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor) -> question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/set_response_limit (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display_tabulation (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/add_choice (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/is_valid_answer (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> question.py/CLASSES/Question/METHODS/set_prompt (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_multiple_choice_input (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> question.py/CLASSES/Question/METHODS/set_user_response (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/set_response_limit (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/add_choice (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/get_choices (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/get_response_limit (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/is_valid_answer (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/remove_choice (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/set_response_limit (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/tabulate (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/tabulate (Method) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
