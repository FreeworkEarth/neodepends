# `compositing/CompositeVideoClip.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 1
- Create: 6
- Call: 6
- Use: 23
- Total: 36

## Extend edges

- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip (Class) -> VideoClip.py/CLASSES/VideoClip (Class)

## Create edges

- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/ColorClip (Class)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip (Class)
- compositing/CompositeVideoClip.py/FUNCTIONS/clips_array (Function) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip (Class)
- compositing/CompositeVideoClip.py/FUNCTIONS/concatenate_videoclips (Function) -> VideoClip.py/CLASSES/ColorClip (Class)
- compositing/CompositeVideoClip.py/FUNCTIONS/concatenate_videoclips (Function) -> VideoClip.py/CLASSES/VideoClip (Class)
- compositing/CompositeVideoClip.py/FUNCTIONS/concatenate_videoclips (Function) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip (Class)

## Call edges

- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/VideoClip/CONSTRUCTORS/__init__ (Constructor)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> VideoClip.py/CLASSES/VideoClip/METHODS/with_mask (Method)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> VideoClip.py/CLASSES/VideoClip/METHODS/compose_mask (Method)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> VideoClip.py/CLASSES/VideoClip/METHODS/compose_on (Method)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/playing_clips (Method)
- compositing/CompositeVideoClip.py/FUNCTIONS/clips_array (Function) -> VideoClip.py/CLASSES/VideoClip/METHODS/with_position (Method)

## Use edges

- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/audio (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/bg (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/bg_color (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/clips (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/created_bg (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/duration (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/end (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/fps (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/is_mask (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/mask (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/memoize_mask (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/precomputed (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/CONSTRUCTORS/__init__ (Constructor) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/size (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/close (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/audio (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/close (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/bg (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/close (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/created_bg (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/bg (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/is_mask (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/mask (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/memoize_mask (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/precomputed (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/frame_function (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/size (Field)
- compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/METHODS/playing_clips (Method) -> compositing/CompositeVideoClip.py/CLASSES/CompositeVideoClip/FIELDS/clips (Field)
