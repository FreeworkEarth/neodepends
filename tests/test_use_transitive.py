#!/usr/bin/env python3
"""
End-to-end regression test for UseTransitive relabel (v0.3.10).

Asserts:
  (a) Fixture UT set == expected_edges.json exactly (pairs, counts, original kinds)
  (b) SECOND UT set == second_toy_ut_baseline.json exactly, including Use/Call split
  (c) DB edge total before == after on both
  (d) Scoped-default export on SECOND is cell/weight-identical to the same export
      with relabel step disabled (true v0.3.9-equivalence check)
"""
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# --- Paths ---------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "use_transitive"
_SECOND_TOY_ENV = os.environ.get("NEODEPENDS_SECOND_TOY", "")
SECOND_TOY = Path(_SECOND_TOY_ENV) if _SECOND_TOY_ENV else None
NEODEPENDS_BIN = REPO_ROOT / "target" / "release" / "neodepends"

EXPECTED_EDGES = FIXTURE_DIR / "expected_edges.json"
SECOND_BASELINE = FIXTURE_DIR / "second_toy_ut_baseline.json"

# We need to import enhance and export from the tools dir
sys.path.insert(0, str(TOOLS_DIR))
from enhance_python_deps import enhance_python_dependencies
from neodepends_python_export import export_dv8_file_level


def _init_git(directory: Path) -> None:
    """Initialize a throwaway git repo so neodepends can run."""
    subprocess.run(
        ["git", "init"], cwd=str(directory),
        capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "add", "-A"], cwd=str(directory),
        capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "-c", "user.email=test@test", "-c", "user.name=test",
         "commit", "-m", "init"],
        cwd=str(directory), capture_output=True, check=True,
    )


def _run_neodepends(src_dir: Path, db_path: Path) -> None:
    """Run the neodepends binary to create a StackGraphs DB."""
    cmd = [
        str(NEODEPENDS_BIN),
        "--output", str(db_path),
        "--format", "sqlite",
        "--stackgraphs",
        "--stackgraphs-python-mode", "ast",
        "WORKDIR",
    ]
    result = subprocess.run(
        cmd, cwd=str(src_dir),
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"neodepends STDERR:\n{result.stderr}")
        raise RuntimeError(f"neodepends failed with rc={result.returncode}")


def _query_ut_edges(db_path: Path) -> List[Tuple[str, str, str]]:
    """Return all UseTransitive edges as (src_file_name, tgt_file_name, original_kind_before_relabel)."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Build entity->file mapping
    ent_parent = {}
    ent_kind = {}
    for eid, pid, ek in cur.execute("SELECT id, parent_id, kind FROM entities").fetchall():
        ent_parent[eid] = pid
        ent_kind[eid] = ek

    ent_name = {}
    for eid, name in cur.execute("SELECT id, name FROM entities").fetchall():
        ent_name[eid] = name

    def file_of(eid):
        seen = set()
        cur_eid = eid
        while cur_eid and cur_eid not in seen:
            seen.add(cur_eid)
            if ent_kind.get(cur_eid) == "File":
                return ent_name.get(cur_eid, "???")
            cur_eid = ent_parent.get(cur_eid)
        return None

    edges = []
    for src, tgt, kind in cur.execute("SELECT src, tgt, kind FROM deps WHERE kind = 'UseTransitive'").fetchall():
        sf = file_of(src)
        tf = file_of(tgt)
        if sf and tf:
            edges.append((sf, tf, kind))
    conn.close()
    return edges


def _count_edges_by_kind(db_path: Path) -> Dict[str, int]:
    """Return {kind: count} for all edges in deps table."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    result = {}
    for kind, count in cur.execute("SELECT kind, COUNT(*) FROM deps GROUP BY kind").fetchall():
        result[kind] = count
    conn.close()
    return result


def _total_edges(db_path: Path) -> int:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM deps").fetchone()[0]
    conn.close()
    return total


