# `tools/credits.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 4
- Call: 3
- Use: 1
- Total: 9

## Extend edges

- tools/credits.py/CLASSES/CreditsClip (Class) -> VideoClip.py/CLASSES/TextClip (Class)

## Create edges

- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/ImageClip (Class)
- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/TextClip (Class)
- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip (Class)
- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> fx/Resize.py/CLASSES/Resize (Class)

## Call edges

- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/TextClip/CONSTRUCTORS/__init__ (Constructor)
- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/VideoClip/METHODS/with_position (Method)
- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_reader.py/CLASSES/FFMPEG_VideoReader/METHODS/get_frame (Method)

## Use edges

- tools/credits.py/CLASSES/CreditsClip/CONSTRUCTORS/__init__ (Constructor) -> tools/credits.py/CLASSES/CreditsClip/FIELDS/mask (Field)
