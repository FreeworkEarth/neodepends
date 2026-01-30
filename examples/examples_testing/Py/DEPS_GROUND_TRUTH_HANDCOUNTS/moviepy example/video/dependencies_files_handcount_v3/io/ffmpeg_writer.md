# `io/ffmpeg_writer.py`

## Totals (unique edges, internal-only)

- Import: 0
- Extend: 0
- Create: 1
- Call: 2
- Use: 12
- Total: 15

## Create edges

- io/ffmpeg_writer.py/FUNCTIONS/ffmpeg_write_video (Function) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter (Class)

## Call edges

- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/__exit__ (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/close (Method)
- io/ffmpeg_writer.py/FUNCTIONS/ffmpeg_write_video (Function) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/write_frame (Method)

## Use edges

- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/audio_codec (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/codec (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/ext (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/filename (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/logfile (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/CONSTRUCTORS/__init__ (Constructor) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/proc (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/close (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/proc (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/write_frame (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/codec (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/write_frame (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/ext (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/write_frame (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/filename (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/write_frame (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/logfile (Field)
- io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/METHODS/write_frame (Method) -> io/ffmpeg_writer.py/CLASSES/FFMPEG_VideoWriter/FIELDS/proc (Field)
