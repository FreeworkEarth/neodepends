# `tools/cuts.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 8
- Call: 2
- Use: 17
- Total: 27

## Create edges

- tools/cuts.py/CLASSES/FramesMatches/METHODS/best (Method) -> tools/cuts.py/CLASSES/FramesMatches (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/filter (Method) -> tools/cuts.py/CLASSES/FramesMatches (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/from_clip (Method) -> tools/cuts.py/CLASSES/FramesMatch (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/from_clip (Method) -> tools/cuts.py/CLASSES/FramesMatches (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/load (Method) -> tools/cuts.py/CLASSES/FramesMatch (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/load (Method) -> tools/cuts.py/CLASSES/FramesMatches (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/select_scenes (Method) -> tools/cuts.py/CLASSES/FramesMatch (Class)
- tools/cuts.py/CLASSES/FramesMatches/METHODS/select_scenes (Method) -> tools/cuts.py/CLASSES/FramesMatches (Class)

## Call edges

- tools/cuts.py/CLASSES/FramesMatch/METHODS/__repr__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/METHODS/__str__ (Method)
- tools/cuts.py/FUNCTIONS/find_video_period (Function) -> io/ffmpeg_reader.py/CLASSES/FFMPEG_VideoReader/METHODS/get_frame (Method)

## Use edges

- tools/cuts.py/CLASSES/FramesMatch/CONSTRUCTORS/__init__ (Constructor) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/end_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/CONSTRUCTORS/__init__ (Constructor) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/max_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/CONSTRUCTORS/__init__ (Constructor) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/min_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/CONSTRUCTORS/__init__ (Constructor) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/start_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/CONSTRUCTORS/__init__ (Constructor) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/time_span (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__eq__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/end_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__eq__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/max_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__eq__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/min_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__eq__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/start_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__iter__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/end_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__iter__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/max_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__iter__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/min_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__iter__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/start_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__str__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/end_time (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__str__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/max_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__str__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/min_distance (Field)
- tools/cuts.py/CLASSES/FramesMatch/METHODS/__str__ (Method) -> tools/cuts.py/CLASSES/FramesMatch/FIELDS/start_time (Field)
