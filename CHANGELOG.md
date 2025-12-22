# Changelog (FreeworkEarth fork)

## v0.0.9

- Adds Python StackGraphs modes: `--stackgraphs-python-mode=ast` and `--stackgraphs-python-mode=use-only`.
- Adds `tools/neodepends_python_export.py` pipeline: DB extraction + Python enhancement + DV8 DSM exports (per-file + full-project).
- Vendors `tools/enhance_python_deps.py` and `tools/filter_false_positives.py` for self-contained releases.
- Adds optional StackGraphs cleanup flag `--filter-stackgraphs-false-positives` in the export pipeline.
- Adds `examples/` with TrainTicket Python toy projects and runnable commands.
- Adds GitHub Actions workflow to build and publish macOS/Windows binaries on tags.

