# NeoDepends Python Dependencies

This document describes the dependency kinds NeoDepends emits for Python, and how the enhancement step expands the raw extraction.

## Core dependency kinds (DV8/DSM)

- **Import**
  - File/module imports another module.
- **Extend**
  - Class inherits from another class.
- **Create**
  - A method/function instantiates a class (e.g., `ClassName(...)`).
- **Call**
  - A method/function calls another method/function.
- **Use**
  - A method/function accesses a field/attribute.
- **Override**
  - A concrete method implements an abstract method from a base class.

These are the kinds used in handcount comparisons and the exported DV8 DSMs.

## Enhancement step (Python)

The Python enhancement step (`tools/enhance_python_deps.py`) adds dependencies that are not captured by raw extraction alone. It focuses on structural dependencies that are important for architectural analysis and handcount alignment.

### 1) Method -> Field (Use)
Detects `self.field` access inside methods and records it as a **Use** edge:

- `Class.method -> Class.field (Use)`

This is critical for clustering and architectural signal.

### 2) Field -> Field (Use)  **(new)**
When a field is defined in terms of another field (for example, `self.a = self.b` or `self.a = self.b + 1`), we add a **Use** edge between fields:

- `Class.field_a -> Class.field_b (Use)`

This captures intra-class data dependencies that otherwise disappear after field-parent normalization.

### 3) Method -> Function (Call)  **(new)**
For module-level functions called inside methods, we add a **Call** edge:

- `Class.method -> module.function (Call)`

Previously only function->function calls were guaranteed; now method->function calls are explicit.

### 4) Override detection (abstract methods)
If a base class defines abstract methods (ABC), and a subclass implements them, we add **Override** edges:

- `Subclass.method -> BaseClass.method (Override)`

This is equivalent to Java `@Override` semantics for Python ABCs.

### 5) Structural field type inference  (Field → Class Use)

Python's duck typing means a class can store another class's object in a field without any
import, type annotation, or explicit reference at the use-site. The field type is only
revealed at runtime when the object is injected. Example from the toy project:

```python
# ticket.py — no import of Passenger, Route, or Train
class Ticket:
    def __init__(self, passenger, route, train, seat_number: str, price: float):
        self.passenger = passenger   # holds a Passenger object — but no annotation
        self.route = route           # holds a Route object
        self.train = train           # holds a Train object
```

These structural couplings are real architectural dependencies (renaming `Passenger` would
break `ticket.py`), but are invisible to import-graph or annotation-only analyzers.

The enhancement step uses four inference patterns to recover these edges:

#### Pattern 1: PEP-526 annotated field assignment (`visit_AnnAssign`)

```python
self.route: Route = route           # direct annotation
self.trains: List[Train] = []       # subscript annotation  (List[X] / Optional[X])
self.stop: "TrainStation" = None    # forward-reference string
```

When a field assignment inside a method body carries a type annotation, and that type name
matches a known internal class, the type is recorded with zero FP risk — only literal class
names from the project's own class index can match.

#### Pattern 2: Setter / constructor — `self.field = param` (name convention)

For every method (not just `__init__`), if:
- `self.field = param` assigns a parameter directly to a field, and
- the parameter name matches a known class via `_match_param_to_class()`

then the field is inferred to hold that class type. Covers setter methods too:

```python
def set_route(self, route):
    self.route = route   # 'route' → Route  (case-insensitive exact match)

def set_managed_station(self, station):
    self.managed_station = station   # 'station' → TrainStation  (suffix match)
```

#### Pattern 3: List accumulator — `self.field.append(param)`

```python
def add_train_schedule(self, train):
    self.scheduled_trains.append(train)  # 'train' → Train

def add_agent(self, agent):
    self.agents.append(agent)            # 'agent' → TicketAgent  (suffix match)
```

Same name-convention matching, applied to list fields that accumulate typed objects.

#### Name matching: `_match_param_to_class()`

Three tiers, tried in order — first match wins:

