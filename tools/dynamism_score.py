#!/usr/bin/env python3
"""dynamism_score.py — extractability/dynamism score from NeoDepends output.

Input:  A NeoDepends dv8-dependency JSON (file-level edge list).
Output: JSON + stdout summary of edge composition by import category.

Thresholds (provisional):
    >= 90% eager-static  -> HIGH extraction confidence
    75-90%               -> MEDIUM
    < 75%                -> LOW

CAVEAT: composition covers OBSERVED edges only; truly invisible edges
(e.g. getattr-based dynamic attribute access with no import statement)
are not countable here.  See the mechanism-coverage table
(planted-fixture benchmark in PYTHON_FAILURE_MODES.md) for
known-mechanism recall.

v0.3.10 development — NeoDepends (FreeworkEarth fork)
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _categorize_edge(kind: str) -> str:
    """Map an edge kind to a dynamism category."""
    k = kind.strip()
    if k == "Import":
        return "eager-static"
    if k == "ImportLazy":
        return "deferred"
    if k == "ImportType":
        return "type-only"
    # Future: importlib tags, __import__, etc.
    if "dynamic" in k.lower() or "importlib" in k.lower():
        return "dynamic-mechanism"
    # Non-import edges (Use, Call, Create, Extend, Contain, etc.)
    return "non-import"


def _is_import_edge(category: str) -> bool:
    return category in ("eager-static", "deferred", "type-only", "dynamic-mechanism", "mixed")


def compute_dynamism_score(edges: List[Tuple[str, str, str]]) -> Dict[str, Any]:
    """Compute the dynamism/extractability score.

    Args:
        edges: list of (src, tgt, kind) triples

    Returns:
        dict with counts, percentages, file-level stats, verdict
    """
    cat_counter = Counter()
    file_has_non_eager = set()
    all_src_files = set()

    for src, tgt, kind in edges:
        cat = _categorize_edge(kind)
        cat_counter[cat] += 1

        # Extract file from variable path (e.g. "foo.py/module (Module)" -> "foo.py")
        src_file = src.split("/")[0] if "/" in src else src
        all_src_files.add(src_file)

        if _is_import_edge(cat) and cat != "eager-static":
            file_has_non_eager.add(src_file)

    # Separate import vs non-import
    import_cats = ["eager-static", "deferred", "type-only", "dynamic-mechanism", "mixed"]
    import_total = sum(cat_counter[c] for c in import_cats)
    total_edges = sum(cat_counter.values())

    # Percentages (of import edges only)
    pct = {}
    for c in import_cats:
        pct[c] = (cat_counter[c] * 100.0 / import_total) if import_total > 0 else 0.0

    eager_pct = pct.get("eager-static", 0.0)

    # Verdict
    if eager_pct >= 90.0:
        verdict = "HIGH"
    elif eager_pct >= 75.0:
        verdict = "MEDIUM"
    else:
        verdict = "LOW"

    # File-level stat
    files_with_non_eager = len(file_has_non_eager)
    total_files = len(all_src_files)
    file_non_eager_pct = (files_with_non_eager * 100.0 / total_files) if total_files > 0 else 0.0

    return {
        "total_edges": total_edges,
        "import_edges": import_total,
        "non_import_edges": cat_counter.get("non-import", 0),
        "by_category": {c: cat_counter[c] for c in import_cats if cat_counter[c] > 0},
        "by_category_pct": {c: round(pct[c], 1) for c in import_cats if cat_counter[c] > 0},
        "eager_static_pct": round(eager_pct, 1),
        "files_total": total_files,
        "files_with_non_eager_import": files_with_non_eager,
        "files_non_eager_pct": round(file_non_eager_pct, 1),
        "verdict": verdict,
        "verdict_line": (
            f"{eager_pct:.1f}% of observed import edges are eager-static; "
            f"extraction confidence {verdict}"
        ),
        "caveat": (
            "Composition covers OBSERVED edges only; truly invisible edges "
            "are not countable here -- see the mechanism-coverage table "
            "(planted-fixture benchmark) for known-mechanism recall."
        ),
    }


def load_edges_from_dv8_dep(path: Path) -> List[Tuple[str, str, str]]:
    """Load edges from a dv8-dependency JSON (the handcount format)."""
    with open(path) as f:
        data = json.load(f)

    # Format: list of [src, tgt, kind] triples
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        return [(e[0], e[1], e[2]) for e in data if len(e) >= 3]

    # Alternative: {"cells": [...]} DV8 DSM format
    if isinstance(data, dict) and "cells" in data:
        variables = data.get("variables", [])
        edges = []
        for cell in data["cells"]:
            src_idx = cell.get("src", 0)
            tgt_idx = cell.get("dest", 0)
            values = cell.get("values", {})
            for kind in values:
                src = variables[src_idx] if src_idx < len(variables) else str(src_idx)
                tgt = variables[tgt_idx] if tgt_idx < len(variables) else str(tgt_idx)
                edges.append((src, tgt, kind))
        return edges

    raise ValueError(f"Unrecognized edge format in {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compute dynamism/extractability score from NeoDepends output"
    )
    parser.add_argument("input", type=Path, help="Path to dv8-dependency JSON or handcount JSON")
    parser.add_argument("--json", type=Path, help="Write JSON output to file")
    args = parser.parse_args()

    edges = load_edges_from_dv8_dep(args.input)
    result = compute_dynamism_score(edges)

    # Print summary
    print(f"=== Dynamism / Extractability Score ===")
    print(f"Input: {args.input}")
    print(f"Total edges: {result['total_edges']} ({result['import_edges']} import, "
          f"{result['non_import_edges']} non-import)")
    print()
    print("Import edge composition:")
    for cat, count in sorted(result["by_category"].items(), key=lambda x: -x[1]):
        pct = result["by_category_pct"][cat]
        print(f"  {cat:20s}  {count:4d}  ({pct:5.1f}%)")
    print()
    print(f"Files with non-eager imports: {result['files_with_non_eager_import']} / "
          f"{result['files_total']} ({result['files_non_eager_pct']:.1f}%)")
    print()
    print(f"VERDICT: {result['verdict_line']}")
    print()
    print(f"CAVEAT: {result['caveat']}")

    if args.json:
        with open(args.json, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nJSON written to {args.json}")


if __name__ == "__main__":
    main()
