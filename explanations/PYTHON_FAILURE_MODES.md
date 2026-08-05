# Python Dependency Extraction — Failure-Mode Catalog

> **NeoDepends v0.3.10** — static analysis boundary conditions for Python.
> Each mechanism is classified as a **precision hazard** (phantom edges),
> **recall hazard** (missed edges), or **both**.

## Baseline (v0.3.6, 12-file adversarial slice)

| Metric | OLD instrument | NEW instrument (v0.3.6) |
|--------|---------------|------------------------|
| Precision | 88.4% | 93.8% |
| Recall | 99.5% | 99.5% |
| F1 | 93.6% | 96.6% |

---

## P — Precision Hazards (phantom edges)

### P1. Stdlib-shadow imports

**Class:** Precision hazard
**Status:** FIXED in v0.3.6

A project file whose name collides with a stdlib module (e.g. `careship/logging.py`)
causes StackGraphs to resolve bare `import logging` to the project file instead of
stdlib. Every file that says `import logging` gets a phantom Import edge to the
project's `logging.py`.

**Mechanism:** Python 3 uses absolute imports by default. `import logging` at module
level always resolves to `stdlib.logging`, not to `pkg/logging.py` nested inside a
package. StackGraphs name-binding cannot distinguish these.

**Impact observed:** 67 phantom Import cells pointing at `careship/logging.py` on the
careship codebase.

**Fix (v0.3.6):** `resolve_shadow_imports.py` — census of project files whose
stem matches a stdlib module name, then AST verification of each importing file to
classify the import as qualified/relative (genuine) vs bare (stdlib phantom → drop).

---

### P2. Unique-method-owner collision (generic method names)

**Class:** Precision hazard
**Status:** FIXED in v0.3.6

When a method name is defined in exactly one class in the project, the enhancer's
`unique_method_owner` heuristic resolves every `var.method()` call in the entire
codebase to that class — even when the receiver is a dict, list, or third-party
object.

**Mechanism:** `enhance_python_deps.py` builds a map of method names owned by
exactly one class. For common names like `.get()`, `.send()`, `.close()`, this
creates a many-to-one false binding. On careship, `ConnectionTypingState.get` was
the only class defining `.get()`, so 613 entity-level Call edges (150 file-level
cells) from 151 files were phantom.

**Impact observed:** 150 phantom file-level cells; largest SCC inflated from 39 to
189 (93% phantom).

**Fix (v0.3.6):** `_STDLIB_SHADOW_METHODS` blocklist — 21 method names that shadow
Python builtins / container protocols (`get`, `set`, `delete`, `update`, `keys`,
`values`, `items`, `pop`, `clear`, `add`, `remove`, `append`, `extend`, `insert`,
`close`, `read`, `write`, `send`, `format`, `copy`, `sort`) are excluded from
`unique_method_owner` resolution.

---

### P3. Definition-site attribution (UseTransitive)

**Class:** Mixed — precision hazard (phantom subset) + recall gap (real subset)
**Status:** LABELED in v0.3.10

StackGraphs resolves Use/Call edges to definition sites even when the source file
has no import to the target file. Some of these edges are phantom (shared-external-
symbol resolution, see P2), but others represent real coupling attributed through
re-export chains, DI injection, or inheritance-mediated access. v0.3.10 relabels
the real subset as `UseTransitive` so they can be distinguished and opted in/out
per export mode.

**Three mechanisms that produce UseTransitive edges:**

1. **Re-export chains** — `import shim; shim.Color.RED` where `shim/__init__.py`
   re-exports `Color` from `defs.py`. StackGraphs resolves the attribute access
   through the re-export chain to `defs.py`, creating Use edges from the consumer
   to `defs.py` without any Import edge between them.

2. **DI injection** — `from factory import create_service; svc = create_service();
   svc.process()` where `process()` is defined in `base.py`. The consumer imports
   the factory, not the definition site. StackGraphs resolves `.process()` to
   `base.py` via return-type inference, creating a Use edge with no Import anchor.

