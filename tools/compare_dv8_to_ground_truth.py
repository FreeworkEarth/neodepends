#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


Edge = Tuple[str, str, str]

def _professor_to_handcount_name(name: str) -> str:
    """
    Convert professor-style DV8 naming into the handcount-style naming.

    Professor examples:
      file.py/self (File)
      file.py/Class/self (Class)
      file.py/Class/constructors/__init__ (Constructor)
      file.py/Class/methods/foo (Method)
      file.py/Class/fields/bar (Field)
      file.py/functions/top (Function)

    Handcount examples:
      file.py/module (Module)
      file.py/CLASSES/Class (Class)
      file.py/CLASSES/Class/CONSTRUCTORS/__init__ (Constructor)
      file.py/CLASSES/Class/METHODS/foo (Method)
      file.py/CLASSES/Class/FIELDS/bar (Field)
      file.py/FUNCTIONS/top (Function)
    """
    if name.endswith("/self (File)"):
        return name[: -len("/self (File)")] + "/module (Module)"

    if "/functions/" in name:
        # file.py/functions/x (Function) -> file.py/FUNCTIONS/x (Function)
        return name.replace("/functions/", "/FUNCTIONS/")

    if name.endswith("/self (Class)") and ".py/" in name:
        file_part, rest = name.split(".py/", 1)
        file_part = file_part + ".py"
        cls_path = rest[: -len("/self (Class)")]
        # Preserve nested classes by joining with "."
        cls_name = ".".join([p for p in cls_path.split("/") if p])
        return f"{file_part}/CLASSES/{cls_name} (Class)"

    for seg, repl in (
        ("/constructors/", "/CONSTRUCTORS/"),
        ("/methods/", "/METHODS/"),
        ("/fields/", "/FIELDS/"),
    ):
        if seg in name and ".py/" in name:
            file_part, rest = name.split(".py/", 1)
            file_part = file_part + ".py"
            before, after = rest.split(seg, 1)
            # `before` is class path (possibly nested)
            cls_name = ".".join([p for p in before.split("/") if p])
            return f"{file_part}/CLASSES/{cls_name}{repl}{after}"

    return name

def _maybe_normalize_neodepends(edges: Set[Edge], *, normalize_professor: bool) -> Set[Edge]:
    if not normalize_professor:
        return edges
    # Quick heuristic: only run if we see professor-style markers.
    looks_prof = any(("/self (Class)" in s or "/self (File)" in s or "/methods/" in s or "/fields/" in s) for s, _t, _k in edges)
    if not looks_prof:
        return edges
    out: Set[Edge] = set()
    for s, t, k in edges:
        out.add((_professor_to_handcount_name(s), _professor_to_handcount_name(t), k))
    return out


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _edges_from_dv8(dv8: dict) -> Set[Edge]:
    variables: Sequence[str] = dv8.get("variables", []) or []
    out: Set[Edge] = set()
    for cell in dv8.get("cells", []) or []:
        s = int(cell["src"])
        t = int(cell["dest"])
        src = variables[s]
        tgt = variables[t]
        values: Dict[str, float] = cell.get("values") or {}
        for k, v in values.items():
            if float(v) > 0.0:
                out.add((src, tgt, str(k)))
    return out


def _edges_from_json(path: Path) -> Set[Edge]:
    obj = json.loads(_read_text(path))
    if isinstance(obj, dict) and "variables" in obj and "cells" in obj:
        return _edges_from_dv8(obj)
    if isinstance(obj, list):
        out: Set[Edge] = set()
        for item in obj:
            if isinstance(item, (list, tuple)) and len(item) == 3:
                out.add((str(item[0]), str(item[1]), str(item[2])))
        return out
    raise ValueError(f"Unsupported ground truth format: {path}")


