# NeoDepends: Depends vs StackGraphs, and Dependency Kinds

## ELI5: what each thing does

### NeoDepends (the tool)
NeoDepends does two separate jobs:

1) **Entity extraction**: find “things” in code (files, classes, methods, fields) using Tree-sitter tag queries (e.g. `languages/python/tags.scm`).
2) **Dependency resolution**: find “arrows” between those things using a resolver.

So the big difference you saw (`depends` vs `stackgraphs`) is not about entities — it’s about the resolver that generates the arrows.

### Depends (the resolver, via `depends.jar`)
ELI5: **Depends is like a smart Java program that tries to understand code behavior** and says:
- “this method **calls** that method” (`Call`)
- “this method **creates** an instance of that class” (`Create`)
- “this class **extends** that class” (`Extend`)
- “this method **uses** that thing” (`Use`, type coupling / variable usage / etc., depending on language support)

For your Python toy example, Depends is the only resolver currently producing `Call/Create/Extend` in NeoDepends.

### StackGraphs (the resolver, via `stack-graphs.tsg`)
ELI5: **StackGraphs is like a super-precise ‘name linker’**.

It answers: “When I see the name `X` here, which definition of `X` does it refer to?”

In upstream NeoDepends, StackGraphs output is converted into **one dependency kind**:
- `Use`

In this fork, we added a Python-only AST classifier on top of StackGraphs so it can also emit:
- `Call`, `Create`, `Extend`, `Import` (when the AST context makes that unambiguous)

So StackGraphs produces a lot of “uses” but it does **not** label them as “call vs create vs extend”.

That’s why your comparison run shows:
- `depends`: `Call/Create/Extend/Use`
- `stackgraphs`: only `Use`

## Why StackGraphs was only `Use` (and what changed in this fork)
Upstream NeoDepends’ StackGraphs resolver (`src/stackgraphs.rs`) emits:

- `DepKind::Use` for every stitched reference path

StackGraphs itself is focused on *name binding* (who refers to what), not on classifying the *reason* for the reference (call/create/extend/etc.).

To get `Call/Create/Extend/Import` from StackGraphs output, NeoDepends needs an extra “syntax classifier” stage:
- Resolve `X` to its definition via StackGraphs
- Look at the AST context where `X` appears:
  - `X(...)` might be a function call (or class construction in Python)
  - `class A(B):` is inheritance (`Extend`)
  - `new X(...)` in Java is `Create`

This fork implements a first version of that idea for Python (using Tree-sitter around the StackGraphs reference span).

This is **not something `tags.scm` controls** — `tags.scm` only finds entities, not dependency semantics.

## Can we “configure StackGraphs” to output Call/Create/Extend?
Not just by editing `tags.scm`.

Possible approaches (code changes in NeoDepends):

1) **Add a StackGraphs + AST classification pass**
   - Keep StackGraphs for “who does this name refer to?”
   - Add Tree-sitter AST checks around the reference site to decide if it’s Call/Create/Extend/Import/etc.
   - Python caveat: `Foo()` is ambiguous (call vs create) unless you know `Foo` resolves to a class.

2) **Keep StackGraphs as Use-only**
   - Treat StackGraphs as a fallback resolver (always available, low semantic detail)
   - Treat Depends as the “semantic-rich” resolver when available

## Dependency kinds NeoDepends supports (schema)
NeoDepends’ dependency kinds are defined in `src/core.rs` as `DepKind`:

- `Annotation`
- `Call`
- `Cast`
- `Contain`
- `Create`
- `Dependency`
- `Extend`
- `Implement`
- `Import`
- `Link`
- `MixIn`
- `Parameter`
- `Parent`
- `Plugin`
- `Receive`
- `Return`
- `Set`
- `Throw`
- `Use`

## Why we usually focus on Call/Create/Extend/Use for Deicide/DV8
For Deicide-style clustering and for DV8 visualization, these are the most consistently useful across languages:

- `Call`: strong “behavioral coupling” between methods
- `Use`: data/field coupling and type coupling
- `Create`: construction/ownership relationships
- `Extend`: inheritance structure

Many other kinds are either:
- Rare in the toy examples,
- Not emitted by the current resolver for your language,
- Too noisy for architecture clustering unless carefully filtered (e.g. `Import` can overwhelm).

## What the “other kinds” mean (and why they’re usually not the default signal)
NeoDepends can store many kinds, but “which ones you actually get” depends on the resolver and language. Also: for architecture clustering, some kinds are too noisy or too inconsistent across languages to be a good default.