3. **Inheritance-mediated access** — `main.py` accesses an entity attribute (e.g.
   `ticket.name`) where `ticket` is a subclass instance. StackGraphs resolves the
   attribute to the parent class definition site. If `main.py` imports only the
   subclass, the parent file has no Import anchor — the edge is relabeled
   UseTransitive. This is real coupling that was previously silently dropped in
   import-scoped mode (a recall gap the label now makes visible and optable-in).

**StackGraphs mechanism note:** `import X; X.attr` does NOT create an Import edge
to `X`'s module-level file. The `import X` statement binds the module object, but
attribute access (`X.attr`) is resolved via scope-chain walking and creates Use
edges to the definition site. In contrast, `from X import attr` resolves the Import
binding directly to the definition site (creating an Import edge). This distinction
is the root cause of re-export UseTransitive edges. Evidence: `tests/fixtures/
use_transitive/consumer_reexport.py` vs a `from shim import Color` variant.

**UseTransitive label policy (mode-preserving defaults):**

- **Import-scoped mode** (default): UseTransitive edges are **dropped** by default
  (v0.3.9 behavior preserved). `--include-transitive-use` opts them in.
- **Non-scoped mode** (`--no-import-scoped`): UseTransitive edges are **kept** by
  default (v0.3.9 behavior preserved). `--exclude-transitive-use` opts them out.
- Edge count is preserved by the relabel (no edges added or removed in the DB).

**Anchor set:** `{Import, ImportLazy, Extend}` with transitive closure on Extend
chains. Matches the import-scoped gate in `neodepends_python_export.py` (continuity
by construction, amendment A1).

**Impact observed:** SECOND toy example (train-ticket Python): 18 UseTransitive
relabels — `main.py→person.py` (4), `main.py→staff.py` (3), `main.py→ticket.py`
(11). All are inheritance-mediated attribute access through subclass instances.

---

### P4. Re-export / transitive coupling

**Class:** Precision hazard
**Status:** Known limitation

When a type is moved to a shared module (e.g. `core/enums.py`) but the original
module re-exports it (`from core.enums import AccountType`), both the forward
import (original → core) and backward re-export (core → original) exist, creating
a net-zero or net-negative cycle effect.

**Mechanism:** The re-export `from X import Y` is a genuine Import edge in
StackGraphs. Users who `from original_module import AccountType` now have a
transitive path through the re-export, keeping the coupling alive.

**Impact observed:** Phase 4 enum extraction showed ΔM < 0.02% per phase because
re-export edges offset the benefit of extraction.

**Mitigation:** Remove re-exports after migration. This is a codebase-level decision,
not an instrument fix.

---

### P5. Star imports (`from module import *`)

**Class:** Precision hazard
**Status:** Known limitation

`from pkg import *` injects all public names from `pkg` into the importing file's
namespace. StackGraphs creates Import edges for all names in `__all__` (or all
non-underscore names). Some of these may be re-exports from other modules, creating
transitive phantom coupling.

**Mechanism:** Static analysis cannot know which of the star-imported names are
actually used without whole-program analysis. The conservative approach (import all)
over-counts.

**Impact observed:** Low on careship (few star imports in application code). Higher
risk in Django projects with `settings` star imports.

**Potential fix:** AST scan of the importing file for actually-used names, then
prune unused star-imported edges.

---

## R — Recall Hazards (missed edges)

### R1. Lazy / function-level imports

**Class:** Recall hazard (for module-level DSM); correctly tracked as `ImportLazy`
**Status:** HANDLED in v0.3.6 (edge-schema v2)

Python allows `import` statements inside function bodies. These are deferred —
they don't create module-level import-order cycles but DO create runtime coupling.

**Mechanism:** `enhance_python_deps.py` STEP 0 classifies imports by AST scope:
module-level → `Import`, function-level → `ImportLazy`. The `--exclude-lazy-imports`
flag creates a module-level-only DSM for package-cycle analysis.

**Impact:** On careship, ~621 lazy imports across the codebase. The distinction
matters: lazy imports don't contribute to import-order cycles but do create
runtime dependencies.