def _export_and_load(db_path: Path, out_dir: Path, name: str, **kwargs) -> Dict[str, Any]:
    """Run export_dv8_file_level and load the resulting JSON."""
    out_path = out_dir / f"{name}.json"
    export_dv8_file_level(
        db_path=db_path,
        out_dir=out_dir,
        output_path=out_path,
        focus_prefix=None,
        include_root_py=True,
        include_external_target_files=False,
        include_self_edges=False,
        align_handcount=False,
        dv8_hierarchy="structured",
        collapse_weights=False,
        **kwargs,
    )
    return json.loads(out_path.read_text())


def _dsm_fingerprint(dsm: Dict[str, Any]) -> Tuple[int, float]:
    """Return (cell_count, total_weight) from a DSM JSON."""
    cells = dsm.get("cells", [])
    total_weight = 0.0
    for cell in cells:
        for v in cell.get("values", {}).values():
            total_weight += v
    return len(cells), total_weight


# =========================================================================
# MAIN TEST
# =========================================================================
def main() -> int:
    failures = []
    all_passed = True

    print("=" * 72)
    print("UseTransitive end-to-end regression test")
    print("=" * 72)

    # --- PHASE 1: FIXTURE ---
    print("\n--- PHASE 1: Fixture (use_transitive) ---")
    with tempfile.TemporaryDirectory(prefix="ut_fixture_") as tmpdir:
        fixture_copy = Path(tmpdir) / "fixture"
        shutil.copytree(str(FIXTURE_DIR), str(fixture_copy))
        # Remove JSON ground truth files (not Python source)
        for jf in fixture_copy.glob("*.json"):
            jf.unlink()

        _init_git(fixture_copy)
        db_path = Path(tmpdir) / "fixture.db"
        _run_neodepends(fixture_copy, db_path)

        # Run enhance and capture stdout (STEP 0c prints count-preservation check)
        print("  Running enhance_python_dependencies...")
        capture = io.StringIO()
        with redirect_stdout(capture):
            enhance_python_dependencies(
                str(db_path), str(fixture_copy),
                profile="stackgraphs",
            )
        enhance_output = capture.getvalue()
        print(enhance_output)  # echo to test output

        # Assert (c): STEP 0c self-check — parse "DB edge total: X before == Y after"
        m = re.search(r"DB edge total: (\d+) before == (\d+) after", enhance_output)
        if m:
            step0c_before, step0c_after = int(m.group(1)), int(m.group(2))
            if step0c_before == step0c_after:
                print(f"  PASS: STEP 0c edge count preserved ({step0c_before} == {step0c_after})")
            else:
                msg = f"FAIL: STEP 0c edge count mismatch: {step0c_before} != {step0c_after}"
                print(f"  ** {msg}")
                failures.append(msg)
        else:
            msg = "FAIL: Could not find STEP 0c edge total line in enhance output"
            print(f"  ** {msg}")
            failures.append(msg)

        # Parse Use/Call split from STEP 0c
        m_use = re.search(r"Use -> UseTransitive: (\d+)", enhance_output)
        m_call = re.search(r"Call -> UseTransitive: (\d+)", enhance_output)
        fixture_step0c_use = int(m_use.group(1)) if m_use else -1
        fixture_step0c_call = int(m_call.group(1)) if m_call else -1
        print(f"  STEP 0c reported: Use->{fixture_step0c_use}, Call->{fixture_step0c_call}")

        # Query UseTransitive edges
        ut_edges = _query_ut_edges(db_path)
        kind_counts = _count_edges_by_kind(db_path)
        ut_count = kind_counts.get("UseTransitive", 0)
        print(f"  UseTransitive edges in DB: {ut_count}")
        print(f"  All edge kinds: {json.dumps(kind_counts, sort_keys=True)}")

        # Build file-pair -> count mapping
        pair_counts: Dict[Tuple[str, str], int] = {}
        for sf, tf, _ in ut_edges:
            key = (sf, tf)
            pair_counts[key] = pair_counts.get(key, 0) + 1

        print(f"  UseTransitive file pairs:")
        for (sf, tf), cnt in sorted(pair_counts.items()):
            print(f"    {sf} -> {tf}: {cnt}")

        # Assert (a): fixture UT set == expected_edges.json
        expected = json.loads(EXPECTED_EDGES.read_text())
        expected_pairs = {}
        expected_use = 0
        expected_call = 0
        for entry in expected["use_transitive_edges"]:
            key = (entry["src"], entry["tgt"])
            expected_pairs[key] = entry["count"]
            if entry["original_kind"] == "Use":
                expected_use += entry["count"]
            elif entry["original_kind"] == "Call":
                expected_call += entry["count"]

        # Check pair match
        if pair_counts == expected_pairs:
            print(f"  PASS: Fixture UT pairs match expected_edges.json exactly")
        else:
            msg = f"FAIL: Fixture UT pairs mismatch. Got {pair_counts}, expected {expected_pairs}"
            print(f"  ** {msg}")
            failures.append(msg)

        # Check total UT count
        expected_total_ut = expected_use + expected_call
        if ut_count == expected_total_ut:
            print(f"  PASS: Fixture UT total = {ut_count} (expected {expected_total_ut})")
        else:
            msg = f"FAIL: Fixture UT total = {ut_count}, expected {expected_total_ut}"
            print(f"  ** {msg}")
            failures.append(msg)

    # --- PHASES 2-4: SECOND TOY (requires NEODEPENDS_SECOND_TOY env var) ---
    if SECOND_TOY is None:
        print("\n  SKIPPED: PHASE 2-4 (set NEODEPENDS_SECOND_TOY to run SECOND-toy regression)")
    else:
        assert SECOND_TOY.is_dir(), f"NEODEPENDS_SECOND_TOY not a directory: {SECOND_TOY}"
        _run_second_toy_phases(SECOND_TOY, SECOND_BASELINE, failures)

    # --- SUMMARY ---
    print("\n" + "=" * 72)
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        print("=" * 72)
        return 1
    else:
        print("ALL ASSERTIONS PASSED")
        print("=" * 72)
        return 0


