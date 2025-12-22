# NeoDepends vs Ground Truth (TrainTicketSystem_TOY_PYTHON_FIRST)

This folder contains two “ground truth” edge sets produced by `generate_ground_truth.py`:

- **Strict (static, Java-like)**: `handcount_edges.json` (251 unique edges)
- **Heuristic (Python-friendly)**: `handcount_edges.heuristic.json` (257 unique edges)

## Closest NeoDepends run saved

Best current NeoDepends run (Depends resolver + enhanced Python postprocessing + handcount-aligned DV8 export):

- `TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/EXAMPLES_CHRIS/RESULTS/NEODEP_V008_ALIGN5_HANDCOUNT_TYPED_DEDUPE`

Key DV8 file:

- `TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/EXAMPLES_CHRIS/RESULTS/NEODEP_V008_ALIGN5_HANDCOUNT_TYPED_DEDUPE/dependencies.full.dv8-dependency.json`

## Which resolver matches best?

Compared against the **Heuristic** ground truth (Python-friendly), including `Import/Extend/Create/Call/Use` kinds and unique-edge counting:

- **Depends** (best): `missing=0`, `extra=0`

So for this project (and these handcount rules), **Depends** is currently the better match.

## How to rerun comparisons

Depends run:

- `python3 dependencies_files_handcount/compare_neodepends_to_ground_truth.py --project-root . --ground-truth dependencies_files_handcount/handcount_edges.heuristic.json --neodepends-dv8 ../RESULTS/NEODEP_V008_ALIGN5_HANDCOUNT_TYPED_DEDUPE/dependencies.full.dv8-dependency.json`

## DV8 naming parity

The NeoDepends full DSM now matches the handcount DSM variable naming exactly:

- Handcount reference: `dependencies_files_handcount/handcount_full_typed.heuristic.dv8-dependency.json`
- NeoDepends output: `../RESULTS/NEODEP_V008_ALIGN5_HANDCOUNT_TYPED_DEDUPE/dependencies.full.dv8-dependency.json`