**Status:** Fully instrumented. Both scales (all-edges, module-edges) available.

---

### R2. `TYPE_CHECKING` guarded imports

**Class:** Recall hazard
**Status:** **FIXED in v0.3.7** — classified as `ImportType`

```python
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from other_module import SomeClass
```

These imports exist only for type checkers (mypy, pyright) and are completely
erased at runtime. They represent a design-time coupling but zero runtime coupling.

**Mechanism:** The `if TYPE_CHECKING:` block is never executed. StackGraphs parses
the AST and sees the import, but cannot evaluate the runtime guard. Current behavior
is inconsistent — sometimes the import is captured, sometimes not, depending on
StackGraphs' scope resolution.

**Architectural relevance:** TYPE_CHECKING imports indicate deliberate decoupling.
They are classified as `ImportType` — a third edge kind distinct from `Import`
(runtime) and `ImportLazy` (deferred runtime).

**Fix (v0.3.7):** `_is_type_checking_guard()` in `enhance_python_deps.py` detects
`if TYPE_CHECKING:` and `if typing.TYPE_CHECKING:` guards. Imports inside these
guards are classified as `ImportType`. Existing StackGraphs Import edges matching
TYPE_CHECKING targets are reclassified. `ImportType` edges are always excluded from
DSM exports (cycle analysis) but remain in the database for data consumers.

---

### R3. String-based / `importlib.import_module()` imports

**Class:** Recall hazard
**Status:** **FIXED in v0.3.7** — constant-string literals detected

```python
module = importlib.import_module("careship.domains.billing.service")
mod = __import__("careship.domains.billing.service")
```

Dynamic imports with string literals are invisible to static analysis but create
real runtime dependencies.

**Mechanism:** Static analyzers see `importlib.import_module(some_string)` but
don't evaluate the string argument. The dependency is completely invisible.

**Architectural relevance:** When string literals are constant and resolvable, these
represent real, measurable coupling. When they are computed at runtime (e.g.
`import_module(f"plugins.{name}")`), they are genuinely dynamic and cannot be
statically resolved.

**BAN RULE:** Using `importlib.import_module()` with a constant string as a
"cycle fix" is PROHIBITED — it is metric evasion, not decoupling.

**Fix (v0.3.7):** `_collect_importlib_literals()` in `enhance_python_deps.py` scans
for `importlib.import_module(` and `import_module(` calls with `ast.Constant` string
arguments. Resolved targets are added as `Import` edges. Only handles constant
strings — f-strings and variable arguments are left as genuinely dynamic.

---

### R4. Conditional imports (non-TYPE_CHECKING)

**Class:** Recall hazard
**Status:** **FIXED in v0.3.7** — module-level try/if/with blocks recursed

```python
try:
    import ujson as json
except ImportError:
    import json

if sys.platform == "win32":
    from .windows_impl import Handler
else:
    from .unix_impl import Handler
```

Imports guarded by try/except or platform/version checks. Both branches represent
potential runtime coupling depending on environment.

**Mechanism:** StackGraphs may capture only one branch or neither. The old
`_resolve_import_targets()` only processed direct children of `tree.body`, missing
imports nested inside `ast.Try`, `ast.If`, or `ast.With` blocks at module level.

**Fix (v0.3.7):** `_collect_module_level_imports()` recursively walks module-level
`try`/`if`/`with` blocks while stopping at `def`/`class` boundaries. Both branches
of try/except and if/else are captured as `Import` edges (conservative — all
branches execute at import time from the perspective of coupling analysis).

---

### R5. PEP 562 — Module `__getattr__` re-exports

**Class:** Recall hazard
**Status:** **HANDLED in v0.3.7** — captured as `ImportLazy` via scope classification

```python
# package/__init__.py
def __getattr__(name):
    if name == "SomeClass":
        from .submodule import SomeClass
        return SomeClass
    raise AttributeError(name)
```

PEP 562 allows modules to define `__getattr__` for lazy attribute access. This
is a dynamic re-export mechanism invisible to static analysis.

