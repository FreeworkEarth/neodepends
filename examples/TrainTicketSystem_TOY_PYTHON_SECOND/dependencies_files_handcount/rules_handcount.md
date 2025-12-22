# Handcount Rules (Ground Truth Spec)

Use this document as the **single source of truth** for what we mean by “a dependency” in the TrainTicketSystem_TOY_PYTHON_FIRST Python project.

This is written in a prompt-like format so you can paste it into local LLMs.

---

## Role

You are a “dependency counter” for a small Python codebase.

Your job: produce the exact set of **internal** dependency edges that exist in the code, according to the rules below, and then count them.

---

## Scope

The project root contains:

- `main.py`
- package directory `tts/` with multiple `*.py` modules

Only these files are in-scope. Everything else is out-of-scope.

---

## Entities (nodes)

We model these internal entities:

1) **File**
   - A Python source file (e.g. `tts/ticket_agent.py`, `main.py`)
2) **Class**
   - `class X: ...` defined in a file
3) **Method**
   - A function defined inside a class (`def m(self, ...)`)
4) **Field**
   - Any attribute name assigned to `self.<field>` somewhere in that class’s methods
   - Also include class variables (`ClassName.some_var = ...` or `some_var = ...` inside class body)
5) **Function**
   - A module-level function (e.g. `main()` in `main.py`)

We consider a target “internal” if it is defined in `main.py` or any `tts/*.py` file.

---

## Dependency kinds (categories)

We count these categories (even if we later “collapse” them in the DV8 DSM):

1) `Import` (File -> File)
   - `import tts.x` or `from tts.x import Y`
   - includes imports inside functions/methods
   - maps to module file `tts/x.py`

2) `Extend` (Class -> Class)
   - `class A(B):` where `B` resolves to an internal class

3) `Create` (Method/Function -> Class)
   - `C(...)` where `C` resolves to an internal class (constructor call)

4) `Call` (Method/Function -> Method/Function)
   - `obj.m(...)` where `m` resolves to an internal method or internal function
   - includes `self.m(...)`, `super().m(...)`, and `ClassName.m(...)` (class method call) if resolvable

5) `Use` (Method/Function -> Field)
   - any read/write of `self.<field>` inside a method body where `<field>` is an internal field
   - inherited fields: if `self.name` is defined on a base class inside this project, it counts as `Use` too

---

## Internal-only rule (important)

Do NOT count dependencies to:

- Python builtins (`print`, `len`, `max`, `hasattr`, `isinstance`, etc.)
- stdlib modules (`datetime`, `typing`, `abc`, etc.)
- third-party libraries (none here)

Only count edges where the **target entity is internal** (in this project).

---

## Uniqueness rule (what is “one” dependency?)

We count **unique edges**, not “call sites”.

That means:

- If a function calls `TicketBookingSystem.add_station` 3 times, it is **1** `Call` edge.
- If a method accesses `self.tickets_processed` 10 times, it is **1** `Use` edge.

Uniqueness is by `(source_entity, target_entity, kind)`.

---

## Output requirements

For each file, produce:

1) A list of edges grouped by kind (`Import`, `Extend`, `Create`, `Call`, `Use`)
2) A totals section:
   - `Import: N`
   - `Extend: N`
   - `Create: N`
   - `Call: N`
   - `Use: N`
   - `Total: N` (sum of the above)

Also produce a “full-project” DSM for DV8:

- Use DV8 DSM JSON format (variables + cells).
- Represent each internal entity with a **path-like variable name** so DV8 shows a tree even without a clustering file:
  - `tts/ticket.py/CLASSES/Ticket/METHODS/cancel (Method)`
  - `tts/ticket.py/CLASSES/Ticket/FIELDS/status (Field)`
  - `main.py/FUNCTIONS/main (Function)`
- For DV8, it’s acceptable to **collapse all kinds into `Use`** values (kind is not important right now), but the edge set must match the rules exactly.

---

## Tie-breakers / ambiguity policy

If you cannot resolve a reference to a specific internal entity (because Python is dynamic), do **not** count it.

Examples:

- `passenger.book_ticket(...)`: count only if `passenger` can be resolved to internal class `Passenger`.
- `self.booking_system.get_trains()`: count only if `booking_system` can be resolved to internal class `TicketBookingSystem`.

Prefer “don’t guess” over “overcount”.

