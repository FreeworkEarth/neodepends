# Releasing (FreeworkEarth fork)

This fork adds Python StackGraphs+AST improvements plus a DV8 export pipeline in `tools/`.

## Versioning

- `Cargo.toml` is the source of truth.
- Tag releases as `vX.Y.Z` (example: `v0.0.9`) to trigger GitHub Actions builds.

## Local sanity checks

```bash
cargo test
cargo build --release
./target/release/neodepends --version
```

## Create a release

1) Bump version in `Cargo.toml` (and regenerate `Cargo.lock` if needed):

```bash
cargo update -p neodepends || true
```

2) Commit changes.

3) Tag and push:

```bash
git tag -a v0.0.9 -m "neodepends v0.0.9 (Freework fork)"
git push origin main --tags
```

4) GitHub Actions builds and publishes assets for:

- macOS (Apple Silicon): `aarch64-apple-darwin`
- macOS (Intel): `x86_64-apple-darwin`
- Windows: `x86_64-pc-windows-msvc`

Assets include:

- `neodepends` / `neodepends.exe`
- `tools/` helper scripts (DV8 export, ground truth generator, comparisons)
- `languages/` (tree-sitter tags + stack-graphs config)
- `examples/` (TrainTicket toy projects)