**Mechanism:** The `from package import SomeClass` resolves to `package/__init__.py`
at the static level, but at runtime it triggers `__getattr__` which imports from
`package/submodule.py`. The dependency on `submodule.py` is invisible.

**Fix (v0.3.7):** The import inside `def __getattr__` is function-level, so edge-
schema v2 scope classification captures it as `ImportLazy` (`__init__.py →
submodule.py`). The transitive hop (`consumer → __init__.py → submodule.py`) is
dynamically visible only and NOT recorded in the handcount (the consumer typically
has a direct import of `submodule.py` already).

---

### R6. Lazy-label package-init hop propagation

**Class:** Recall hazard (for edge-schema correctness)
**Status:** **FIXED in v0.3.9** — entity-level reclassifier + hop propagation

```python
def handle_provider_error(self, error_code: int) -> str:
    from tts.providers.protocol import (
        ProviderError as PErr,
    )
    raise PErr(f"Provider error: {error_code}", code=error_code)
```

When a function-level import targets a module inside a nested subpackage (e.g.
`from pkg.sub.mod import X`), StackGraphs creates Import edges to BOTH the final
target (`sub/mod.py`) AND intermediate `__init__.py` files traversed during
package resolution (`pkg/__init__.py`, `pkg/sub/__init__.py`).

**Bug (pre-v0.3.9):** The lazy reclassifier only updated File-to-File Import edges.
StackGraphs also creates entity-level edges (Method→File, Method→Class) that were
never reclassified. Additionally, Import edges to intermediate `__init__.py` hops
were never relabeled as ImportLazy, even when the import was function-scoped.

**Mechanism:** Two sub-issues:

1. **Entity-level edges:** StackGraphs creates edges between entities at various
   granularities (Function→File, Method→Class). The old reclassifier matched
   `WHERE src = <file_id> AND tgt = <file_id>`, missing entity-level edges.
2. **Package-init hops:** `from pkg.sub.mod import X` traverses `pkg/sub/__init__.py`
   during resolution. The hop edge must carry the same label as the import that
   caused it. If the hop prefix is exclusive to lazy imports (not shared with
   module-level imports), the hop edge is reclassified to ImportLazy.

**Fix (v0.3.9):**

- `file_descendants` precomputation: BFS from each File entity to collect all
  descendant entity IDs, enabling `WHERE src IN (...) AND tgt IN (...)`.
- `_pkg_prefixes()` helper: computes package directory prefixes for a set of
  file targets. Exclusive prefixes (in fl_pfx but not in ml_pfx) identify
  `__init__.py` hops that belong to lazy imports only.
- Same logic applied for `ImportType` (TYPE_CHECKING) hops.

**Impact:** On the toy benchmark, 7 entity-level edges were correctly reclassified
(Import→ImportLazy or Import→ImportType) that were previously mislabeled. On
production codebases, the number scales with function-level imports targeting
nested subpackages.

---

### R7. Dynamic `getattr()` on modules

**Class:** Recall hazard
**Status:** NOT instrumented

```python
handler = getattr(billing_module, "BillingHandler")
```

When `getattr()` is called on a module object with a string literal, the target
is invisible to static analysis.

**Mechanism:** Similar to string imports but operates on already-imported module
objects. The dependency on the specific symbol is unresolvable statically.

**Impact:** Low — most `getattr()` usage is on instances, not modules.

---

### R8. Decorator-based registration

**Class:** Recall hazard
**Status:** NOT instrumented

```python
@app.route("/api/billing")
def billing_endpoint():
    from .billing.service import process
    return process()
```

Decorator registration (Flask routes, Celery tasks, signal handlers) creates
implicit coupling between the registrar and the decorated function. The import
inside the decorated function is captured (as ImportLazy), but the registration
coupling itself is invisible.

**Mechanism:** `@app.route(...)` creates a runtime binding between the Flask app
object and the function. This is framework-mediated coupling that no static
analyzer can capture without framework-specific knowledge.

