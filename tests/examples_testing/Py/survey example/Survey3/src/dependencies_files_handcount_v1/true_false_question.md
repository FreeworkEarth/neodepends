# `true_false_question.py`

## Totals (unique edges, internal-only)

- Import: 3
- Extend: 1
- Create: 1
- Call: 7
- Use: 0
- Total: 12

## Import edges

- true_false_question.py/module (Module) -> input_handler.py/module (Module)
- true_false_question.py/module (Module) -> multiple_choice_question.py/module (Module)
- true_false_question.py/module (Module) -> output_handler.py/module (Module)

## Extend edges

- true_false_question.py/CLASSES/TrueFalseQuestion (Class) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion (Class)

## Create edges

- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/create (Method) -> true_false_question.py/CLASSES/TrueFalseQuestion (Class)

## Call edges

- true_false_question.py/CLASSES/TrueFalseQuestion/CONSTRUCTORS/__init__ (Constructor) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/CONSTRUCTORS/__init__ (Constructor)
- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_yn_console_input (Method)
- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/modify_question (Method) -> multiple_choice_question.py/CLASSES/MultipleChoiceQuestion/METHODS/display (Method)
- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- true_false_question.py/CLASSES/TrueFalseQuestion/METHODS/modify_question (Method) -> question.py/CLASSES/Question/METHODS/set_prompt (Method)
