# `short_answer_question.py`

## Totals (unique edges, internal-only)

- Import: 2
- Extend: 1
- Create: 1
- Call: 4
- Use: 0
- Total: 8

## Import edges

- short_answer_question.py/module (Module) -> essay_question.py/module (Module)
- short_answer_question.py/module (Module) -> output_handler.py/module (Module)

## Extend edges

- short_answer_question.py/CLASSES/ShortAnswerQuestion (Class) -> essay_question.py/CLASSES/EssayQuestion (Class)

## Create edges

- short_answer_question.py/CLASSES/ShortAnswerQuestion/METHODS/create (Method) -> short_answer_question.py/CLASSES/ShortAnswerQuestion (Class)

## Call edges

- short_answer_question.py/CLASSES/ShortAnswerQuestion/CONSTRUCTORS/__init__ (Constructor) -> essay_question.py/CLASSES/EssayQuestion/CONSTRUCTORS/__init__ (Constructor)
- short_answer_question.py/CLASSES/ShortAnswerQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- short_answer_question.py/CLASSES/ShortAnswerQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- short_answer_question.py/CLASSES/ShortAnswerQuestion/METHODS/display_tabulation (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
