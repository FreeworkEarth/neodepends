#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


Edge = Tuple[str, str, str]

def _normalize_to_handcount_name(name: str) -> str:
    """
    Convert NeoDepends DV8 naming (structured/flat) into the handcount-style naming.

    Structured ("professor"/"structured") examples:
      file.py/self (File)
      file.py/Class/self (Class)
      file.py/Class/constructors/__init__ (Constructor)
      file.py/Class/methods/foo (Method)
      file.py/Class/fields/bar (Field)
      file.py/functions/top (Function)

    Flat examples:
      file.py/self (File)
      file.py/-self Foo (Class)
      file.py/+CONSTRUCTORS/Foo/__init__ (Constructor)
      file.py/+METHODS/Foo/foo (Method)
      file.py/+FIELDS/Foo/bar (Field)

    Handcount examples:
      file.py/module (Module)
      file.py/CLASSES/Class (Class)
      file.py/CLASSES/Class/CONSTRUCTORS/__init__ (Constructor)
      file.py/CLASSES/Class/METHODS/foo (Method)
      file.py/CLASSES/Class/FIELDS/bar (Field)
      file.py/FUNCTIONS/top (Function)
    """
    if ".py::" in name:
        file_part, rest = name.split(".py::", 1)
        file_part = file_part + ".py"
        func = rest.strip("/")
        return f"{file_part}/FUNCTIONS/{func} (Function)"

    if name.endswith("/self (File)"):
        return name[: -len("/self (File)")] + "/module (Module)"

    # Flat optional subclass grouping:
    #   file.py/+SUBCLASSES/Base/-self Sub (Class)
    # Normalize by dropping the grouping and treating the remaining node normally.
    if "/+SUBCLASSES/" in name and ".py/" in name:
        file_part, rest = name.split(".py/", 1)
        file_part = file_part + ".py"
        parts = [p for p in rest.split("/") if p]
        # Expect: ["+SUBCLASSES", "<Base>", ...]
        if len(parts) >= 3 and parts[0] == "+SUBCLASSES":
            rest2 = "/".join(parts[2:])
            return _normalize_to_handcount_name(f"{file_part}/{rest2}")

    # Flat class marker: file.py/-self Foo (Class) -> file.py/CLASSES/Foo (Class)
    if "/-self " in name and name.endswith(" (Class)"):
        file_part, rest = name.split("/-self ", 1)
        cls = rest[: -len(" (Class)")].strip()
        return f"{file_part}/CLASSES/{cls} (Class)"

    # Flat member folders: +METHODS/+FIELDS/+CONSTRUCTORS
    for seg, repl in (
        ("/+FUNCTIONS/", "/FUNCTIONS/"),
        ("/+METHODS/", "/METHODS/"),
        ("/+FIELDS/", "/FIELDS/"),
        ("/+CONSTRUCTORS/", "/CONSTRUCTORS/"),
    ):
        if seg in name and ".py" in name:
            # file.py/+FUNCTIONS/x (Function) -> file.py/FUNCTIONS/x (Function)
            if seg == "/+FUNCTIONS/":
                return name.replace("/+FUNCTIONS/", "/FUNCTIONS/")
            # file.py/+METHODS/Foo/bar (Method) -> file.py/CLASSES/Foo/METHODS/bar (Method)
            file_part, after_file = name.split(".py", 1)
            file_part = file_part + ".py"
            rest = after_file.lstrip("/")
            before, tail = rest.split(seg.lstrip("/"), 1)
            _ = before  # unused
            # tail is: Foo/thing (Kind)
            parts = tail.split("/", 1)
            if len(parts) != 2:
                break
            cls, member = parts[0], parts[1]
            return f"{file_part}/CLASSES/{cls}{repl}{member}"

    if "/functions/" in name:
        # file.py/functions/x (Function) -> file.py/FUNCTIONS/x (Function)
        return name.replace("/functions/", "/FUNCTIONS/")

    if name.endswith("/self (Class)") and ".py/" in name:
        file_part, rest = name.split(".py/", 1)
        file_part = file_part + ".py"
        cls_path = rest[: -len("/self (Class)")]
        # Preserve nested classes by joining with "."
        cls_name = ".".join([p for p in cls_path.split("/") if p])
        # Normalize optional nesting markers used by some DV8 hierarchies.
        # - `inner_classes` is a synthetic folder used for nested classes.
        if ".inner_classes." in cls_name:
            cls_name = cls_name.replace(".inner_classes.", ".")
        # NeoDepends "structured" may optionally nest subclasses under `<Base>.subclasses.<Sub>`.
        # The handcount naming convention used for comparisons typically uses just `<Sub>`.
        if ".subclasses." in cls_name:
            cls_name = cls_name.split(".subclasses.")[-1]
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
            if ".inner_classes." in cls_name:
                cls_name = cls_name.replace(".inner_classes.", ".")
            if ".subclasses." in cls_name:
                cls_name = cls_name.split(".subclasses.")[-1]
            return f"{file_part}/CLASSES/{cls_name}{repl}{after}"

    return name

