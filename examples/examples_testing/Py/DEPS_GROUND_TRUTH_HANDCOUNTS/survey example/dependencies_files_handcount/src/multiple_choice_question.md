# `src/multiple_choice_question.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 2
- Call: 24
- Use: 17
- Total: 44

## Extend edges

- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion (Class) -> src/question.py/CLASSES/Question (Class)

## Create edges

- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion (Class)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/set_response_limit (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display_tabulation (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/add_choice (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/is_valid_answer (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/question.py/CLASSES/Question/METHODS/set_prompt (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_multiple_choice_input (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/question.py/CLASSES/Question/METHODS/set_user_response (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/set_response_limit (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/add_choice (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/get_choices (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/get_response_limit (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/is_valid_answer (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/modify_question (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/obtain_user_response (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/remove_choice (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/set_response_limit (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/response_limit (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/tabulate (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/FIELDS/choices (Field)
- src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/tabulate (Method) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
