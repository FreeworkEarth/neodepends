#!/usr/bin/env python3
"""mypy_oracle.py — 4th ruler: mypy import graph vs NeoDepends.

Uses mypy's build API to extract the full import graph for a Python
package, then diffs it against a handcount (ground truth) and/or
NeoDepends output at file-level granularity.

For each edge disagreement, produces a per-edge verdict:
  AGREE             both mypy and handcount see the edge
  NEO_BUG           NeoDepends reports an edge the handcount does NOT have
  NEO_MISS          handcount has the edge, NeoDepends does not
  MYPY_BLIND        handcount has the edge but mypy cannot see it
  MAPPING_ARTIFACT  mypy sees it, handcount says no (module-mapping noise)

Pinned config:
  mypy >= 2.3.0
  --follow-imports normal
  --no-implicit-reexport

v0.3.10 development — NeoDepends (FreeworkEarth fork)
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# mypy priority constants (from mypy/build.py)
# ---------------------------------------------------------------------------
PRI_HIGH = 5       # top-level "import mod" or "from mod import x"
PRI_MED = 10       # from mod import * (or star-import level)
PRI_LOW = 20       # package __init__ reference, lazy, or re-export
PRI_MYPY = 25      # TYPE_CHECKING / if False guarded
PRI_INDIRECT = 30  # implicit / transitive (no import statement)

MYPY_VERSION_PINNED = "2.3.0"


# ---------------------------------------------------------------------------
# mypy build API
# ---------------------------------------------------------------------------

def run_mypy_graph(target_dir: Path, package: str,
                   main_file: Optional[str] = None) -> Dict[str, Any]:
    """Run mypy.build.build() and extract the import graph.

    Returns metadata dict plus raw graph keyed by module ID.
    """
    try:
        import mypy
        from mypy import build
        from mypy.fscache import FileSystemCache
        from mypy.options import Options
    except ImportError:
        print("ERROR: mypy not installed. Install with: pip install mypy",
              file=sys.stderr)
        sys.exit(1)

    try:
        from mypy.version import __version__ as actual_version
    except ImportError:
        actual_version = getattr(mypy, "__version__", "unknown")

    opts = Options()
    opts.follow_imports = "normal"
    opts.implicit_reexport = False
    opts.incremental = False
    opts.cache_dir = "/dev/null"
    # Add target directory to mypy's search path so it can find the package
    opts.mypy_path = [str(target_dir)]

    # Build from entry point(s)
    sources = []
    main_module = None
    if main_file:
        main_path = target_dir / main_file
        main_module = main_file.replace(".py", "").replace("/", ".")
        if main_path.exists():
            sources.append(build.BuildSource(str(main_path), main_module, None))

    fscache = FileSystemCache()

    try:
        result = build.build(sources=sources, options=opts, fscache=fscache)
    except Exception as e:
        print(f"ERROR: mypy build failed: {e}", file=sys.stderr)
        sys.exit(1)

    graph_data = {}
    for mod_id, state in result.graph.items():
        deps = []
        for dep_id in state.dependencies:
            pri = state.priorities.get(dep_id, PRI_INDIRECT)
            deps.append((dep_id, pri))
        graph_data[mod_id] = {
            "path": state.path or "",
            "deps": deps,
        }

    return {
        "mypy_version": actual_version,
        "pinned_version": MYPY_VERSION_PINNED,
        "follow_imports": "normal",
        "implicit_reexport": False,
        "total_modules": len(result.graph),
        "main_module": main_module,
        "graph": graph_data,
    }


# ---------------------------------------------------------------------------
# module -> file mapping
# ---------------------------------------------------------------------------

def _module_to_relfile(mod_id: str, graph_data: dict,
                       target_dir: Path) -> Optional[str]:
    """Map a mypy module ID to a relative file path."""
    info = graph_data.get(mod_id)
    if not info or not info["path"]:
        return None
    abs_path = Path(info["path"])
    try:
        return str(abs_path.relative_to(target_dir))
    except ValueError:
        return None  # stdlib or outside target


# ---------------------------------------------------------------------------
# extract mypy edges
# ---------------------------------------------------------------------------

def extract_mypy_file_edges(
    graph_data: dict,
    target_dir: Path,
    package: str,
    main_module: Optional[str] = None,
) -> List[Tuple[str, str, int, str]]:
    """Extract file-level import edges from mypy graph.

    Returns (src_file, dst_file, priority, category) tuples.
    Skips implicit/transitive (pri >= 30) and stdlib edges.
    """

    def _is_project(mid: str) -> bool:
        if mid == package or mid.startswith(package + "."):
            return True
        if main_module and mid == main_module:
            return True
        return False

    def _priority_category(pri: int) -> str:
        if pri <= PRI_MED:
            return "eager-static"
        if pri <= PRI_LOW:
            return "package-ref"
        if pri <= PRI_MYPY:
            return "type-only"
        return "implicit"

    edges = []
    for mod_id, info in graph_data.items():
        if not _is_project(mod_id):
            continue

        src_file = _module_to_relfile(mod_id, graph_data, target_dir)
        if not src_file:
            continue

        for dep_id, pri in info["deps"]:
            if not _is_project(dep_id):
                continue
            if pri >= PRI_INDIRECT:
                continue

            dst_file = _module_to_relfile(dep_id, graph_data, target_dir)
            if not dst_file:
                continue
            if src_file == dst_file:
                continue

            cat = _priority_category(pri)
            edges.append((src_file, dst_file, pri, cat))

    return edges


# ---------------------------------------------------------------------------
# handcount / NeoDepends loaders
# ---------------------------------------------------------------------------

def _extract_file(entity_path: str) -> str:
    """Extract file path from entity path.

    "tts/booking_service.py/module (Module)" -> "tts/booking_service.py"
    "tts/providers/__init__.py/module (Module)" -> "tts/providers/__init__.py"
    """
    m = re.match(r"^(.*?\.py)", entity_path)
    return m.group(1) if m else entity_path


def load_handcount_edges(path: Path) -> List[Tuple[str, str, str]]:
    """Load import edges from handcount edge-list JSON.

    Extracts Import/ImportLazy/ImportType, collapses to file level.
    """
    with open(path) as f:
        data = json.load(f)

    import_kinds = {"Import", "ImportLazy", "ImportType"}
    seen: Set[Tuple[str, str]] = set()
    edges: List[Tuple[str, str, str]] = []

    for edge in data:
        src_ent, dst_ent, kind = edge[0], edge[1], edge[2]
        if kind not in import_kinds:
            continue

        src_file = _extract_file(src_ent)
        dst_file = _extract_file(dst_ent)

        key = (src_file, dst_file)
        if key not in seen:
            seen.add(key)
            edges.append((src_file, dst_file, kind))

    return edges


def load_neo_edges(path: Path) -> List[Tuple[str, str, str]]:
    """Load import edges from NeoDepends output (edge-list or DSM JSON)."""
    with open(path) as f:
        data = json.load(f)

    import_kinds = {"Import", "ImportLazy", "ImportType"}

    # Edge list format: [[src, tgt, kind], ...]
    if isinstance(data, list) and data and isinstance(data[0], list):
        seen: Set[Tuple[str, str]] = set()
        edges: List[Tuple[str, str, str]] = []
        for e in data:
            if len(e) >= 3 and e[2] in import_kinds:
                sf = _extract_file(e[0])
                df = _extract_file(e[1])
                key = (sf, df)
                if key not in seen:
                    seen.add(key)
                    edges.append((sf, df, e[2]))
        return edges

    # DSM format: {"variables": [...], "cells": [...]}
    if isinstance(data, dict) and "cells" in data:
        variables = data.get("variables", [])
        seen2: Set[Tuple[str, str]] = set()
        edges2: List[Tuple[str, str, str]] = []
        for cell in data["cells"]:
            si = cell.get("src", 0)
            di = cell.get("dest", 0)
            for kind in cell.get("values", {}):
                if kind in import_kinds:
                    sv = variables[si] if si < len(variables) else str(si)
                    dv = variables[di] if di < len(variables) else str(di)
                    sf = _extract_file(sv)
                    df = _extract_file(dv)
                    key = (sf, df)
                    if key not in seen2:
                        seen2.add(key)
                        edges2.append((sf, df, kind))
        return edges2

    raise ValueError(f"Unrecognized format in {path}")


# ---------------------------------------------------------------------------
# diff + arbitration
# ---------------------------------------------------------------------------

def diff_and_arbitrate(
    mypy_edges: List[Tuple[str, str, int, str]],
    handcount_edges: List[Tuple[str, str, str]],
    neo_edges: Optional[List[Tuple[str, str, str]]] = None,
) -> Dict[str, Any]:
    """Diff mypy vs handcount (and optionally NeoDepends), produce verdicts."""

    mypy_set = {(s, d) for s, d, _, _ in mypy_edges}
    mypy_detail = {(s, d): {"priority": p, "category": c}
                   for s, d, p, c in mypy_edges}

    hc_set = {(s, d) for s, d, _ in handcount_edges}
    hc_detail = {(s, d): k for s, d, k in handcount_edges}

    neo_set: Set[Tuple[str, str]] = set()
    neo_detail: Dict[Tuple[str, str], str] = {}
    if neo_edges is not None:
        neo_set = {(s, d) for s, d, _ in neo_edges}
        neo_detail = {(s, d): k for s, d, k in neo_edges}

    all_edges = mypy_set | hc_set | neo_set

    verdicts = []
    for edge in sorted(all_edges):
        src, dst = edge
        in_mypy = edge in mypy_set
        in_hc = edge in hc_set
        in_neo = edge in neo_set if neo_edges is not None else None

        # Determine verdict
        if in_mypy and in_hc:
            if in_neo is None or in_neo:
                verdict = "AGREE"
            else:
                verdict = "NEO_MISS"
        elif in_mypy and not in_hc:
            verdict = "MAPPING_ARTIFACT"
        elif not in_mypy and in_hc:
            verdict = "MYPY_BLIND"
        else:
            # not in mypy, not in handcount
            if in_neo:
                verdict = "NEO_BUG"
            else:
                continue

        entry = {
            "src": src,
            "dst": dst,
            "verdict": verdict,
            "in_mypy": in_mypy,
            "in_handcount": in_hc,
            "handcount_kind": hc_detail.get(edge, ""),
            "mypy_priority": mypy_detail.get(edge, {}).get("priority"),
            "mypy_category": mypy_detail.get(edge, {}).get("category", ""),
        }
        if neo_edges is not None:
            entry["in_neo"] = in_neo
            entry["neo_kind"] = neo_detail.get(edge, "")

        verdicts.append(entry)

    verdict_counts = defaultdict(int)
    for v in verdicts:
        verdict_counts[v["verdict"]] += 1

    return {
        "mypy_edge_count": len(mypy_set),
        "handcount_edge_count": len(hc_set),
        "neo_edge_count": len(neo_set) if neo_edges is not None else None,
        "verdict_counts": dict(verdict_counts),
        "verdicts": verdicts,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Mypy oracle: compare mypy import graph against "
                    "NeoDepends/handcount"
    )
    parser.add_argument("--target", type=Path, required=True,
                        help="Project root (contains package dir and/or main.py)")
    parser.add_argument("--package", type=str, required=True,
                        help="Package name (e.g. 'tts')")
    parser.add_argument("--main", type=str, default=None,
                        help="Main file relative to target (e.g. 'main.py')")
    parser.add_argument("--handcount", type=Path, required=True,
                        help="Handcount edges JSON (entity-level edge list)")
    parser.add_argument("--neo", type=Path, default=None,
                        help="NeoDepends output (edge list or DSM JSON)")
    parser.add_argument("--json", type=Path, default=None,
                        help="Write JSON output to file")
    args = parser.parse_args()

    # --- 1. Run mypy ---
    print("=== Mypy Oracle ===")
    print(f"Target: {args.target}")
    print(f"Package: {args.package}")

    main_module = args.main.replace(".py", "") if args.main else None
    mypy_result = run_mypy_graph(args.target, args.package, args.main)

    print(f"mypy version: {mypy_result['mypy_version']} "
          f"(pinned: {mypy_result['pinned_version']})")
    print(f"Config: follow_imports={mypy_result['follow_imports']}, "
          f"implicit_reexport={mypy_result['implicit_reexport']}")
    print(f"Total modules in graph: {mypy_result['total_modules']}")

    # --- 2. Extract file-level edges ---
    mypy_edges = extract_mypy_file_edges(
        mypy_result["graph"], args.target, args.package, main_module
    )
    print(f"Project import edges (mypy): {len(mypy_edges)}")

    # --- 3. Load handcount ---
    handcount_edges = load_handcount_edges(args.handcount)
    print(f"Handcount import edges (file-level): {len(handcount_edges)}")

    # --- 4. Load NeoDepends (optional) ---
    neo_edges = None
    if args.neo:
        neo_edges = load_neo_edges(args.neo)
        print(f"NeoDepends import edges (file-level): {len(neo_edges)}")

    # --- 5. Diff and arbitrate ---
    result = diff_and_arbitrate(mypy_edges, handcount_edges, neo_edges)

    print()
    print("=== Verdict Summary ===")
    for vname, count in sorted(result["verdict_counts"].items()):
        print(f"  {vname:20s}  {count}")

    print()
    print("=== Per-Edge Verdicts ===")
    for v in result["verdicts"]:
        if v["verdict"] == "AGREE":
            marker = "  "
        elif v["verdict"] in ("MYPY_BLIND", "NEO_MISS"):
            marker = "! "
        elif v["verdict"] == "NEO_BUG":
            marker = "!!"
        else:
            marker = "? "

        line = (f"{marker}{v['verdict']:20s}  "
                f"{v['src']:45s} -> {v['dst']}")
        if v.get("handcount_kind"):
            line += f"  [hc:{v['handcount_kind']}]"
        if v.get("mypy_priority") is not None:
            line += f"  [mypy:pri={v['mypy_priority']},{v['mypy_category']}]"
        if v.get("neo_kind"):
            line += f"  [neo:{v['neo_kind']}]"
        print(line)

    # --- 6. Diagnostic sections ---
    print()
    mypy_blind = [v for v in result["verdicts"] if v["verdict"] == "MYPY_BLIND"]
    if mypy_blind:
        print("=== What Mypy Cannot See ===")
        for v in mypy_blind:
            print(f"  {v['src']} -> {v['dst']}  "
                  f"(handcount: {v['handcount_kind']})")
        print()

    mapping_art = [v for v in result["verdicts"]
                   if v["verdict"] == "MAPPING_ARTIFACT"]
    if mapping_art:
        print("=== Mapping Artifacts (mypy-only, not in handcount) ===")
        for v in mapping_art:
            print(f"  {v['src']} -> {v['dst']}  "
                  f"[mypy:pri={v.get('mypy_priority')},{v.get('mypy_category')}]")
        print()

    if neo_edges is not None:
        neo_bugs = [v for v in result["verdicts"] if v["verdict"] == "NEO_BUG"]
        neo_misses = [v for v in result["verdicts"]
                      if v["verdict"] == "NEO_MISS"]
        if neo_bugs:
            print("=== NeoDepends False Positives (NEO_BUG) ===")
            for v in neo_bugs:
                print(f"  {v['src']} -> {v['dst']}  (neo: {v['neo_kind']})")
            print()
        if neo_misses:
            print("=== NeoDepends Misses (NEO_MISS) ===")
            for v in neo_misses:
                print(f"  {v['src']} -> {v['dst']}  "
                      f"(handcount: {v['handcount_kind']})")
            print()

    # --- 7. JSON output ---
    if args.json:
        output = {
            "mypy": {
                "version": mypy_result["mypy_version"],
                "pinned_version": mypy_result["pinned_version"],
                "config": {
                    "follow_imports": mypy_result["follow_imports"],
                    "implicit_reexport": mypy_result["implicit_reexport"],
                },
                "total_modules": mypy_result["total_modules"],
                "project_edges": len(mypy_edges),
            },
            "handcount_edges": len(handcount_edges),
            "neo_edges": len(neo_edges) if neo_edges else None,
            "verdict_counts": result["verdict_counts"],
            "verdicts": result["verdicts"],
        }
        with open(args.json, "w") as f:
            json.dump(output, f, indent=2)
        print(f"JSON written to {args.json}")


if __name__ == "__main__":
    main()
