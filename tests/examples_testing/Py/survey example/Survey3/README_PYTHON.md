# Survey System - Python Version

This is a Python conversion of the Java Survey System originally created by Joe Halcisak for SE310 - Spring 2023.

## Overview

A console-based application for creating and managing surveys and tests. The system supports multiple question types, response collection, tabulation, and automatic grading for tests.

## Features

### Question Types
- **True/False** - Simple binary choice questions
- **Multiple Choice** - Single or multiple correct answers
- **Short Answer** - Text responses with tabulation
- **Essay** - Free-form text responses (ungraded)
- **Valid Date** - Date format validation (MM-DD-YYYY)
- **Matching** - Match left items to right items

### Survey Operations
- Create surveys with 1-50 questions
- Display surveys
- Save/Load surveys (serialized to `.survey` files)
- Take surveys (collects and saves responses)
- Modify surveys (name, questions, add/delete questions)
- Tabulate responses (aggregates and displays statistics)

### Test Operations
All survey features, plus:
- Store correct answers for each question
- Display tests with or without correct answers
- Auto-grade responses (calculates scores, excludes essay questions)
- Modify correct answers

## Installation

No external dependencies required! This project uses only Python standard library modules.

```bash
# Python 3.6+ required
python3 --version
```

## Usage

Run the main application:

```bash
python3 src/main.py
```

Or from the src directory:

```bash
cd src
python3 main.py
```

## File Structure

```
Survey3/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Entry point
│   ├── input_handler.py           # Console input handling
│   ├── output_handler.py          # Console output formatting
│   ├── question.py                # Abstract base class
│   ├── survey.py                  # Survey class
│   ├── test.py                    # Test class (extends Survey)
│   ├── response_correct_answer.py # Response data structure
│   ├── serializer.py              # File I/O and serialization
│   ├── tabulator.py              # Response tabulation
│   ├── grader.py                 # Test grading
│   ├── menu.py                   # Base menu class
│   ├── survey_menu.py            # Survey menu
│   ├── test_menu.py              # Test menu
│   ├── true_false_question.py
│   ├── multiple_choice_question.py
│   ├── short_answer_question.py
│   ├── essay_question.py
│   ├── valid_date_question.py
│   └── matching_question.py
├── outputs/                      # Generated files
│   ├── surveys/                  # Saved surveys (.survey files)
│   ├── tests/                    # Saved tests (.test files)
│   └── responses/               # Response files (.response files)
├── requirements.txt
└── README_PYTHON.md
```

## Data Persistence

The system uses Python's `pickle` module for serialization:

- **Surveys** → `outputs/surveys/{name}.survey`
- **Tests** → `outputs/tests/{name}.test`
- **Responses** → `outputs/responses/{surveyOrTestName}/{name}-resp-{number}.response`

## Example Workflow

1. Start the application
2. Choose "Survey" or "Test"
3. Create a new survey/test
4. Add questions (choose from 6 types)
5. Save the survey/test
6. Take the survey/test (responses saved automatically)
7. For surveys: Tabulate responses
8. For tests: Grade responses and view scores

## Differences from Java Version

- Uses Python's `pickle` instead of Java serialization
- Python naming conventions (snake_case instead of camelCase)
- Uses Python's `os` module for file operations
- Uses `datetime` module for date validation
- No need for explicit type declarations
- Uses Python's abstract base classes (ABC) for abstract classes

## Notes

- The `outputs/` directory will be created automatically when saving surveys/tests/responses
- Example surveys and tests from the Java version can be loaded if they were serialized in a compatible format (may require re-creation)
- All user input is validated before processing
- Response files are automatically numbered sequentially