**Impact:** Framework coupling is architectural but orthogonal to module-level
dependency analysis. Generally does not affect M-score.

---

### R9. Dependency injection / service locator

**Class:** Recall hazard
**Status:** NOT instrumented (but service-registry pattern is used in refactoring)

```python
# provider
container.register("billing", BillingService)
# consumer
billing = container.get("billing")
billing.process()
```

DI frameworks decouple static imports but create runtime coupling through the
container. The consumer's dependency on `BillingService` is invisible to static
analysis.

**Mechanism:** Registration happens at startup; lookup happens at runtime. The
string key `"billing"` is the coupling mechanism, invisible to import analysis.

**Impact:** This is by design — DI intentionally decouples static dependencies.
The M-score improvement from registry inversion (Phase 2, Phase 3) is REAL
architectural improvement, not metric evasion, because it eliminates import-order
constraints.

---

### R10. Dual-scope TYPE_CHECKING + lazy import

**Class:** Recall hazard
**Status:** **FIXED v0.3.9** — dual-scope detection in `enhance_python_deps.py`

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tts.route import Route  # design-time only

class Service:
    def process(self, route_id):
        from tts.route import Route  # runtime lazy import
        ...
```

When the same module is imported BOTH under `if TYPE_CHECKING:` (module level)
AND inside a function body (lazy import), the target-set subtraction
`fl_only_targets = all_targets - ml_targets - tc_targets` erased the
function-level classification because the target appeared in `tc_targets`.

**Impact:** The entity-level reclassifier then swept ALL Import edges for that
target to ImportType, losing the runtime dependency anchor. With import-scoped
filtering, the entire file pair's Use/Call/Create edges were also lost.

**Fix (v0.3.9):** Collect function-body imports separately via
`ast.FunctionDef`/`ast.AsyncFunctionDef` walk. Compute
`dual_scope = tc_targets & func_body_targets`. Subtract only pure
TYPE_CHECKING targets: `tc_targets = tc_targets - dual_scope`. The runtime
half gets ImportLazy (runtime supersedes design-time).

**Fixture:** `tts/reporting_service.py` — dual-scope import of `tts.route`
(TYPE_CHECKING at module level + lazy import in `format_route_detail()`).

---

## B — Both Precision and Recall

### B1. Inheritance chain / override resolution

**Class:** Both
**Status:** Partially instrumented (`detect_overrides.py`)

```python
class Base:
    def process(self): ...

class Child(Base):
    def process(self):  # override
        super().process()
```

**Precision risk:** StackGraphs may resolve `obj.process()` to `Base.process`
when the runtime type is `Child` (dispatches to `Child.process`).

**Recall risk:** Override relationships (`Child.process` overrides `Base.process`)
may not generate explicit dependency edges.

**Status:** `detect_overrides.py` adds Extend edges for inheritance and tracks
override relationships. `super().method()` calls are captured. Cross-file
polymorphic dispatch (call site in file A, base in file B, override in file C)
remains partially unresolved.

---

### B2. Protocol / structural typing

**Class:** Both
**Status:** NOT instrumented

```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict: ...

def save(obj: Serializable):  # structural, not nominal
    data = obj.to_dict()
```

**Precision risk:** Any class with a `to_dict()` method could match, even if
unrelated. Static analysis may over-bind.

**Recall risk:** The structural relationship between `Serializable` and
implementing classes is implicit — no `extends` or `implements` keyword.

**Impact:** Protocols are increasingly common in modern Python. No static analyzer
fully handles structural subtyping.

---

### B3. String / forward-reference type annotations

**Class:** Both
**Status:** Partially instrumented (enhance_python_deps.py handles `"ClassName"` in annotated assignments)

```python
class Tree:
    left: "Tree"       # forward ref
    right: "Tree"

def process(node: "billing.Invoice"):  # cross-module forward ref
    ...
