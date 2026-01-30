# `src/question.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 0
- Call: 8
- Use: 6
- Total: 14

## Call edges

- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/essay_question.py/CLASSES/EssayQuestion/METHODS/create (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/create (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/short_answer_question.py/CLASSES/ShortAnswerQuestion/METHODS/create (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/create (Method)
- src/question.py/CLASSES/Question/METHODS/create (Method) -> src/valid_date_question.py/CLASSES/ValidDateQuestion/METHODS/create (Method)

## Use edges

- src/question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
- src/question.py/CLASSES/Question/METHODS/get_prompt (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/question.py/CLASSES/Question/METHODS/get_user_response (Method) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
- src/question.py/CLASSES/Question/METHODS/set_prompt (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/question.py/CLASSES/Question/METHODS/set_user_response (Method) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
