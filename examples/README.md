# Examples

This repo includes small toy projects used to validate Python entity extraction, dependency resolution, and DV8 DSM exports.

## TrainTicket (Python) — Toy 1 (more coupled)

Project: `examples/TrainTicketSystem_TOY_PYTHON_FIRST`

Build NeoDepends:

```bash
cargo build --release
```

Run NeoDepends + Python enhancement + DV8 exports (recommended settings for this workspace):

```bash
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./target/release/neodepends \
  --input examples/TrainTicketSystem_TOY_PYTHON_FIRST/tts \
  --output-dir /tmp/neodepends_tts_toy1_stackgraphs_ast \
  --resolver stackgraphs \
  --stackgraphs-python-mode ast \
  --filter-architecture \
  --dv8-hierarchy structured \
  --filter-stackgraphs-false-positives
```

Outputs:

- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dependencies_stackgraphs_ast.db` (enhanced DB)
- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dependencies_stackgraphs_ast.full.dv8-dependency.json` (full DSM for DV8)
- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dv8_deps/*.dv8-dependency.json` (per-file DSMs)

## TrainTicket (Python) — Toy 2 (more modular)

Project: `examples/TrainTicketSystem_TOY_PYTHON_SECOND`

```bash
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./target/release/neodepends \
  --input examples/TrainTicketSystem_TOY_PYTHON_SECOND/tts \
  --output-dir /tmp/neodepends_tts_toy2_stackgraphs_ast \
  --resolver stackgraphs \
  --stackgraphs-python-mode ast \
  --filter-architecture \
  --dv8-hierarchy structured \
  --filter-stackgraphs-false-positives
```