- `Annotation`: metadata usage (e.g. `@Something`); often noisy for architecture clustering.
- `Cast`: explicit type cast (mostly Java/C-family); limited value for modularity.
- `Contain`: “X contains Y” (composition/containment); not consistently emitted across resolvers.
- `Dependency`: very generic fallback; not specific enough to drive refactoring decisions.
- `Implement`: interface implementation (Java); useful sometimes, but less common in the toy systems.
- `Import`: module/package import; can dominate the graph and hide runtime coupling unless filtered.
- `Link`: linker-level relation (C/C++); not applicable to Python/Java toy examples.
- `MixIn`: mixin usage (Ruby/Python patterns); resolver support varies a lot.
- `Parameter`: uses a type via parameter annotation; Python typing is optional and inconsistent.
- `Parent`: structural relationship; usually already represented by the entity tree, not a dependency edge.
- `Plugin`: framework/plugin wiring; not present in toy systems.
- `Receive`: callback/event/message receive; highly framework-specific.
- `Return`: return-type coupling; same issues as `Parameter` (typing optional in Python).
- `Set`: assignment to a variable/field; can be extremely frequent without careful scoping.
- `Throw`: exception thrown; usually not a modularity driver unless you analyze exception-flow.

We can still export all kinds for research, but for Deicide/DV8 the default should remain a small, high-signal subset with optional “include more kinds” flags.

## Can we merge Depends + StackGraphs?
Yes, but “merge” needs a policy, because StackGraphs can add lots of extra `Use` edges that are not the same signal as Depends’ `Call/Create/Extend`.

The safest incremental merge strategy is:

1) Use **Depends** as the base (keep its `Call/Create/Extend/Use`).
2) Add **StackGraphs** edges only for the subset you want (usually additional `Use` edges).
3) Filter out noisy StackGraphs-only patterns if needed (common filters: `Method->File`, `Field->File`, or other edges that don’t help clustering).
4) Deduplicate identical `(src, tgt, kind)` edges.

This gives “maximum recall” for `Use` while preserving the richer semantic kinds from Depends.

## “Shouldn’t it be StackGraphs vs Depends inside NeoDepends?”
Yes.

NeoDepends is the orchestrator:
- entity extraction (Tree-sitter tag queries)
- dependency resolution (Depends or StackGraphs)

So the correct comparison is: “NeoDepends with resolver=Depends” vs “NeoDepends with resolver=StackGraphs”.

## ELI5: what “noisy” and “inconsistent across languages” means
When we say a dependency kind is “too noisy”, we mean:
- it happens *so often* that it dominates the graph (you see mostly that kind), and
- it doesn’t tell you much about *design structure* without heavy filtering.

Examples:
- `Import`: almost every file imports something; the graph becomes “everything depends on everything” unless you filter.
- `Set`: assignments can occur on nearly every line; if emitted at method granularity it can swamp the signal.

When we say “inconsistent across languages”, we mean:
- the same kind exists in the schema, but different languages/resolvers emit it very differently,
- or the language feature isn’t even present (e.g. `Cast` in Python),
- or it depends on optional information (e.g. Python type hints).

Examples:
- `Parameter` / `Return`: in Java this is always explicit; in Python it’s optional and often missing.
- `Implement` / `MixIn`: meaningful in some languages and almost absent in others.

That’s why the “default” clustering signal is usually the small subset that tends to exist across languages and carry strong modularity meaning: `Call`, `Use`, `Create`, `Extend`.

## ELI5: how Deicide clustering works (high level)
Think of a class as a box with many methods/fields inside.

Deicide tries to answer: “Which of these inside-things belong together in smaller groups?”

It builds a similarity/coupling signal between methods/fields using:
- dependencies (e.g. calls, uses), and
- name/text similarity (methods that talk about the same concepts often share words).

Then it repeatedly groups the “most related” items together, building a hierarchy (a tree).
That hierarchy is the “clustering”.

If the hierarchy gets very deep (many levels), it’s a sign the class contains multiple unrelated responsibilities (“god class” signal).

## Why the “sibling-only” issue shows up
In our class-layer workflow, we typically cluster the *direct children* of a class:
- Methods and Fields directly under the class.

If NeoDepends tags a field as a child of a method (because the assignment `self.x = ...` happens inside that method), then:
- the field is no longer a direct child of the class
- method->field `Use` edges aren’t between same-parent siblings
- and the class-layer clustering can miss that coupling

So we fix it by re-parenting fields to the class (and merging duplicates), so Deicide sees a clean “class contains methods+fields” layer.

You’re right that Deicide could also be changed to cluster across descendants (not just direct children). That’s doable, but it’s a larger semantic change: you must decide how to handle nested defs/classes and how to avoid mixing unrelated scopes.
