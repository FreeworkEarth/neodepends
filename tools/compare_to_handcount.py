#!/usr/bin/env python3
"""
Compare NeoDepends outputs (SQLite DBs) to hand-counted dependency totals.

This script is intentionally conservative:
- Only compares internal project relationships (File/Class/Method/Field inside the same DB).
- Uses UNIQUE edges (unique (src,tgt,kind)) rather than multiplicity.
- Compares only these kinds:
  - Import: File -> File
  - Extend: Class -> Class
  - Create: Method -> Class
  - Call: Method -> Method
  - Use: Method -> Field   (field access semantics used by our Python enhancement)
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


KINDS = ("Import", "Extend", "Create", "Call", "Use", "Parameter", "Cast")


@dataclass(frozen=True)
class HandcountTotals:
    file: str
    totals: Dict[str, int]


def _parse_handcount_file(path: Path) -> Optional[HandcountTotals]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^#\s+`([^`]+)`\s*$", text, flags=re.MULTILINE)
    if not m:
        return None
    file_name = m.group(1).strip()

    totals: Dict[str, int] = {}
    for kind in KINDS:
        mm = re.search(rf"^\-\s+{re.escape(kind)}\:\s+(\d+)\b", text, flags=re.MULTILINE)
        if mm:
            totals[kind] = int(mm.group(1))

    # Require at least one total so we don't accidentally parse README.md
    if not totals:
        return None

    # Fill missing kinds with 0
    for kind in KINDS:
        totals.setdefault(kind, 0)

    return HandcountTotals(file=file_name, totals=totals)


def load_handcounts(handcount_dir: Path) -> Dict[str, HandcountTotals]:
    out: Dict[str, HandcountTotals] = {}
    for path in sorted(handcount_dir.rglob("*.md")):
        parsed = _parse_handcount_file(path)
        if not parsed:
            continue
        out[parsed.file] = parsed
    return out


def _connect_ro(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{db_path.resolve()}?immutable=1", uri=True)


def _fetch_file_of_entity(cur: sqlite3.Cursor, entity_id: bytes) -> Optional[str]:
    # Walk parent pointers until we hit a File.
    seen: Set[bytes] = set()
    current = entity_id
    while current and current not in seen:
        seen.add(current)
        row = cur.execute("SELECT parent_id, kind, name FROM entities WHERE id = ?", (current,)).fetchone()
        if not row:
            return None
        parent_id, kind, name = row
        if kind == "File":
            return name
        current = parent_id
    return None


def compute_db_counts(
    db_path: Path,
    *,
    scope_files: Set[str],
) -> Dict[str, Dict[str, int]]:
    """
    Returns counts per source file:
      out[src_file][kind] = count
    """
    con = _connect_ro(db_path)
    cur = con.cursor()

    # Preload entity kinds for quick filtering.
    kind_by_id: Dict[bytes, str] = {}
    file_by_id: Dict[bytes, Optional[str]] = {}

    for entity_id, kind in cur.execute("SELECT id, kind FROM entities").fetchall():
        kind_by_id[entity_id] = kind

    def file_of(entity_id: bytes) -> Optional[str]:
        if entity_id in file_by_id:
            return file_by_id[entity_id]
        name = _fetch_file_of_entity(cur, entity_id)
        file_by_id[entity_id] = name
        return name

    edges_seen: Set[Tuple[bytes, bytes, str]] = set()
    out: Dict[str, Dict[str, int]] = {f: {k: 0 for k in KINDS} for f in scope_files}

    for src, tgt, dep_kind in cur.execute("SELECT src, tgt, kind FROM deps").fetchall():
        if dep_kind not in KINDS:
            continue

        src_kind = kind_by_id.get(src)
        tgt_kind = kind_by_id.get(tgt)
        if not src_kind or not tgt_kind:
            continue

        src_file = file_of(src)
        tgt_file = file_of(tgt)
        if not src_file or not tgt_file:
            continue

        if src_file not in scope_files or tgt_file not in scope_files:
            continue

        # Apply "definition-based" constraints to match our handcount semantics.
        if dep_kind == "Import":
            if not (src_kind == "File" and tgt_kind == "File"):
                continue
        elif dep_kind == "Extend":
            if not (src_kind == "Class" and tgt_kind == "Class"):
                continue
        elif dep_kind == "Create":
            if not (src_kind == "Method" and tgt_kind == "Class"):
                continue
        elif dep_kind == "Call":
            if not (src_kind == "Method" and tgt_kind == "Method"):
                continue
        elif dep_kind == "Use":
            if not (src_kind == "Method" and tgt_kind == "Field"):
                continue

        key = (src, tgt, dep_kind)
        if key in edges_seen:
            continue
        edges_seen.add(key)

        out.setdefault(src_file, {k: 0 for k in KINDS})
        out[src_file][dep_kind] += 1

    con.close()
    return out


def score_against_handcount(
    *,
    measured: Dict[str, Dict[str, int]],
    expected: Dict[str, HandcountTotals],
) -> Dict[str, Any]:
    files = sorted(set(expected.keys()) | set(measured.keys()))

    per_file: Dict[str, Any] = {}
    total_abs = 0
    total_sq = 0
    kind_abs: Dict[str, int] = {k: 0 for k in KINDS}

    for f in files:
        exp = expected.get(f).totals if f in expected else {k: 0 for k in KINDS}
        got = measured.get(f, {k: 0 for k in KINDS})

        diffs: Dict[str, int] = {}
        abs_sum = 0
        sq_sum = 0
        for k in KINDS:
            d = int(got.get(k, 0)) - int(exp.get(k, 0))
            diffs[k] = d
            abs_sum += abs(d)
            sq_sum += d * d
            kind_abs[k] += abs(d)

        total_abs += abs_sum
        total_sq += sq_sum
        per_file[f] = {"expected": exp, "measured": got, "diff": diffs, "abs_error": abs_sum, "sq_error": sq_sum}

    return {
        "total_abs_error": total_abs,
        "total_sq_error": total_sq,
        "abs_error_by_kind": kind_abs,
        "per_file": per_file,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-dir", type=Path, required=True, help="Folder containing resolver subfolders")
    parser.add_argument("--handcount-dir", type=Path, required=True, help="Folder with per-file handcount .md files")
    parser.add_argument(
        "--scope-files",
        type=str,
        default="",
        help="Comma-separated list of file paths to compare (default: infer from handcount)",
    )
    args = parser.parse_args()

    experiment_dir = args.experiment_dir.expanduser().resolve()
    handcount_dir = args.handcount_dir.expanduser().resolve()

    expected = load_handcounts(handcount_dir)
    if not expected:
        raise SystemExit(f"No handcount files found under: {handcount_dir}")

    if args.scope_files.strip():
        scope_files = {s.strip() for s in args.scope_files.split(",") if s.strip()}
    else:
        scope_files = set(expected.keys())

    resolver_dirs: List[Path] = []
    for child in sorted(experiment_dir.iterdir()):
        if not child.is_dir():
            continue
        # Prefer the primary DB produced by neodepends_python_export.py:
        #   dependencies.<tag>.filtered.db
        # and ignore raw snapshots:
        #   dependencies.<tag>.raw.db, dependencies.<tag>.raw_filtered.db
        has_db = any(
            p.is_file()
            and p.suffix == ".db"
            and (p.name.startswith("dependencies.") or p.name.startswith("dependencies_"))
            and p.name.endswith(".filtered.db")
            for p in child.iterdir()
        )
        if has_db:
            resolver_dirs.append(child)

    results: Dict[str, Any] = {
        "experiment_dir": str(experiment_dir),
        "handcount_dir": str(handcount_dir),
        "scope_files": sorted(scope_files),
        "resolvers": {},
        "best_by_abs_error": None,
    }

    best_name: Optional[str] = None
    best_abs: Optional[int] = None

    for rdir in resolver_dirs:
        name = rdir.name
        candidates = sorted(
            [
                p
                for p in rdir.iterdir()
                if p.is_file()
                and p.suffix == ".db"
                and (p.name.startswith("dependencies.") or p.name.startswith("dependencies_"))
                and p.name.endswith(".filtered.db")
            ]
        )
        if not candidates:
            continue
        db_path = candidates[0]
        measured = compute_db_counts(db_path, scope_files=scope_files)
        score = score_against_handcount(measured=measured, expected=expected)
        results["resolvers"][name] = {
            "db_path": str(db_path),
            "score": score,
        }

        if best_abs is None or score["total_abs_error"] < best_abs:
            best_abs = int(score["total_abs_error"])
            best_name = name

    results["best_by_abs_error"] = best_name

    out_path = experiment_dir / "handcount_comparison.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[OK] Wrote: {out_path}")

    if best_name is not None:
        print(f"[OK] Best (lowest total_abs_error): {best_name} = {best_abs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
