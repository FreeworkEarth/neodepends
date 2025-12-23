# NeoDepends (FreeworkEarth fork)

NeoDepends extracts code entities and dependency relationships from a project and exports them in machine-readable formats (SQLite/DSM) for architecture analysis.

This repository is a fork that adds a Python-focused DV8 export pipeline (post-processing + DV8 DSM export helper scripts under `tools/`) while keeping the upstream NeoDepends CLI intact.

## Install

### Release bundle (recommended)

Download a release artifact from this fork and unzip it. The bundle includes:

- `neodepends` executable
- `depends.jar` (required for `--depends`)
- `languages/` (Tree-sitter tagging + StackGraphs definitions)
- `tools/` (Python DV8 export helpers)
- `examples/` (toy projects)

Run:

```bash
./neodepends --help
```

If you downloaded the release bundle, do not run `cargo build` inside it (there is no `Cargo.toml`).

Release tags in this fork use a suffix to avoid confusion with upstream (example: `v0.0.9-pyfork`).

macOS note: if Gatekeeper blocks the executable after download/unzip, use System Settings → Privacy & Security to allow it, or run:

```bash
chmod +x ./neodepends
xattr -dr com.apple.quarantine ./neodepends
```

### Build from source

Requires Rust and Cargo.

```bash
cargo build --release
./target/release/neodepends --help
```

If you built from source and want to use `--depends`, either place `depends.jar` next to the executable
or pass it explicitly:

```bash
./target/release/neodepends --depends --depends-jar ./artifacts/depends.jar --help
```

## CLI usage (core NeoDepends)

Scan directly from disk (no git required) and export to SQLite:

```bash
./neodepends \
  --input WORKDIR \
  --output out.sqlite \
  --format sqlite \
  --resources entities,deps,contents \
  --langs java \
  --depends
```

Windows:

```powershell
.\neodepends.exe --help
.\neodepends.exe --input WORKDIR --output out.sqlite --format sqlite --resources entities,deps,contents --langs java --depends
```

Notes:

- Depends (`--depends`) requires a Java runtime (and ships a `depends.jar` in this fork’s bundle).
- StackGraphs (`--stackgraphs`) is a name-binding resolver; it is available without Java.

Git mode (optional): you can also scan commits from a git repository instead of scanning directly from disk. For example:

```bash
./neodepends --output out.dsm-v2.json --format dsm-v2 --depends HEAD
```

`HEAD` can be replaced with any commit-ish, or with `WORKDIR` to force disk mode.

## DV8 export helper (Python)

For DV8 Explorer workflows, use `tools/neodepends_python_export.py`. It runs NeoDepends, applies optional Python post-processing, and exports DV8-openable DSM JSONs (full-project + file-level + per-file).

Example (StackGraphs + AST classification, structured DV8 hierarchy):

```bash
python3 tools/neodepends_python_export.py \
  --input examples/TrainTicketSystem_TOY_PYTHON_FIRST/tts \
  --output-dir /tmp/neodepends_tts_toy1 \
  --resolver stackgraphs \
  --stackgraphs-python-mode ast \
  --dv8-hierarchy structured \
  --filter-architecture \
  --filter-stackgraphs-false-positives
```

Windows (Python):

```powershell
py -3 tools\neodepends_python_export.py `
  --input examples\TrainTicketSystem_TOY_PYTHON_FIRST\tts `
  --output-dir C:\tmp\neodepends_tts_toy1 `
  --resolver stackgraphs `
  --stackgraphs-python-mode ast `
  --dv8-hierarchy structured `
  --filter-architecture `
  --filter-stackgraphs-false-positives
```

Key outputs (naming scheme “DV8 DSM v3”):

- `dependencies.<resolver>.filtered.db`
- `dependencies.<resolver>.filtered.dv8-dsm-v3.json` (full-project DSM)
- `dependencies.<resolver>.filtered.file.dv8-dsm-v3.json` (file-level DSM)
- `dv8_deps/*.dv8-dependency.json` (per-file DSMs)

Where `<resolver>` is one of:

- `depends`
- `stackgraphs_ast`
- `stackgraphs_use_only`

**Which file to open in DV8:**

- Open `dependencies.<resolver>.filtered.dv8-dsm-v3.json` for the full, drill-down DSM (recommended for most analysis).
- Open `dependencies.<resolver>.filtered.file.dv8-dsm-v3.json` for a file-level DSM.
- Per-file DSMs are in the `dv8_deps/` subdirectory.

**Note on binary location:**

- In the release bundle: the `neodepends` executable is in the root directory of the extracted archive.
- When building from source: the executable is at `target/release/neodepends`.

## Examples

See `examples/README.md` for bundled toy projects and runnable commands.

## Help

```bash
./neodepends --help
python3 tools/neodepends_python_export.py --help
```