def _kind_counts(edges: Iterable[Edge]) -> Dict[str, int]:
    c = Counter()
    for _s, _t, k in edges:
        c[k] += 1
    return dict(c)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ground-truth", type=Path, required=True, help="handcount_edges*.json (list of [src,tgt,kind])")
    parser.add_argument("--neodepends-dv8", type=Path, required=True, help="NeoDepends DV8 dependency json")
    parser.add_argument("--show", type=int, default=30)
    parser.add_argument("--out", type=Path, default=None, help="Optional JSON diff output path")
    parser.add_argument("--out-md", type=Path, default=None, help="Optional Markdown diff output path (writes full Missing/Extra lists)")
    parser.add_argument(
        "--normalize-neodepends-professor",
        action="store_true",
        default=False,
        help="If NeoDepends DV8 uses professor-style naming (file/self, Class/self, methods/fields), normalize it to the handcount naming before diffing.",
    )
    args = parser.parse_args()

    gt = _edges_from_json(args.ground_truth.expanduser().resolve())
    nd = _edges_from_json(args.neodepends_dv8.expanduser().resolve())
    nd = _maybe_normalize_neodepends(nd, normalize_professor=bool(args.normalize_neodepends_professor))

    missing = sorted(gt - nd)
    extra = sorted(nd - gt)

    print("=== DV8 vs Ground Truth ===")
    print(f"Ground truth edges: {len(gt)}  kinds={_kind_counts(gt)}")
    print(f"NeoDepends edges:   {len(nd)}  kinds={_kind_counts(nd)}")
    print(f"Missing: {len(missing)}  Extra: {len(extra)}")

    if missing:
        print("\nMissing sample:")
        for e in missing[: args.show]:
            print(f"  MISSING {e[2]}: {e[0]} -> {e[1]}")
    if extra:
        print("\nExtra sample:")
        for e in extra[: args.show]:
            print(f"  EXTRA {e[2]}: {e[0]} -> {e[1]}")

    if args.out is not None:
        out_path = args.out.expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(
                {
                    "ground_truth": str(args.ground_truth),
                    "neodepends_dv8": str(args.neodepends_dv8),
                    "ground_truth_count": len(gt),
                    "neodepends_count": len(nd),
                    "ground_truth_kinds": _kind_counts(gt),
                    "neodepends_kinds": _kind_counts(nd),
                    "missing": missing,
                    "extra": extra,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"\n[OK] Wrote diff: {out_path}")

    if args.out_md is not None:
        out_md = args.out_md.expanduser().resolve()
        out_md.parent.mkdir(parents=True, exist_ok=True)
        lines: List[str] = []
        lines.append("# DV8 vs Ground Truth Diff")
        lines.append("")
        lines.append(f"- Ground truth: `{args.ground_truth}`")
        lines.append(f"- NeoDepends DV8: `{args.neodepends_dv8}`")
        lines.append(f"- Ground truth edges: `{len(gt)}`")
        lines.append(f"- NeoDepends edges: `{len(nd)}`")
        lines.append(f"- Missing: `{len(missing)}`")
        lines.append(f"- Extra: `{len(extra)}`")
        lines.append("")
        lines.append("## Kind Counts")
        lines.append("")
        lines.append(f"- Ground truth: `{_kind_counts(gt)}`")
        lines.append(f"- NeoDepends: `{_kind_counts(nd)}`")
        lines.append("")
        lines.append(f"## Missing ({len(missing)})")
        lines.append("")
        if missing:
            for src, tgt, k in missing:
                lines.append(f"- `{k}`: `{src}` -> `{tgt}`")
        else:
            lines.append("- (none)")
        lines.append("")
        lines.append(f"## Extra ({len(extra)})")
        lines.append("")
        if extra:
            for src, tgt, k in extra:
                lines.append(f"- `{k}`: `{src}` -> `{tgt}`")
        else:
            lines.append("- (none)")
        lines.append("")
        out_md.write_text("\n".join(lines), encoding="utf-8")
        print(f"[OK] Wrote diff markdown: {out_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
