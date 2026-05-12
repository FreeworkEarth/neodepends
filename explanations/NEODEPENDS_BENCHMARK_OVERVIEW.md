# NeoDepends Python Benchmark Overview

This file tracks all Python dependency extraction benchmarks run against NeoDepends,
with absolute numbers, percentages, and the exact terminal commands to reproduce each run.

Last updated: 2026-05-12

---

## Benchmark 1: TrainTicketSystem TOY -- Python FIRST (God Class Anti-Pattern)

### Project info

| Property | Value |
|----------|-------|
| Path | `TEST_AUTO/000_TOY_EXAMPLES/ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG/python/first_godclass_antipattern/` |
| Language | Python 3.11+ |
| Files | 12 (1 main.py + 11 tts/*.py) |
| Architecture | God class anti-pattern (intentional) |
| Ground truth | `DEPS_GROUND_TRUTH_HANDCOUNT/python/first_godclass_antipattern/DEPS__GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json` |

### Ground truth counts

| Kind | Count |
|------|-------|
| Import | 86 |
| Extend | 3 |
| Create | 26 |
| Call | 110 |
| Use | 92 |
| **Total edges** | **317** |
| **File-pairs (GT)** | **36** |

### NeoDepends results (current -- with field type inference)

| Metric | Value |
|--------|-------|
| File-pairs detected | 35 |
| File-pairs in GT | 36 |
| True positives | 33 |
| False positives | 2 (pre-existing StackGraphs -- not from our patterns) |
| False negatives | 3 |
| **File-pair Recall** | **91.7%** (33/36) |
| **File-pair Precision** | **94.3%** (33/35) |
| **File-pair Jaccard** | **86.8%** |
| Entity Jaccard | 89.4% |
| Entity Precision | 96.1% |

### Remaining 3 false-negative file-pairs

| Missing pair | Root cause | Fixable without runtime? |
|-------------|-----------|--------------------------|
| `ticket.py -> train_station.py` | `display_ticket` calls `self.route.get_origin().get_name()` -- 2-hop method return type | Hard (no `-> TrainStation` annotation, param name doesn't hint type) |
| `ticket_booking_system.py -> person.py` | `passenger.name` where `name` is inherited from `Person` -- requires var-type inference + inheritance traversal | Hard (2-hop) |
| `train_station.py -> route.py` | `train.route.destination` accessed as `var.field.field` chain | Hard (2-hop) |

### Run commands

**Full pipeline (re-run extraction + export):**
```bash
cd "TEST_AUTO/000_TOY_EXAMPLES/ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG/python/first_godclass_antipattern"
python3 "../../../../00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/neodepends/tools/neodepends_python_export.py" \
  --input . \
  --output-dir /tmp/toy_first_run \
  --full-dv8 --align-handcount --dv8-hierarchy handcount --config python
```

**Compare to ground truth:**
```bash
python3 "DEPS_GROUND_TRUTH_HANDCOUNT/python/first_godclass_antipattern/DEPS__GROUND_TRUTH_HANDCOUNT/compare_neodepends_to_ground_truth.py" \
  --project-root . \
  --ground-truth "DEPS_GROUND_TRUTH_HANDCOUNT/python/first_godclass_antipattern/DEPS__GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json" \
  --neodepends-dv8 /tmp/toy_first_run/dependencies.full.dv8-dependency.json
```

---

## Benchmark 2: Survey System -- Python

### Project info

| Property | Value |
|----------|-------|
| Path | `TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/examples_readmy_python/survey-testing-neodepends-main/Survey-Python/src/` |
| Language | Python 3.x |
| Files | 21 (src/*.py) |
| Architecture | Survey/Quiz system with abstract question hierarchy |
| Ground truth | None (qualitative check only -- no formal GT yet) |

### Project characteristics

- 23 classes (6 concrete Question subclasses, Menu hierarchy, Survey/Test hierarchy, Serializer, Tabulator, Grader)
- Strong constructor injection pattern: `SurveyMenu` creates `Serializer()`, `Tabulator()`; `TestMenu` creates `Grader()`
- No type hints on injected fields -- tests name-convention inference
- Parallel Java version exists for cross-language comparison

### NeoDepends results (qualitative -- 2026-05-11)

| Metric | Value |
|--------|-------|
| Files | 21 |
| Classes | 22 |
| Methods | 147 |
| Total deps extracted | Call: 1130, Create: 35, Extend: 20, Import: 179, Override: 26, Use: 575 |
| File-pairs detected | 82 |
| Key injection pairs detected | All |

**Key file-pair edges confirmed detected:**

| Pair | Expected | Detected |
|------|----------|----------|
| `survey_menu.py -> serializer.py` | Yes | Yes |
| `survey_menu.py -> tabulator.py` | Yes | Yes |
| `test_menu.py -> grader.py` | Yes | Yes |
| `test_menu.py -> serializer.py` | Yes | Yes |
| `test_menu.py -> tabulator.py` | Yes | Yes |
| `tabulator.py -> serializer.py` | Yes | Yes |

No unexpected FPs observed (all detected edges are architecturally meaningful).

### Run command

```bash
cd "TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/neodepends"
python3 tools/neodepends_python_export.py \
  --input "examples_readmy_python/survey-testing-neodepends-main/Survey-Python/src" \
  --output-dir /tmp/survey_neodepends_out \
  --full-dv8 --align-handcount --dv8-hierarchy handcount --config python
```

---

## Benchmark 3: ARCH_AGENT

### Project info

| Property | Value |
|----------|-------|
| Path | `AGENT/ARCH_AGENT/` |
| Language | Python 3.11+ |
| Files | 29 (across 3 stage subdirectories) |
| Architecture | 3-stage pipeline: analyze -> interpret -> query/RAG |
| Ground truth | `AGENT/ARCH_AGENT/DEPS_GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json` |

### Ground truth counts (updated 2026-05-12)

| Kind | Count |
|------|-------|
| Import | 18 (was 14 -- 4 late imports found by NeoDepends were missing from GT) |
| Create | 4 |
| Call | 28 |
| Use | 3 |
| **Total edges** | **53** |
| **File-pairs (GT)** | **18** |

**4 GT misses corrected**: `backfill_temporal_payloads.py -> generate_hotspot_csv.py`,
`backfill_temporal_payloads.py -> export_dv8_binary_files.py`,
`temporal_analyzer.py -> metric_plotter.py`, `compute_file_risk_scores.py -> llm_backend.py`
-- all confirmed as real late imports inside functions (verified in source).

### NeoDepends results (2026-05-12)

| Metric | Value |
|--------|-------|
| Files | 29 |
| Classes | 8 |
| Methods | 26 |
| Total deps extracted | Call: 853+, Create: 27, Import: **18**, Use: 172+ |
| File-pairs detected (DSM) | **18** |
| File-pairs in GT | **18** |
| True positives | **18** |
| False positives | **0** |
| False negatives | **0** |
| **File-pair Recall** | **100%** |
| **File-pair Precision** | **100%** |

**Note on previous session**: A comparison script bug caused a false "0% DSM recall" reading --
the script extracted file names from variables like `01_stage_analyze/foo.py/module (Module)`
incorrectly, splitting on `/` and only taking the first part. The DSM export was always correct.
The 4 "FPs" were actually real imports missing from the GT.

### GT file-pairs (all detected)

| File-pair | Import kind |
|-----------|------------|
| `temporal_analyzer.py -> dv8_agent.py` | Import |
| `compare_dependency_extractors.py -> dv8_agent.py` | Import |
| `run_extractor_benchmark.py -> dv8_agent.py` | Import |
| `backfill_temporal_payloads.py -> mscore_dv8_exact.py` | Import |
| `backfill_temporal_payloads.py -> generate_hotspot_csv.py` | Import (late) |
| `backfill_temporal_payloads.py -> export_dv8_binary_files.py` | Import (late) |
| `temporal_analyzer.py -> mscore_dv8_exact.py` | Import |
| `temporal_analyzer.py -> metric_plotter.py` | Import (late) |
| `build_risk_calibration_dataset.py -> compute_file_risk_scores.py` | Import |
| `compute_file_risk_scores.py -> llm_backend.py` | Import (late) |
| `interpret_metrics.py -> commit_analyzer.py` | Import |
| `interpret_drh_diff.py -> commit_analyzer.py` | Import (late) |
| `interpret_drh_diff.py -> compute_evidence_graph_diff.py` | Import (late) |
| `interpret_drh_diff.py -> llm_backend.py` | Import (late) |
| `interpret_temporal_bundle.py -> llm_backend.py` | Import (late) |
| `query_engine.py -> llm_backend.py` | Import |
| `query_engine.py -> rag_index.py` | Import |
| `dv8_agent.py -> generate_hotspot_csv.py` | Import |

### Run commands

**Step 1 -- run NeoDepends binary directly:**
```bash
NEODEPENDS_BIN="TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/neodepends/target/release/neodepends"
"$NEODEPENDS_BIN" --input ARCH_AGENT --output ~/tmp/arch_agent_deps.db --langs python
```

**Step 2 -- run enhance (adds Import + Use edges):**
```bash
python3 "TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/neodepends/tools/enhance_python_deps.py" \
  ~/tmp/arch_agent_deps.db ARCH_AGENT/
```

**Step 3 -- export file-level DSM:**
```bash
python3 - <<'EOF'
import sys, json
sys.path.insert(0, "TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/neodepends/tools")
from pathlib import Path
from neodepends_python_export import export_dv8_file_level
export_dv8_file_level(
    db_path=Path("/Users/chrisharing/tmp/arch_agent_deps.db"),
    out_dir=Path("/Users/chrisharing/tmp/arch_agent_dsm"),
    focus_prefix=None, include_root_py=False,
    include_external_target_files=False, include_self_edges=False,
    align_handcount=True, dv8_hierarchy="handcount", collapse_weights=True,
)
data = json.loads(Path("/Users/chrisharing/tmp/arch_agent_dsm/dependencies.dv8-dependency.json").read_text())
variables = data["variables"]
for c in data["cells"]:
    print(variables[c["src"]], "->", variables[c["dest"]])
EOF
```

---

## Summary table (all benchmarks)

| Repo | Files | GT file-pairs | TP | FP | FN | Recall | Precision | Jaccard | Note |
|------|-------|--------------|----|----|-----|--------|-----------|---------|------|
| Toy Python FIRST | 12 | 36 | 33 | 2 | 3 | **91.7%** | 94.3% | 86.8% | 2 FPs are pre-existing StackGraphs; 3 FNs need interprocedural tracking |
| Survey Python | 21 | -- (no GT) | -- | 0 | -- | -- | -- | -- | All key pairs detected |
| ARCH_AGENT | 29 | 18 | 18 | 0 | 0 | **100%** | **100%** | **100%** | Includes late imports inside functions |

---

## Known issues / open work

### 1. Toy FIRST: 3 remaining false-negative file-pairs

All require 2-hop interprocedural reasoning that is fundamentally hard without type annotations or runtime info:

1. `ticket.py -> train_station.py` -- `self.route.get_origin()` where `get_origin()` returns a `TrainStation`, but there's no `-> TrainStation` annotation and `origin` param doesn't hint at the type
2. `ticket_booking_system.py -> person.py` -- `passenger.name` where `name` is inherited from `Person`; requires var-type inference + inheritance traversal
3. `train_station.py -> route.py` -- `train.route.destination` accessed as `var.field.field` chain

**Stage 2 (implemented 2026-05-12)**: Method return-type inference is now in `enhance_python_deps.py`.
It handles `-> ClassName` annotations and `return self.field` patterns. Doesn't close these
3 FNs because the toy's param names (`origin`, `destination`) don't map to class names.
Helps on real-world codebases with proper type annotations.

### 2. Survey Python: no formal ground truth

The Survey project has no `handcount_edges.heuristic.json`. Creating one would give us a
proper second benchmark. Estimated: ~2h effort (~23 classes, known architecture).
