#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


KINDS = {"Import", "Extend", "Create", "Call", "Use"}


@dataclass(frozen=True)
class ClassIndex:
    methods: Set[str]
    fields: Set[str]


@dataclass(frozen=True)
class FileIndex:
    functions: Set[str]
    classes: Dict[str, ClassIndex]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _iter_project_py(project_root: Path) -> List[Path]:
    files: List[Path] = []
    for p in project_root.glob("*.py"):
        if not p.name.startswith("."):
            files.append(p)
    tts = project_root / "tts"
    if tts.is_dir():
        files.extend(sorted(tts.rglob("*.py")))
    return sorted(files)


def _build_index(project_root: Path) -> Tuple[Dict[str, FileIndex], Set[str]]:
    """
    Index project-local entities so we can normalize NeoDepends variable names into our canonical DV8 names.
    Returns:
      - per-file index keyed by workspace-relative posix path (e.g. tts/route.py, main.py)
      - set of all file paths (same keys)
    """
    out: Dict[str, FileIndex] = {}

    for path in _iter_project_py(project_root):
        rel = path.relative_to(project_root).as_posix()
        tree = ast.parse(_read_text(path), filename=rel)

        functions: Set[str] = set()
        classes: Dict[str, ClassIndex] = {}

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.add(node.name)
            elif isinstance(node, ast.ClassDef):
                method_names: Set[str] = set()
                field_names: Set[str] = set()

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_names.add(item.name)
                        for sub in ast.walk(item):
                            if isinstance(sub, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                                targets: List[ast.AST] = []
                                if isinstance(sub, ast.Assign):
                                    targets = list(sub.targets)
                                elif isinstance(sub, ast.AnnAssign):
                                    targets = [sub.target]
                                elif isinstance(sub, ast.AugAssign):
                                    targets = [sub.target]
                                for t in targets:
                                    if (
                                        isinstance(t, ast.Attribute)
                                        and isinstance(t.value, ast.Name)
                                        and t.value.id == "self"
                                    ):
                                        field_names.add(t.attr)
                    elif isinstance(item, ast.Assign):
                        for t in item.targets:
                            if isinstance(t, ast.Name):
                                field_names.add(t.id)
                    elif isinstance(item, ast.AnnAssign):
                        if isinstance(item.target, ast.Name):
                            field_names.add(item.target.id)

                classes[node.name] = ClassIndex(methods=method_names, fields=field_names)

        out[rel] = FileIndex(functions=functions, classes=classes)

    return out, set(out.keys())


def _canonical_var(*, file: str, kind: str, cls: Optional[str] = None, name: Optional[str] = None) -> str:
    if kind == "File":
        return f"{file}/module (Module)"
    if kind == "Function":
        assert name
        return f"{file}/FUNCTIONS/{name} (Function)"
    if kind == "Class":
        assert name
        return f"{file}/CLASSES/{name} (Class)"
    if kind == "Method":
        assert cls and name
        if name == "__init__":
            return f"{file}/CLASSES/{cls}/CONSTRUCTORS/{name} (Constructor)"
        return f"{file}/CLASSES/{cls}/METHODS/{name} (Method)"
    if kind == "Field":
        assert cls and name
        return f"{file}/CLASSES/{cls}/FIELDS/{name} (Field)"
    raise ValueError(kind)


def _normalize_file_path(raw: str, project_files: Set[str]) -> Optional[str]:
    """
    raw may be:
      - "tts/route.py"
      - "/tmp/.../tts/route.py"
      - "namespace/tts/route.py"
    We try to map it to an exact project file by suffix match.
    """
    raw_posix = raw.replace("\\", "/")
    if raw_posix in project_files:
        return raw_posix
    # pick the longest suffix match
    best: Optional[str] = None
    for f in project_files:
        if raw_posix.endswith("/" + f) or raw_posix.endswith(f):
            if best is None or len(f) > len(best):
                best = f
    return best


_NEODEPENDS_KIND_MAP = {
    "Use": "Use",
    "Call": "Call",
    "Create": "Create",
    "Extend": "Extend",
    "Import": "Import",
}


def _normalize_neodepends_var(
    raw_var: str, *, file_index: Dict[str, FileIndex], project_files: Set[str]
) -> Optional[str]:
    """
    Normalize NeoDepends DV8 variable names into canonical ground-truth names.
    Supported NeoDepends forms:
      - "tts/route.py"                                 (file)
      - "tts/route.py::Route"                          (class)
      - "tts/route.py::Route.get_origin"               (method)
      - "tts/ticket_agent.py::TicketAgent.tickets_processed" (field)
      - "main.py::main"                                (function)
    Any variable not resolvable to a project-local entity returns None.
    """
    if "::" not in raw_var:
        f = _normalize_file_path(raw_var, project_files)
        if not f:
            return None
        return _canonical_var(file=f, kind="File")

    file_part, entity_part = raw_var.split("::", 1)
    f = _normalize_file_path(file_part, project_files)
    if not f:
        return None

    idx = file_index.get(f)
    if idx is None:
        return None

    # Class.method or Class.field
    if "." in entity_part:
        cls, member = entity_part.split(".", 1)
        cidx = idx.classes.get(cls)
        if cidx is None:
            # can't confidently classify; treat as a function-like symbol and keep as Function.
            return _canonical_var(file=f, kind="Function", name=entity_part)

        if member in cidx.methods:
            return _canonical_var(file=f, kind="Method", cls=cls, name=member)
        if member in cidx.fields:
            return _canonical_var(file=f, kind="Field", cls=cls, name=member)

        # Unknown member name: keep it, but choose Field (less disruptive for architecture DSMs).
        # This makes diffs explicit instead of silently dropping edges.
        return _canonical_var(file=f, kind="Field", cls=cls, name=member)

    # Either a class or a function
    if entity_part in idx.classes:
        return _canonical_var(file=f, kind="Class", name=entity_part)
    if entity_part in idx.functions:
        return _canonical_var(file=f, kind="Function", name=entity_part)

    # Unknown top-level symbol: drop (usually external, dynamic, or untagged).
    return None


def _edges_from_dv8(dv8: dict) -> List[Tuple[str, str, str]]:
    vars_: Sequence[str] = dv8.get("variables", [])
    cells: Sequence[dict] = dv8.get("cells", [])
    out: List[Tuple[str, str, str]] = []
    for c in cells:
        s = int(c["src"])
        t = int(c["dest"])
        values: dict = c.get("values", {})
        for k, v in values.items():
            if k not in _NEODEPENDS_KIND_MAP:
                continue
            if float(v) <= 0.0:
                continue
            out.append((vars_[s], vars_[t], _NEODEPENDS_KIND_MAP[k]))
    return out


def _load_edges_json(path: Path) -> List[Tuple[str, str, str]]:
    data = json.loads(_read_text(path))
    if not isinstance(data, list):
        raise ValueError("Expected a JSON list for edges")
    edges: List[Tuple[str, str, str]] = []
    for row in data:
        if not (isinstance(row, list) and len(row) == 3):
            raise ValueError("Expected edges as [src, tgt, kind] lists")
        src, tgt, kind = row
        edges.append((str(src), str(tgt), str(kind)))
    return edges


def _dedupe(edges: Iterable[Tuple[str, str, str]], *, collapse_to_use: bool) -> Set[Tuple[str, str, str]]:
    out: Set[Tuple[str, str, str]] = set()
    for s, t, k in edges:
        kk = "Use" if collapse_to_use else k
        out.add((s, t, kk))
    return out


def _counts(edges: Iterable[Tuple[str, str, str]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for _s, _t, k in edges:
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--ground-truth", type=Path, default=Path(__file__).with_name("handcount_edges.json"))
    parser.add_argument("--neodepends-dv8", type=Path, required=True, help="Path to NeoDepends DV8 dependency JSON")
    parser.add_argument("--collapse-to-use", action="store_true", help="Ignore kinds and compare as Use-only edges")
    parser.add_argument(
        "--inner-only",
        action="store_true",
        help="Compare only inner entities (exclude file/module nodes and derived file-level edges)",
    )
    parser.add_argument("--show", type=int, default=50, help="Max edges to print for missing/extra")
    parser.add_argument("--out-dir", type=Path, default=None, help="If set, write normalized edges + diff JSON here")
    args = parser.parse_args()

    project_root = args.project_root.expanduser().resolve()
    gt_path = args.ground_truth.expanduser().resolve()
    nd_path = args.neodepends_dv8.expanduser().resolve()

    file_index, project_files = _build_index(project_root)

    gt_edges_raw = _load_edges_json(gt_path)
    gt_edges = _dedupe(gt_edges_raw, collapse_to_use=args.collapse_to_use)

    nd_dv8 = json.loads(_read_text(nd_path))
    nd_edges_raw = _edges_from_dv8(nd_dv8)

    normalized: List[Tuple[str, str, str]] = []
    dropped = 0
    for src, tgt, kind in nd_edges_raw:
        if kind not in KINDS:
            continue
        s = _normalize_neodepends_var(src, file_index=file_index, project_files=project_files)
        t = _normalize_neodepends_var(tgt, file_index=file_index, project_files=project_files)
        if not s or not t:
            dropped += 1
            continue
        normalized.append((s, t, kind))

    nd_edges = _dedupe(normalized, collapse_to_use=args.collapse_to_use)

    if args.inner_only:
        def is_module_node(v: str) -> bool:
            return v.endswith("/module (Module)")

        gt_edges = {e for e in gt_edges if not is_module_node(e[0]) and not is_module_node(e[1])}
        nd_edges = {e for e in nd_edges if not is_module_node(e[0]) and not is_module_node(e[1])}

    missing = sorted(gt_edges - nd_edges)
    extra = sorted(nd_edges - gt_edges)

    print("=== NeoDepends vs Ground Truth ===")
    print(f"Project root: {project_root}")
    print(f"Ground truth edges: {len(gt_edges)}  kinds={_counts(gt_edges)}")
    print(f"NeoDepends edges (normalized): {len(nd_edges)}  kinds={_counts(nd_edges)}")
    print(f"Dropped NeoDepends edges during normalization (external/unknown): {dropped}")
    print("")
    print(f"Missing edges (ground truth but not in NeoDepends): {len(missing)}")
    for e in missing[: args.show]:
        print(f"  MISSING {e[2]}: {e[0]} -> {e[1]}")
    if len(missing) > args.show:
        print(f"  ... {len(missing) - args.show} more")
    print("")
    print(f"Extra edges (NeoDepends but not in ground truth): {len(extra)}")
    for e in extra[: args.show]:
        print(f"  EXTRA   {e[2]}: {e[0]} -> {e[1]}")
    if len(extra) > args.show:
        print(f"  ... {len(extra) - args.show} more")

    if args.out_dir is not None:
        out_dir = args.out_dir.expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "neodepends_edges.normalized.json").write_text(
            json.dumps(sorted(nd_edges), indent=2), encoding="utf-8"
        )
        (out_dir / "diff.json").write_text(
            json.dumps(
                {
                    "ground_truth_count": len(gt_edges),
                    "neodepends_count": len(nd_edges),
                    "dropped_count": dropped,
                    "missing": missing,
                    "extra": extra,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print("")
        print(f"[OK] Wrote: {out_dir / 'neodepends_edges.normalized.json'}")
        print(f"[OK] Wrote: {out_dir / 'diff.json'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
