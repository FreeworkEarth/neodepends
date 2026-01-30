# `matching_question.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 1
- Create: 2
- Call: 36
- Use: 19
- Total: 62

## Import edges

- matching_question.py/module (Module) -> input_handler.py/module (Module)
- matching_question.py/module (Module) -> output_handler.py/module (Module)
- matching_question.py/module (Module) -> question.py/module (Module)
- matching_question.py/module (Module) -> response_correct_answer.py/module (Module)

## Extend edges

- matching_question.py/CLASSES/MatchingQuestion (Class) -> question.py/CLASSES/Question (Class)

## Create edges

- matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> matching_question.py/CLASSES/MatchingQuestion (Class)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- matching_question.py/CLASSES/MatchingQuestion/CONSTRUCTORS/__init__ (Constructor) -> question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/safe_to_split (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/safe_to_split (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_spaced_strings (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/display_tabulation (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/is_valid_answer (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/safe_to_split (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> question.py/CLASSES/Question/METHODS/set_prompt (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> question.py/CLASSES/Question/METHODS/set_user_response (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- matching_question.py/CLASSES/MatchingQuestion/CONSTRUCTORS/__init__ (Constructor) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/CONSTRUCTORS/__init__ (Constructor) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/get_original_pairs (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/get_original_pairs (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/is_valid_answer (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> question.py/CLASSES/Question/FIELDS/prompt (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method) -> matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- matching_question.py/CLASSES/MatchingQuestion/METHODS/tabulate (Method) -> question.py/CLASSES/Question/FIELDS/user_response (Field)