```

**Precision risk:** If the string matches a class name in another file, a phantom
Use edge may be created.

**Recall risk:** If the string doesn't match any known class, the dependency is
missed entirely.

**Status:** `enhance_python_deps.py` handles `self.field: "ClassName"` via
`ast.Constant` string matching against `known_classes`. Cross-module dotted
forward refs (e.g. `"billing.Invoice"`) are NOT resolved.

---

### B4. `exec()` / `eval()` with import statements

**Class:** Both
**Status:** NOT instrumented (and should NOT be)

```python
exec("from billing.service import BillingService")
module = eval("__import__('billing.service')")
```

**Mechanism:** Arbitrary code execution. Cannot be statically analyzed.

**Impact:** Extremely rare in production code. Should trigger a lint warning,
not a dependency edge.

**Policy:** Intentionally excluded from static analysis scope.

---

### B5. Stdlib shadow generality (second shadow name)

**Class:** Both (precision: phantom bare-import edges; recall: n/a for in-scope)
**Status:** **VALIDATED in v0.3.7** — census-based resolver generalizes

Verifies that the stdlib-shadow resolver (P1 fix) generalizes beyond the originally
discovered `logging.py` shadow to any stdlib name collision. The toy fixture adds
`tts/json.py` which shadows stdlib `json`.

**Mechanism:** `import json` in a file resolves to stdlib, not `tts/json.py`.
`from tts.json import to_json` is a qualified import → genuine edge.

**Validation (v0.3.7):** The census-based `resolve_shadow_imports.py` automatically
discovers `tts/json.py` as a second shadow name (alongside `tts/logging.py`) with
zero configuration. Bare `import json` edges are correctly dropped; qualified
`from tts.json import ...` edges are preserved. This confirms the fix is a
**class-level solution**, not a one-off bug patch.

---

## Summary Table

| ID | Mechanism | Class | Status | Impact |
|----|-----------|-------|--------|--------|
| P1 | Stdlib-shadow imports | Precision | **FIXED v0.3.6** | 67 phantom cells |
| P2 | Unique-method-owner collision | Precision | **FIXED v0.3.6** | 150 phantom cells |
| P3 | Definition-site attribution (UseTransitive) | Attribution | **LABELLED v0.3.10** | ~46 cells |
| P4 | Re-export / transitive coupling | Precision | Known | ΔM < 0.02% |
| P5 | Star imports | Precision | Known | Low (project-dependent) |
| R1 | Lazy / function-level imports | Recall | **HANDLED v0.3.6** | 621 edges reclassified |
| R2 | TYPE_CHECKING guarded imports | Recall | **FIXED v0.3.7** | Reclassified as ImportType |
| R3 | String-based importlib imports | Recall | **FIXED v0.3.7** | Constant-string detection |
| R4 | Conditional imports | Recall | **FIXED v0.3.7** | Module-level try/if/with recursion |
| R5 | PEP 562 module `__getattr__` | Recall | **HANDLED v0.3.7** | Captured as ImportLazy |
| R6 | Lazy-label package-init hop | Recall | **FIXED v0.3.9** | Entity-level + hop propagation |
| R7 | Dynamic `getattr()` on modules | Recall | Not instrumented | Low |
| R8 | Decorator-based registration | Recall | Not instrumented | Framework-level |
| R9 | Dependency injection / service locator | Recall | Not instrumented | By design |
| R10 | Dual-scope TYPE_CHECKING + lazy | Recall | **FIXED v0.3.9** | Runtime supersedes design-time |
| B1 | Inheritance / override resolution | Both | Partial | Medium |
| B2 | Protocol / structural typing | Both | Not instrumented | Growing |
| B3 | String / forward-ref annotations | Both | Partial | Low-medium |
| B4 | `exec()` / `eval()` | Both | Excluded | Negligible |
| B5 | Stdlib shadow generality | Both | **VALIDATED v0.3.7** | Census-based resolver generalizes |

---

## Priority for next release

1. **P3 → UseTransitive label shipped in v0.3.10** (definition-site edges labelled, excluded from import-scoped DSM)
2. **B2 → Protocol / structural typing detection** (growing adoption in modern Python)
3. **B3 → Cross-module dotted forward refs** (e.g. `"billing.Invoice"`)