1. **snake_case → CamelCase exact**: `train_station` → `TrainStation`
2. **Case-insensitive exact**: `passenger` → `Passenger`, `route` → `Route`
3. **Unambiguous suffix** (≥ 4 chars): `station` → `TrainStation`
   — only fires when exactly **one** known internal class ends with that string;
   silently skips if two classes share the suffix (no FP risk from ambiguous names).

#### F block: emitting `Field → Class Use` edges

After all method passes, for each field with exactly one inferred type, a
`Field → Class Use` edge is inserted into the dependency DB — but only if:

- the target class is in a **different file** than the field's owning class (same-file edges
  are already covered by other mechanisms), and
- the target class is **not an ancestor** of the owning class (blocks StackGraphs-generated
  spurious edges such as `loyalty_points → Person` arising from inherited member resolution), and
- the field type is **unambiguous** — if multiple conflicting types were inferred for the
  same field, the field is skipped entirely.

This results in `Field → Class Use` cross-file edges visible in the DV8/DSM output:

```
Ticket.passenger          → Passenger     (ticket.py → passenger.py)
Ticket.route              → Route         (ticket.py → route.py)
Ticket.train              → Train         (ticket.py → train.py)
Train.route               → Route         (train.py → route.py)
TrainStation.available_trains → Train     (train_station.py → train.py)
Route.origin              → TrainStation  (route.py → train_station.py)
Route.destination         → TrainStation  (route.py → train_station.py)
StationManager.managed_station → TrainStation  (station_manager.py → train_station.py)
TicketAgent.assigned_station  → TrainStation   (ticket_agent.py → train_station.py)
```

#### Benchmark impact (TrainTicketSystem_TOY_PYTHON_FIRST)

| Metric | Before | After |
|--------|--------|-------|
| File-pair Recall | 55.9% | **91.7%** |
| File-pair Jaccard | ~56% | **86.8%** |
| Entity Jaccard | 87.4% | **89.4%** |
| Entity Precision | ~96% | **96.1%** |
| File-pair FPs | 2 | **2** (unchanged — pre-existing StackGraphs) |

#### What remains undetected (Stage 2 — deferred)

Three file-pair couplings require interprocedural call-chain tracing beyond static naming:

1. **`ticket.py → train_station.py`** — `display_ticket` calls methods on route/train objects
   that return `TrainStation`; the coupling is 2 hops through a return value.
2. **`ticket_booking_system.py → person.py`** — `display_system_stats` accesses `passenger.name`
   where `name` is inherited from `Person`; requires 2-hop: `passengers` list → `Passenger`
   → inherits `Person` → `Person.name`.
3. **`train_station.py → route.py`** — `search_trains` calls `train.get_route()` returning
   a `Route` object; requires tracking method return types across files.

These require **Stage 2**: call-site interprocedural analysis — scan constructor call sites,
match positional args to `__init__` parameter names, propagate inferred arg types back to
the field-type dict. Significantly more complex and deferred.

## Notes on naming / normalization

Handcount comparisons normalize names (file paths, class/method formatting) to align DV8 output with the handcount convention. This is done by `tools/compare_dv8_to_ground_truth.py` and does **not** change the underlying dependencies.

## ADVANCED: Abstract classes & duck typing

### Abstract Classes (Static typing in Python)
Abstract base classes (ABCs) define method signatures without implementation. Child classes must implement them.

Example:

from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass

class Car(Vehicle):
    def start_engine(self):
        print("Car engine started")

Dependency meaning: renaming `Vehicle.start_engine()` forces changes to `Car.start_engine()`.

### Duck Typing (Dynamic typing)
Python allows implicit interfaces without inheritance. Two classes with matching method names can be used interchangeably.

Example:

class Dog:
    def speak(self): return "Woof"

class Cat:
    def speak(self): return "Meow"

def make_it_speak(thing):
    thing.speak()

Duck-typing dependencies are real but **hard to detect** statically without type inference or runtime tracing. NeoDepends does not currently emit duck-typing edges.

### What exists in the toy examples

- Abstract classes: **Yes** (Python SECOND, Java SECOND)
- Duck typing: **No**

NeoDepends detects abstract-method override edges in Python and Java as **Override** dependencies.