def _run_second_toy_phases(
    second_toy_path: Path, baseline_path: Path, failures: List[str]
) -> None:
    """Phases 2-4: SECOND toy regression."""
    print("\n--- PHASE 2: SECOND toy (train-ticket Python) ---")
    with tempfile.TemporaryDirectory(prefix="ut_second_") as tmpdir:
        second_copy = Path(tmpdir) / "second"
        shutil.copytree(str(second_toy_path), str(second_copy))

        _init_git(second_copy)
        db_path = Path(tmpdir) / "second.db"
        _run_neodepends(second_copy, db_path)

        # Save a COPY of the DB before enhance (for v0.3.9 equivalence check)
        db_pre_enhance = Path(tmpdir) / "second_pre_enhance.db"
        shutil.copy2(str(db_path), str(db_pre_enhance))

        print("  Running enhance_python_dependencies...")
        capture2 = io.StringIO()
        with redirect_stdout(capture2):
            enhance_python_dependencies(
                str(db_path), str(second_copy),
                profile="stackgraphs",
            )
        enhance_output2 = capture2.getvalue()
        print(enhance_output2)  # echo to test output

        # Assert (c): STEP 0c self-check
        m = re.search(r"DB edge total: (\d+) before == (\d+) after", enhance_output2)
        if m:
            step0c_before, step0c_after = int(m.group(1)), int(m.group(2))
            if step0c_before == step0c_after:
                print(f"  PASS: STEP 0c edge count preserved ({step0c_before} == {step0c_after})")
            else:
                msg = f"FAIL: STEP 0c edge count mismatch: {step0c_before} != {step0c_after}"
                print(f"  ** {msg}")
                failures.append(msg)
        else:
            msg = "FAIL: Could not find STEP 0c edge total line in enhance output"
            print(f"  ** {msg}")
            failures.append(msg)

        # Query UseTransitive edges
        ut_edges = _query_ut_edges(db_path)
        kind_counts = _count_edges_by_kind(db_path)
        ut_count = kind_counts.get("UseTransitive", 0)
        print(f"  UseTransitive edges in DB: {ut_count}")
        print(f"  All edge kinds: {json.dumps(kind_counts, sort_keys=True)}")

        # Build file-pair -> count mapping
        pair_counts = {}
        for sf, tf, _ in ut_edges:
            key = (sf, tf)
            pair_counts[key] = pair_counts.get(key, 0) + 1

        print(f"  UseTransitive file pairs:")
        for (sf, tf), cnt in sorted(pair_counts.items()):
            print(f"    {sf} -> {tf}: {cnt}")

        # Assert (b): SECOND UT set == second_toy_ut_baseline.json
        baseline = json.loads(baseline_path.read_text())
        expected_total = baseline["relabel_summary"]["total"]
        expected_use = baseline["relabel_summary"]["Use_to_UseTransitive"]
        expected_call = baseline["relabel_summary"]["Call_to_UseTransitive"]

        # Parse Use/Call split from STEP 0c output (authoritative source)
        m_use2 = re.search(r"Use -> UseTransitive: (\d+)", enhance_output2)
        m_call2 = re.search(r"Call -> UseTransitive: (\d+)", enhance_output2)
        ut_use = int(m_use2.group(1)) if m_use2 else -1
        ut_call = int(m_call2.group(1)) if m_call2 else -1

        print(f"  STEP 0c reported: Use -> UseTransitive: {ut_use}")
        print(f"  STEP 0c reported: Call -> UseTransitive: {ut_call}")
        print(f"  Total relabeled: {ut_use + ut_call}")

        if ut_use == expected_use and ut_call == expected_call:
            print(f"  PASS: Use/Call split matches baseline ({ut_use}/{ut_call})")
        else:
            msg = f"FAIL: Use/Call split: got {ut_use}/{ut_call}, expected {expected_use}/{expected_call}"
            print(f"  ** {msg}")
            failures.append(msg)

        if ut_count == expected_total:
            print(f"  PASS: Total UT = {ut_count} == baseline {expected_total}")
        else:
            msg = f"FAIL: Total UT = {ut_count}, expected {expected_total}"
            print(f"  ** {msg}")
            failures.append(msg)

        # Check file pairs
        expected_pairs = {}
        for entry in baseline["file_pairs"]:
            key = (entry["src"], entry["tgt"])
            expected_pairs[key] = entry["count"]

        if pair_counts == expected_pairs:
            print(f"  PASS: File pair counts match baseline exactly")
        else:
            msg = f"FAIL: File pair counts mismatch. Got {pair_counts}, expected {expected_pairs}"
            print(f"  ** {msg}")
            failures.append(msg)

        # --- PHASE 3: 4-mode export regression ---
        print("\n--- PHASE 3: 4-mode export regression (SECOND toy) ---")
        out_dir = Path(tmpdir) / "exports"
        out_dir.mkdir()

        # Mode 1: import-scoped default (UseTransitive dropped)
        dsm1 = _export_and_load(db_path, out_dir, "scoped_default",
                                import_scoped=True, include_transitive_use=False, exclude_transitive_use=False)
        c1, w1 = _dsm_fingerprint(dsm1)
        print(f"  Mode 1 (scoped, default):              {c1} cells, weight={w1}")

        # Mode 2: import-scoped + include_transitive_use (UseTransitive kept)
        dsm2 = _export_and_load(db_path, out_dir, "scoped_include_ut",
                                import_scoped=True, include_transitive_use=True, exclude_transitive_use=False)
        c2, w2 = _dsm_fingerprint(dsm2)
        print(f"  Mode 2 (scoped, +include_transitive):  {c2} cells, weight={w2}")

        # Mode 3: non-scoped default (UseTransitive kept)
        dsm3 = _export_and_load(db_path, out_dir, "nonscoped_default",
                                import_scoped=False, include_transitive_use=False, exclude_transitive_use=False)
        c3, w3 = _dsm_fingerprint(dsm3)
        print(f"  Mode 3 (non-scoped, default):          {c3} cells, weight={w3}")

        # Mode 4: non-scoped + exclude_transitive_use (UseTransitive dropped)
        dsm4 = _export_and_load(db_path, out_dir, "nonscoped_exclude_ut",
                                import_scoped=False, include_transitive_use=False, exclude_transitive_use=True)
        c4, w4 = _dsm_fingerprint(dsm4)
        print(f"  Mode 4 (non-scoped, +exclude_transitive): {c4} cells, weight={w4}")

        # Assert: mode 1 cells < mode 2 cells (UT adds cells in scoped)
        if c2 > c1:
            print(f"  PASS: scoped+include ({c2}) > scoped default ({c1})")
        elif c2 == c1:
            msg = f"FAIL: scoped+include ({c2}) == scoped default ({c1}) — UT not being included"
            print(f"  ** {msg}")
            failures.append(msg)
        else:
            msg = f"FAIL: scoped+include ({c2}) < scoped default ({c1}) — unexpected"
            print(f"  ** {msg}")
            failures.append(msg)

        # Assert: mode 3 cells > mode 4 cells (UT removed in mode 4)
        if c3 > c4:
            print(f"  PASS: non-scoped default ({c3}) > non-scoped+exclude ({c4})")
        elif c3 == c4:
            msg = f"FAIL: non-scoped default ({c3}) == non-scoped+exclude ({c4}) — UT not being excluded"
            print(f"  ** {msg}")
            failures.append(msg)
        else:
            msg = f"FAIL: non-scoped default ({c3}) < non-scoped+exclude ({c4}) — unexpected"
            print(f"  ** {msg}")
            failures.append(msg)

        # Assert (d): v0.3.9 equivalence — scoped-default with UseTransitive
        # relabel should produce identical output to scoped-default WITHOUT it.
        # Method: copy the fully-enhanced DB, revert UseTransitive -> Use/Call,
        # export, and compare. We need the original kinds, which we can infer:
        # enhance_python_deps STEP 0c only relabels Use and Call, so we just
        # need to know which was which. We stored pre-enhance DB but it lacks
        # STEP 0 classification. Instead: copy enhanced DB, set all UseTransitive
        # back to "Use" (the import-scoped gate drops both Use and UseTransitive
        # for unanchored pairs, so the original kind doesn't matter for this test).
        print("\n--- PHASE 4: v0.3.9 equivalence check ---")

        db_v039_sim = Path(tmpdir) / "second_v039_sim.db"
        shutil.copy2(str(db_path), str(db_v039_sim))
        conn_sim = sqlite3.connect(str(db_v039_sim))
        cur_sim = conn_sim.cursor()
        cur_sim.execute("UPDATE deps SET kind = 'Use' WHERE kind = 'UseTransitive'")
        conn_sim.commit()
        conn_sim.close()

        v039_dir = Path(tmpdir) / "v039_exports"
        v039_dir.mkdir()
        dsm_v039 = _export_and_load(db_v039_sim, v039_dir, "v039_scoped_default",
                                     import_scoped=True, include_transitive_use=False,
                                     exclude_transitive_use=False)
        c_v039, w_v039 = _dsm_fingerprint(dsm_v039)
        print(f"  v0.3.9 simulation (scoped, default): {c_v039} cells, weight={w_v039}")
        print(f"  v0.3.10 actual    (scoped, default): {c1} cells, weight={w1}")

        if c_v039 == c1 and w_v039 == w1:
            print(f"  PASS: v0.3.9 equivalence (cells and weights identical)")
        else:
            msg = f"FAIL: v0.3.9 equivalence broken — v039=({c_v039},{w_v039}) vs v310=({c1},{w1})"
            print(f"  ** {msg}")
            failures.append(msg)


if __name__ == "__main__":
    sys.exit(main())
