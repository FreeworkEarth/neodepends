# `tts/staff.py`

## Totals (unique edges, internal-only)

- Import: 1
- Extend: 1
- Create: 0
- Call: 1
- Use: 6
- Total: 9

## Import edges

- tts/staff.py/module (Module) -> tts/person.py/module (Module)

## Extend edges

- tts/staff.py/CLASSES/Staff (Class) -> tts/person.py/CLASSES/Person (Class)

## Call edges

- tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor) -> tts/person.py/CLASSES/Person/CONSTRUCTORS/__init__ (Constructor)

## Use edges

- tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/FIELDS/department (Field)
- tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/FIELDS/employee_id (Field)
- tts/staff.py/CLASSES/Staff/CONSTRUCTORS/__init__ (Constructor) -> tts/staff.py/CLASSES/Staff/FIELDS/salary (Field)
- tts/staff.py/CLASSES/Staff/METHODS/get_department (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/department (Field)
- tts/staff.py/CLASSES/Staff/METHODS/get_employee_id (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/employee_id (Field)
- tts/staff.py/CLASSES/Staff/METHODS/get_salary (Method) -> tts/staff.py/CLASSES/Staff/FIELDS/salary (Field)