def _normalize_java_name(name: str) -> str:
    if ".java/" not in name:
        return name
    file_part, rest = name.split(".java/", 1)
    file_part = file_part + ".java"
    file_base = Path(file_part).stem

    def drop_outer(path: str) -> str:
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 2 and parts[0] == file_base:
            parts = parts[1:]
        return "/".join(parts)

    if rest == "self (File)":
        return f"{file_part}/module (Module)"

    if rest.endswith("/self (Class)"):
        cls_path = rest[: -len("/self (Class)")]
        cls_path = drop_outer(cls_path)
        return f"{file_part}/{cls_path} (Class)"

    if rest.endswith(" (Class)"):
        cls_path = rest[: -len(" (Class)")]
        cls_path = drop_outer(cls_path)
        return f"{file_part}/{cls_path} (Class)"

    for seg in ("/constructors/", "/methods/", "/fields/"):
        if seg in rest:
            before, after = rest.split(seg, 1)
            before = drop_outer(before)
            return f"{file_part}/{before}{seg}{after}"

    return name


def _strip_prefixes(name: str, prefixes: Sequence[str]) -> str:
    for prefix in prefixes:
        if not prefix:
            continue
        while name.startswith(prefix):
            name = name[len(prefix):]
    return name


def _maybe_strip_prefixes(edges: Set[Edge], prefixes: Sequence[str]) -> Set[Edge]:
    if not prefixes:
        return edges
    out: Set[Edge] = set()
    for s, t, k in edges:
        out.add((_strip_prefixes(s, prefixes), _strip_prefixes(t, prefixes), k))
    return out


def _exclude_prefixes(edges: Set[Edge], prefixes: Sequence[str]) -> Set[Edge]:
    if not prefixes:
        return edges
    out: Set[Edge] = set()
    for s, t, k in edges:
        if any(s.startswith(p) or t.startswith(p) for p in prefixes):
            continue
        out.add((s, t, k))
    return out


def _expand_prefixes(raw: Sequence[str] | None) -> List[str]:
    if not raw:
        return []
    out: List[str] = []
    for item in raw:
        if not item:
            continue
        parts = [p.strip() for p in str(item).split(",") if p.strip()]
        out.extend(parts)
    return out


def _maybe_normalize_java(edges: Set[Edge], *, normalize_java: bool) -> Set[Edge]:
    if not normalize_java:
        return edges
    looks_java = any(".java/" in s or ".java/" in t for s, t, _k in edges)
    if not looks_java:
        return edges
    out: Set[Edge] = set()
    for s, t, k in edges:
        out.add((_normalize_java_name(s), _normalize_java_name(t), k))
    return out


def _maybe_normalize_neodepends(edges: Set[Edge], *, normalize_professor: bool) -> Set[Edge]:
    if not normalize_professor:
        return edges
    out: Set[Edge] = set()
    for s, t, k in edges:
        out.add((_normalize_to_handcount_name(s), _normalize_to_handcount_name(t), k))
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
                kind = str(item[2]).strip()
                if not kind or kind.startswith("==="):
                    continue
                out.add((str(item[0]).strip(), str(item[1]).strip(), kind))
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
    parser.add_argument(
        "--normalize-java-handcount",
        action="store_true",
        default=False,
        help="Normalize Java naming differences (drop /self for classes and collapse inner-class paths) on both ground truth and NeoDepends edges.",
    )
    parser.add_argument(
        "--strip-prefix",
        action="append",
        default=None,
        help="Strip leading path prefix(es) from both NeoDepends and handcount edges (repeatable or comma-separated).",
    )
    parser.add_argument(
        "--exclude-prefix",
        action="append",
        default=None,
        help="Exclude edges where src or tgt starts with prefix(es) (repeatable or comma-separated).",
    )
    args = parser.parse_args()

    gt = _edges_from_json(args.ground_truth.expanduser().resolve())
    nd = _edges_from_json(args.neodepends_dv8.expanduser().resolve())
    nd = _maybe_normalize_neodepends(nd, normalize_professor=bool(args.normalize_neodepends_professor))
    gt = _maybe_normalize_java(gt, normalize_java=bool(args.normalize_java_handcount))
    nd = _maybe_normalize_java(nd, normalize_java=bool(args.normalize_java_handcount))
    prefixes = _expand_prefixes(args.strip_prefix)
    if prefixes:
        gt = _maybe_strip_prefixes(gt, prefixes)
        nd = _maybe_strip_prefixes(nd, prefixes)
    exclude_prefixes = _expand_prefixes(args.exclude_prefix)
    if exclude_prefixes:
        gt = _exclude_prefixes(gt, exclude_prefixes)
        nd = _exclude_prefixes(nd, exclude_prefixes)

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
