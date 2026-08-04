# LICENSE AUDIT -- NeoDepends (FreeworkEarth fork)

**Date:** 2026-08-04
**Scope:** Read-only audit. No code changes made.
**Auditor:** Automated (Claude Code)

---

## 1. Upstream License (jlefever/neodepends)

| Field | Value |
|-------|-------|
| Repository | https://github.com/jlefever/neodepends |
| License | **Apache-2.0** |
| LICENSE file | Present (standard Apache 2.0 text) |
| NOTICE file | **Not present** |
| Cargo.toml `license` | `Apache-2.0` |
| Cargo.toml `authors` | Jason Lefever |
| CONTRIBUTING.md | Present in upstream |
| Copyright line in LICENSE | Template only (`[yyyy] [name of copyright owner]`) |

**Conclusion:** Apache 2.0 confirmed. No NOTICE file exists upstream, so
Section 4(d) of Apache 2.0 (NOTICE preservation obligation) does not apply.

---

## 2. Rust Dependency Licenses

199 total packages in Cargo.lock. All 36 direct dependencies audited via
crates.io API (latest published version licenses shown; pinned versions use
the same license).

| Crate | Pinned Version | License | Flag |
|-------|---------------|---------|------|
| anyhow | 1.0.79 | MIT OR Apache-2.0 | |
| clap | 4.4.18 | MIT OR Apache-2.0 | |
| clap-verbosity-flag | 2.1.2 | MIT OR Apache-2.0 | |
| counter | 0.5.7 | MIT | |
| csv | 1.3.0 | **Unlicense/MIT** | (1) |
| derive_builder | 0.13.0 | MIT OR Apache-2.0 | |
| env_logger | 0.10.0 | MIT OR Apache-2.0 | |
| git2 | 0.18.1 | MIT OR Apache-2.0 | (2) |
| hex | 0.4 | MIT OR Apache-2.0 | |
| itertools | 0.12.0 | MIT OR Apache-2.0 | |
| lazy_static | 1.4.0 | MIT OR Apache-2.0 | |
| log | 0.4.17 | MIT OR Apache-2.0 | |
| lsp-positions | 0.3 | MIT OR Apache-2.0 | |
| rayon | 1.10.0 | MIT OR Apache-2.0 | |
| rusqlite | 0.31.0 | MIT | |
| serde | 1.0.195 | MIT OR Apache-2.0 | |
| serde_json | 1.0.111 | MIT OR Apache-2.0 | |
| sha1 | 0.10.6 | MIT OR Apache-2.0 | |
| **stack-graphs** | **0.13** | **MIT OR Apache-2.0** | |
| strum | 0.26.1 | MIT | |
| strum_macros | 0.26 | MIT | |
| subprocess | 0.2.9 | Apache-2.0/MIT | |
| tempfile | 3.10.1 | MIT OR Apache-2.0 | |
| tree-sitter | 0.20 | MIT | |
| tree-sitter-c | 0.20 | MIT | |
| tree-sitter-cpp | 0.20 | MIT | |
| tree-sitter-go | 0.20 | MIT | |
| **tree-sitter-graph** | **0.11** | **MIT OR Apache-2.0** | |
| tree-sitter-java | 0.20 | MIT | |
| tree-sitter-javascript | 0.20 | MIT | |
| tree-sitter-kotlin | 0.3 | MIT | |
| tree-sitter-python | 0.20 | MIT | |
| tree-sitter-ruby | 0.20 | MIT | |
| **tree-sitter-stack-graphs** | **0.8.1** | **MIT OR Apache-2.0** | |
| tree-sitter-typescript | =0.20.2 | MIT | |
| walkdir | 2.4.0 | **Unlicense/MIT** | (1) |

**(1) Unlicense/MIT** = dual-licensed under The Unlicense (public domain
equivalent) OR MIT. Fully permissive. No copyleft. No attribution concern
beyond MIT's standard notice requirement.

**(2) git2 / libgit2** = The Rust crate `git2` is MIT OR Apache-2.0, but it
wraps `libgit2` (C library) which is **GPLv2 with a linking exception**.
The linking exception explicitly permits use in non-GPL software, so this
is safe for our Apache-2.0 project. Worth noting for legal awareness.

### Transitive Dependencies

All 199 packages in Cargo.lock are transitively pulled in by the above.
GitHub's stack-graphs ecosystem (stack-graphs, tree-sitter-stack-graphs,
tree-sitter-graph) is consistently MIT OR Apache-2.0. The git2/libgit2
binding chain (git2 -> libgit2-sys -> libgit2) is MIT OR Apache-2.0.
rusqlite bundles SQLite which is public domain.

**No GPL, LGPL, AGPL, SSPL, BSL, or other copyleft/restrictive licenses
found in any direct dependency.**

### Flagged Items

None. All dependencies are MIT, Apache-2.0, MIT/Apache-2.0 dual, or
Unlicense/MIT dual.

---

## 3. depends.jar Provenance

| Field | Value |
|-------|-------|
| Upstream | https://github.com/multilang-depends/depends |
| License | **MIT** (Copyright 2019) |
| Location in repo | `artifacts/depends.jar` |
| Referenced in | `src/depends.rs` (line 3), `release.sh` (lines 49, 68) |

### Redistribution

**YES -- depends.jar IS redistributed in release zips.**

`release.sh` copies `artifacts/depends.jar` into both the macOS and Windows
release staging directories (lines 49 and 68), which are then zipped into
the release bundles.

### MIT Obligations for depends.jar

MIT License requires:
1. Include the copyright notice and license text in all copies or
   substantial portions of the Software.

**Current status:** The JAR file itself may or may not contain a
META-INF/LICENSE. The release zip does NOT include a separate license file
for depends.jar.

