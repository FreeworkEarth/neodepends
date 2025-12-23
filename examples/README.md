# Examples

This repo includes small toy projects used to validate Python entity extraction, dependency resolution, and DV8 DSM exports.

## TrainTicket (Python) — Toy 1 (more coupled)

Project: `examples/TrainTicketSystem_TOY_PYTHON_FIRST`

If you built from source, use `./target/release/neodepends`. If you downloaded a release bundle, use `./neodepends`.

Run NeoDepends + Python enhancement + DV8 exports (recommended settings for this workspace):

```bash
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./neodepends \
  --input examples/TrainTicketSystem_TOY_PYTHON_FIRST/tts \
  --output-dir /tmp/neodepends_tts_toy1_stackgraphs_ast \
  --resolver stackgraphs \
  --stackgraphs-python-mode ast \
  --filter-architecture \
  --dv8-hierarchy structured \
  --filter-stackgraphs-false-positives
```

Outputs:

- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dependencies.stackgraphs_ast.filtered.db` (enhanced DB)
- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json` (full DSM for DV8)
- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dependencies.stackgraphs_ast.filtered.file.dv8-dsm-v3.json` (file-level DSM for DV8)
- `/tmp/neodepends_tts_toy1_stackgraphs_ast/dv8_deps/*.dv8-dependency.json` (per-file DSMs)

Open in DV8 Explorer:

- Use the full-project DSM: `dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json`

## TrainTicket (Python) — Toy 2 (more modular)

Project: `examples/TrainTicketSystem_TOY_PYTHON_SECOND`

```bash
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./neodepends \
  --input examples/TrainTicketSystem_TOY_PYTHON_SECOND/tts \
  --output-dir /tmp/neodepends_tts_toy2_stackgraphs_ast \
  --resolver stackgraphs \
  --stackgraphs-python-mode ast \
  --filter-architecture \
  --dv8-hierarchy structured \
  --filter-stackgraphs-false-positives
```
