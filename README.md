NeoDepends extracts code entities and dependency relationships from a project and exports them in machine-readable formats (SQLite/DSM) for architecture analysis.

## Build

```bash
cargo build --release
```

## CLI usage

Show all options:

```bash
./target/release/neodepends --help
```

Scan directly from disk (no git required) and export to SQLite:

```bash
./target/release/neodepends \
  --input WORKDIR \
  --output out.sqlite \
  --format sqlite \
  --resources entities,deps,contents \
  --langs python \
  --depends
```

Java example:

```bash
./target/release/neodepends \
  --input WORKDIR \
  --output out.sqlite \
  --format sqlite \
  --resources entities,deps,contents \
  --langs java \
  --depends
```

## Dependency resolvers

NeoDepends supports two dependency resolvers:

- `--depends`: uses Depends (`depends.jar`) to infer `Call`, `Create`, `Extend`, and related dependency kinds.
- `--stackgraphs`: uses StackGraphs to resolve name bindings (reference → definition). In this fork, Python can optionally classify some StackGraphs references using AST context via `--stackgraphs-python-mode`.

## DV8 (Python) export helper

For DV8 Explorer workflows, use `tools/neodepends_python_export.py`. It runs NeoDepends, applies optional Python post-processing, and exports DV8 dependency JSONs (full-project DSM + per-file DSMs).

```bash
python3 tools/neodepends_python_export.py \
  --neodepends-bin ./target/release/neodepends \
  --input /path/to/python_package_or_folder \
  --output-dir /tmp/neodepends_run \
  --resolver stackgraphs \
  --stackgraphs-python-mode ast \
  --filter-architecture \
  --dv8-hierarchy structured \
  --filter-stackgraphs-false-positives
```

## Examples

See `examples/README.md` for bundled TrainTicket toy projects and runnable commands.
