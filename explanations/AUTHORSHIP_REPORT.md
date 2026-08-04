# AUTHORSHIP REPORT -- NeoDepends (FreeworkEarth fork)

**Date:** 2026-08-04
**Method:** `git blame --line-porcelain` on tracked files (excluding
`.venv/`, `Cargo.lock`, `depends.jar`, `.class` binaries)
**Scope:** Read-only measurement. No code changes.

---

## Summary

Current tree: **72.6% of surviving lines by FreeworkEarth** (91.8% of
tools/, 100% of examples/, 100% of explanations/, 7.7% of src/).
Fork diverged by **+132,539 / -207 lines** over **61 commits** since
2025-09-03.

---

## 1. Fork Point

| Field | Value |
|-------|-------|
| Upstream | `jlefever/neodepends` (upstream/main) |
| Fork SHA | `fd66fbf` |
| Fork date | 2025-09-03 |
| Fork commit | "fix Windows path issue" |
| Our remote | `FreeworkEarth/neodepends` (origin/main) |

---

## 2. Commits Since Fork

| Author | Commits |
|--------|---------|
| FreeworkEarth | 61 |

All 61 post-fork commits are by FreeworkEarth. No upstream commits merged
in after the fork point.

---

## 3. Line Attribution (git blame, current tree)

### By directory

| Directory | FreeworkEarth | Jason Lefever | Bao Vuong | Nick | Total | FE % |
|-----------|--------------|---------------|-----------|------|-------|------|
| `src/` (Rust core) | 326 | 3,887 | -- | -- | 4,213 | 7.7% |
| `tools/` (Python) | 9,695 | -- | 866 | -- | 10,561 | 91.8% |
| `examples/` | 34,210 | -- | -- | -- | 34,210 | 100.0% |
| `explanations/` | 1,399 | -- | -- | -- | 1,399 | 100.0% |
| other (root, build, CI, languages, tests) | 7,197 | 14,755 | 302 | 176 | 22,430 | 32.1% |
| **TOTAL** | **52,827** | **18,642** | **1,168** | **176** | **72,813** | **72.6%** |

### By author (grand total)

| Author | Lines | % |
|--------|-------|---|
| FreeworkEarth | 52,827 | 72.6% |
| Jason Lefever | 18,642 | 25.6% |
| Bao Vuong | 1,168 | 1.6% |
| Nick | 176 | 0.2% |
| **Total** | **72,813** | **100.0%** |

---

## 4. Divergence from Upstream

```
793 files changed, 132,539 insertions(+), 207 deletions(-)
```

The fork added 793 files and 132K lines while modifying only 207 upstream
lines. The upstream Rust core (`src/`) is largely untouched.

---

## 5. LOC by Directory (wc -l, all tracked files)

| Directory | Files | Lines | Primary language |
|-----------|-------|-------|-----------------|
| `src/` | 13 | 4,213 | Rust |
| `tools/` | 15 | 11,013 | Python |
| `examples/` | many | 33,645 | Python, Java, JSON, Markdown |
| `explanations/` | several | 2,532 | Markdown |
| `languages/` | 8 | 16,116 | TSG (tree-sitter-graph) |
| `tests/` | many | 934,766 | Markdown (test reports, mostly generated) |
| `build/` | 3 | 530 | Shell, Python, PyInstaller spec |

Note: `languages/` contains tree-sitter-graph rule files from the upstream
stack-graphs project (Jason Lefever's selections/modifications).
`tests/` LOC is inflated by generated test report files.

---

## 6. Interpretation

The numbers confirm the expected authorship split:

- **`src/` (Rust core):** 92.3% Jason Lefever. This is the upstream
  neodepends binary -- entity extraction, stack-graphs integration,
  dependency resolution. FreeworkEarth's 7.7% (326 lines) represents
  targeted fixes (HEAD worktree, Python config, shadow-import support).

- **`tools/` (Python toolchain):** 91.8% FreeworkEarth. This is the
  Python post-processing pipeline: `enhance_python_deps.py` (edge-schema
  v2, ImportLazy/ImportType classification, dual-scope fix),
  `neodepends_python_export.py` (DSM export), `detect_overrides.py`,
  `filter_false_positives.py`, etc. Bao Vuong contributed 8.2%
  (production UI: progress bars, error handling, `pipeline_errors.py`).

- **`examples/` + `explanations/`:** 100% FreeworkEarth. All toy
  train-ticket systems (4 variants x 2 languages), failure-mode fixtures,
  handcount benchmarks, and technical documentation.

- **`other/`:** Mixed. `languages/` TSG rules are upstream lineage (Jason
  Lefever). Build scripts, CI, README, release tooling added by
  FreeworkEarth and Bao Vuong.

**Paper claim supported:** The contribution is the Python validation
toolchain (`tools/`), cross-language toy examples (`examples/`), and
technical documentation (`explanations/`) -- all predominantly or
exclusively authored by FreeworkEarth.
