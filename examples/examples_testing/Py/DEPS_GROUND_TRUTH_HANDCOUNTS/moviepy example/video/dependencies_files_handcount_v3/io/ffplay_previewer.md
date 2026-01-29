# `io/ffplay_previewer.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 1
- Call: 2
- Use: 3
- Total: 6

## Create edges

- io/ffplay_previewer.py/FUNCTIONS/ffplay_preview_video (Function) -> io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer (Class)

## Call edges

- io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/METHODS/__exit__ (Method) -> io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/METHODS/close (Method)
- io/ffplay_previewer.py/FUNCTIONS/ffplay_preview_video (Function) -> io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/METHODS/show_frame (Method)

## Use edges

- io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/CONSTRUCTORS/__init__ (Constructor) -> io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/FIELDS/proc (Field)
- io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/METHODS/close (Method) -> io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/FIELDS/proc (Field)
- io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/METHODS/show_frame (Method) -> io/ffplay_previewer.py/CLASSES/FFPLAY_VideoPreviewer/FIELDS/proc (Field)
