# `serializer.py`

## Totals (unique edges, internal-only)

- Import: 4
- Extend: 0
- Create: 0
- Call: 18
- Use: 0
- Total: 22

## Import edges

- serializer.py/module (Module) -> input_handler.py/module (Module)
- serializer.py/module (Module) -> output_handler.py/module (Module)
- serializer.py/module (Module) -> survey.py/module (Module)
- serializer.py/module (Module) -> test.py/module (Module)

## Call edges

- serializer.py/CLASSES/Serializer/METHODS/deserialize_surveys (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_survey (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_survey (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_survey (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_survey (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_test (Method) -> input_handler.py/CLASSES/InputHandler/METHODS/get_console_int (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_test (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_test (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_test (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- serializer.py/CLASSES/Serializer/METHODS/load_test_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/save (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/save (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- serializer.py/CLASSES/Serializer/METHODS/save_survey_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/save_survey_response (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- serializer.py/CLASSES/Serializer/METHODS/save_survey_response (Method) -> survey.py/CLASSES/Survey/METHODS/get_times_taken (Method)
- serializer.py/CLASSES/Serializer/METHODS/save_test_response (Method) -> output_handler.py/CLASSES/OutputHandler/METHODS/output_line (Method)
- serializer.py/CLASSES/Serializer/METHODS/save_test_response (Method) -> survey.py/CLASSES/Survey/METHODS/get_name (Method)
- serializer.py/CLASSES/Serializer/METHODS/save_test_response (Method) -> survey.py/CLASSES/Survey/METHODS/get_times_taken (Method)
