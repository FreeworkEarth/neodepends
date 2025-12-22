# Hand-Counted Dependencies (TrainTicketSystem_TOY_PYTHON_FIRST)

This folder contains one Markdown file per Python source file with a **manual dependency inventory** to sanity-check NeoDepends output.

## Counting rules (strict, internal-only)

These hand counts are for **internal project dependencies only**:

- “Internal” means the target is defined inside this repo (`main.py` or the `tts/` package).
- **Not counted**: builtins and stdlib (`print`, `len`, `max`, `datetime`, `typing`, `abc`, dict/list methods, etc.).

Dependency kinds:

- `Import` (File -> File): `from tts.x import ...` / `import tts.x` / in-method imports.
- `Extend` (Class -> Class): `class A(B):` where `B` is internal.
- `Create` (Method -> Class): `C(...)` when `C` is an internal class.
- `Call` (Method -> Method): `obj.method(...)` / `super().method(...)` when the target method is internal.
- `Use` (Method -> Field): `self.field` reads/writes for fields owned by that class.
  - Some files also note **optional** “inherited field uses” (e.g. reading `self.name` defined in a base class).

## Files

- `main.md`: the entry point script.
- `tts/*.md`: one file per module under `tts/`.

