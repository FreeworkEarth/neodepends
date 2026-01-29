# `src/matching_question.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 2
- Call: 36
- Use: 19
- Total: 58

## Extend edges

- src/matching_question.py/CLASSES/MatchingQuestion (Class) -> src/question.py/CLASSES/Question (Class)

## Create edges

- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> src/matching_question.py/CLASSES/MatchingQuestion (Class)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer (Class)

## Call edges

- src/matching_question.py/CLASSES/MatchingQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/question.py/CLASSES/Question/CONSTRUCTORS/__init__ (Constructor)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/safe_to_split (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/safe_to_split (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/create (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_spaced_strings (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display_tabulation (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/is_valid_answer (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/safe_to_split (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_int_less_than (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/input_handler.py/CLASSES/InputHandler/METHODS/get_console_string (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/question.py/CLASSES/Question/METHODS/set_prompt (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_valid_match_input (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/question.py/CLASSES/Question/METHODS/set_user_response (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/response_correct_answer.py/CLASSES/ResponseCorrectAnswer/METHODS/add_response (Method)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method) -> src/output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)

## Use edges

- src/matching_question.py/CLASSES/MatchingQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/CONSTRUCTORS/__init__ (Constructor) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/add_pair (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/display (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_original_pairs (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/get_original_pairs (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/is_valid_answer (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_pair (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/modify_question (Method) -> src/question.py/CLASSES/Question/FIELDS/prompt (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/obtain_user_response (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/left_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/remove_pair (Method) -> src/matching_question.py/CLASSES/MatchingQuestion/FIELDS/right_matches (Field)
- src/matching_question.py/CLASSES/MatchingQuestion/METHODS/tabulate (Method) -> src/question.py/CLASSES/Question/FIELDS/user_response (Field)
