# `question.py`

## Totals (unique edges, internal-only)

- Import: 8
- Extend: 0
- Create: 0
- Call: 8
- Use: 6
- Total: 22

## Import edges

- question.py/module (Module) -> essay_question.py/module (Module)
- question.py/module (Module) -> input_handler.py/module (Module)
- question.py/module (Module) -> matching_question.py/module (Module)
- question.py/module (Module) -> multiple_choice_question.py/module (Module)
- question.py/module (Module) -> output_handler.py/module (Module)
- question.py/module (Module) -> short_answer_question.py/module (Module)
- question.py/module (Module) -> true_false_question.py/module (Module)
- question.py/module (Module) -> valid_date_question.py/module (Module)

## Call edges

- question.py/CLASSES/Question/METHODS/create (Method) -> essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> short_answer_question.py/CLASSES/ShortAnswerQuestion/METHODS/create (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/create (Method)
- question.py/CLASSES/Question/METHODS/create (Method) -> valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method)

## Use edges

- question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
- question.py/CLASSES/Question/METHODS/get_prompt (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- question.py/CLASSES/Question/METHODS/get_user_response (Method) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
- question.py/CLASSES/Question/METHODS/set_prompt (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- question.py/CLASSES/Question/METHODS/set_user_response (Method) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