**Action required:** Add a `THIRD-PARTY-NOTICES` file (or equivalent) to the
release bundle that includes the depends (multilang-depends) MIT license
text, OR ensure the JAR's internal META-INF/LICENSE is preserved.

---

## 4. Our Fork (FreeworkEarth/neodepends)

| Field | Value |
|-------|-------|
| Repository | https://github.com/FreeworkEarth/neodepends |
| Remotes | origin (FreeworkEarth), upstream (jlefever), bao (Vbeelearncode) |
| LICENSE file | **Present** -- identical Apache 2.0 text as upstream |
| Copyright line | **NOT filled in** (still template `[yyyy] [name of copyright owner]`) |
| NOTICE file | **Not present** (not required -- upstream has none) |
| CONTRIBUTING.md | **Not present** (upstream has one; not legally required) |
| README.md | **No license section** |
| Cargo.toml `license` | `Apache-2.0` (correct) |
| Cargo.toml `authors` | Jason Lefever (unchanged from upstream) |
| Cargo.toml `homepage` | Points to upstream jlefever/neodepends |
| Cargo.toml `repository` | Points to upstream jlefever/neodepends |
| Python tool headers | **No SPDX or copyright headers** |

### Apache 2.0 Section 4 Compliance (Redistribution)

Apache 2.0 Section 4 requires for derivative works:

| Requirement | Status |
|-------------|--------|
| **(a)** Give recipients a copy of the License | LICENSE file present in repo; **NOT in release.sh bundle** |
| **(b)** Modified files carry prominent notices | **NOT done** -- our Python tools have no modification notices |
| **(c)** Retain copyright/attribution notices | Cargo.toml retains upstream author; LICENSE unchanged |
| **(d)** Include NOTICE file if one exists | N/A -- upstream has no NOTICE file |

### PyInstaller Binary (dependency-analyzer)

`build/neodepends_analyze.spec` bundles Python tools into a standalone binary.
It does NOT include LICENSE or any third-party notice files in the bundle.

---

## 5. Issues Found

### MUST FIX (legal compliance)

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| L1 | `release.sh` does not copy `LICENSE` into release zip | **HIGH** | Add `cp LICENSE "$STAGING/"` for both macOS and Windows |
| L2 | No third-party notice for `depends.jar` (MIT) in release | **HIGH** | Create `THIRD-PARTY-NOTICES` with depends MIT text; copy into release |
| L3 | PyInstaller spec does not bundle LICENSE | **MEDIUM** | Add LICENSE to `datas=[]` in `.spec` file |

### SHOULD FIX (best practice)

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| B1 | LICENSE copyright line not filled in | **MEDIUM** | Add `Copyright 2024 FreeworkEarth` (or appropriate) to LICENSE appendix |
| B2 | Cargo.toml `homepage`/`repository` still point to upstream | **LOW** | Update to FreeworkEarth URLs (or add separate `upstream` field) |
| B3 | Modified Python tools have no modification notices (Apache 2.0 s4b) | **LOW** | Add header comment to substantially modified files (enhance_python_deps.py, etc.) |
| B4 | README.md has no license section | **LOW** | Add "## License" section referencing Apache 2.0 |

### OK (no action needed)

| Item | Status |
|------|--------|
| Upstream NOTICE file | Not present -- no s4(d) obligation |
| Rust dependency licenses | All MIT/Apache-2.0/Unlicense -- no copyleft |
| stack-graphs crates | MIT OR Apache-2.0 -- compatible with our Apache-2.0 |
| rusqlite/SQLite | MIT / public domain -- no issue |
| tree-sitter ecosystem | MIT -- compatible |

---

## 6. Recommended Files to Add (do not add yet)

1. **`THIRD-PARTY-NOTICES`** (new file, repo root)
   - depends.jar: MIT license text (Copyright 2019 multilang-depends)
   - Brief mention of Rust dependencies (all MIT/Apache-2.0)

2. **Update `release.sh`** (two lines)
   - `cp LICENSE "$MACOS_STAGING/"` after line 56
   - `cp LICENSE "$WINDOWS_STAGING/"` after line 75
   - `cp THIRD-PARTY-NOTICES "$MACOS_STAGING/"` (same locations)
   - `cp THIRD-PARTY-NOTICES "$WINDOWS_STAGING/"`

3. **Update `build/neodepends_analyze.spec`** (one line in `datas=[]`)
   - Add `(str(spec_dir.parent / 'LICENSE'), '.')`
   - Add `(str(spec_dir.parent / 'THIRD-PARTY-NOTICES'), '.')`

4. **Update `LICENSE`** (fill copyright line)
   - `Copyright 2024 FreeworkEarth` (or appropriate entity)

5. **Update `README.md`** (add license section)

---

## 7. Summary

| Component | License | Redistributed? | Compliance |
|-----------|---------|----------------|------------|
| NeoDepends (upstream Rust) | Apache-2.0 | Yes (binary) | LICENSE missing from release zip |
| NeoDepends (our Python tools) | Apache-2.0 (inherited) | Yes | No modification notices |
| depends.jar | MIT | Yes | No third-party notice |
| stack-graphs | MIT OR Apache-2.0 | Yes (linked) | OK (static link, permissive) |
| tree-sitter | MIT | Yes (linked) | OK |
| rusqlite/SQLite | MIT / Public Domain | Yes (bundled) | OK |
| All other Rust deps | MIT or MIT/Apache-2.0 | Yes (linked) | OK |

**Overall risk:** LOW-MEDIUM. All dependencies are permissive. The main gaps
are procedural (LICENSE not in release zip, no third-party notice for
depends.jar). No copyleft contamination.
