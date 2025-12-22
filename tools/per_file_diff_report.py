#!/usr/bin/env python3
"""
Generate per-file Missing/Extra reports from a ground-truth edge list and a diff JSON.

Inputs:
  - Ground truth: a JSON list of edges: [src_name, dest_name, kind]
  - Diff JSON: produced by compare_dv8_to_ground_truth.py, containing:
      { missing: [[src, dest, kind], ...], extra: [[src, dest, kind], ...], ... }

Output:
  - A directory tree mirroring file paths (prefix up to ".py"), with one Markdown file per
    source file, reporting:
      - GT outgoing totals
      - NeoDepends outgoing totals (reconstructed as (GT - missing) + extra)
      - Missing/Extra lists, grouped by dependency kind

Notes:
  - This tool intentionally groups edges by the *source* file (based on src node name).
  - External nodes without a ".py" prefix are grouped under "__external__".
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import DefaultDict, Iterable, Iterator, List, Sequence, Tuple


Edge = Tuple[str, str, str]


_PY_FILE_RE = re.compile(r"^(.*?\.py)(?:/|\b|$)")


def _file_key(node_name: str) -> str:
    match = _PY_FILE_RE.match(node_name)
    if match:
        return match.group(1)
    return "__external__"


def _load_edges_list(path: Path) -> List[Edge]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON list at {path}, got {type(data)}")
    edges: List[Edge] = []
    for idx, item in enumerate(data):
        if (
            not isinstance(item, list)
            or len(item) != 3
            or not all(isinstance(x, str) for x in item)
        ):
            raise ValueError(f"Invalid edge at {path} index {idx}: {item!r}")
        edges.append((item[0], item[1], item[2]))
    return edges


def _load_diff(path: Path) -> tuple[List[Edge], List[Edge]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = data.get("missing", [])
    extra = data.get("extra", [])
    if not isinstance(missing, list) or not isinstance(extra, list):
        raise ValueError(f"Invalid diff JSON at {path}: missing/extra must be lists")

    def parse_edges(items: Sequence[Sequence[str]], label: str) -> List[Edge]:
        edges: List[Edge] = []
        for idx, item in enumerate(items):
            if (
                not isinstance(item, list)
                or len(item) != 3
                or not all(isinstance(x, str) for x in item)
            ):
                raise ValueError(f"Invalid {label} edge at {path} index {idx}: {item!r}")
            edges.append((item[0], item[1], item[2]))
        return edges

    return parse_edges(missing, "missing"), parse_edges(extra, "extra")


def _group_by_src_file(edges: Iterable[Edge]) -> DefaultDict[str, List[Edge]]:
    grouped: DefaultDict[str, List[Edge]] = defaultdict(list)
    for src, dest, kind in edges:
        grouped[_file_key(src)].append((src, dest, kind))
    return grouped


def _count_by_kind(edges: Iterable[Edge]) -> Counter[str]:
    c: Counter[str] = Counter()
    for _, _, kind in edges:
        c[kind] += 1
    return c


@dataclass(frozen=True)
class FileReport:
    file_key: str
    gt_edges: List[Edge]
    nd_edges: List[Edge]
    missing: List[Edge]
    extra: List[Edge]


def _reconstruct_neodepends_edges(gt_edges: Iterable[Edge], missing: Iterable[Edge], extra: Iterable[Edge]) -> List[Edge]:
    gt_set = set(gt_edges)
    miss_set = set(missing)
    extra_set = set(extra)
    nd_set = (gt_set - miss_set) | extra_set
    return sorted(nd_set)


def _fmt_pct(n: int, denom: int) -> str:
    if denom <= 0:
        return "n/a"
    return f"{(100.0 * n / denom):.1f}%"


def _md_edge(edge: Edge) -> str:
    src, dest, kind = edge
    return f"- `{kind}`: `{src}` -> `{dest}`"


def _write_file_report(path: Path, report: FileReport) -> None:
    gt_total = len(set(report.gt_edges))
    nd_total = len(set(report.nd_edges))
    miss_total = len(set(report.missing))
    extra_total = len(set(report.extra))

    gt_by_kind = _count_by_kind(set(report.gt_edges))
    nd_by_kind = _count_by_kind(set(report.nd_edges))

    missing_by_kind = defaultdict(list)
    for e in sorted(set(report.missing)):
        missing_by_kind[e[2]].append(e)
    extra_by_kind = defaultdict(list)
    for e in sorted(set(report.extra)):
        extra_by_kind[e[2]].append(e)

    lines: List[str] = []
    lines.append(f"# `{report.file_key}`")
    lines.append("")
    lines.append("## Summary (outgoing edges)")
    lines.append("")
    lines.append(f"- Ground truth: {gt_total}")
    lines.append(f"- NeoDepends (reconstructed): {nd_total}")
    lines.append(
        f"- Missing: {miss_total} ({_fmt_pct(miss_total, gt_total)} of ground truth)"
    )
    lines.append(
        f"- Extra: {extra_total} ({_fmt_pct(extra_total, gt_total)} of ground truth)"
    )
    lines.append("")

    def add_kind_table(title: str, counter: Counter[str]) -> None:
        lines.append(f"## {title}")
        lines.append("")
        if not counter:
            lines.append("- (none)")
            lines.append("")
            return
        for kind, count in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"- {kind}: {count}")
        lines.append("")

    add_kind_table("Ground truth breakdown", gt_by_kind)
    add_kind_table("NeoDepends breakdown", nd_by_kind)

    lines.append("## Missing edges")
    lines.append("")
    if not missing_by_kind:
        lines.append("- (none)")
        lines.append("")
    else:
        for kind in sorted(missing_by_kind.keys()):
            lines.append(f"### {kind}")
            lines.append("")
            for edge in missing_by_kind[kind]:
                lines.append(_md_edge(edge))
            lines.append("")

    lines.append("## Extra edges")
    lines.append("")
    if not extra_by_kind:
        lines.append("- (none)")
        lines.append("")
    else:
        for kind in sorted(extra_by_kind.keys()):
            lines.append(f"### {kind}")
            lines.append("")
            for edge in extra_by_kind[kind]:
                lines.append(_md_edge(edge))
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _relative_report_path(out_dir: Path, file_key: str) -> Path:
    if file_key == "__external__":
        return out_dir / "__external__.md"
    parts = file_key.split("/")
    if len(parts) == 1:
        return out_dir / f"{parts[0]}.md"
    *dirs, filename = parts
    return out_dir.joinpath(*dirs) / f"{filename}.md"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", required=True, type=Path, help="Path to ground truth edge list JSON")
    parser.add_argument("--diff", required=True, type=Path, help="Path to diff JSON (missing/extra)")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory to write per-file markdown reports")
    args = parser.parse_args(argv)

    gt_edges = _load_edges_list(args.ground_truth)
    missing_edges, extra_edges = _load_diff(args.diff)

    gt_by_file = _group_by_src_file(gt_edges)
    missing_by_file = _group_by_src_file(missing_edges)
    extra_by_file = _group_by_src_file(extra_edges)

    all_files = set(gt_by_file) | set(missing_by_file) | set(extra_by_file)
    reports: List[FileReport] = []

    for file_key in sorted(all_files):
        gt_file_edges = gt_by_file.get(file_key, [])
        miss_file_edges = missing_by_file.get(file_key, [])
        extra_file_edges = extra_by_file.get(file_key, [])
        nd_file_edges = _reconstruct_neodepends_edges(gt_file_edges, miss_file_edges, extra_file_edges)
        reports.append(
            FileReport(
                file_key=file_key,
                gt_edges=gt_file_edges,
                nd_edges=nd_file_edges,
                missing=miss_file_edges,
                extra=extra_file_edges,
            )
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Write per-file markdowns
    for r in reports:
        report_path = _relative_report_path(args.out_dir, r.file_key)
        _write_file_report(report_path, r)

    # Write index
    index_lines: List[str] = []
    index_lines.append("# Per-file diff report")
    index_lines.append("")
    index_lines.append(f"- Ground truth: `{args.ground_truth}`")
    index_lines.append(f"- Diff JSON: `{args.diff}`")
    index_lines.append("")
    index_lines.append("## Files")
    index_lines.append("")
    index_lines.append("| File | GT | Missing | Extra |")
    index_lines.append("|---|---:|---:|---:|")
    for r in reports:
        gt_total = len(set(r.gt_edges))
        miss_total = len(set(r.missing))
        extra_total = len(set(r.extra))
        rel = os.path.relpath(_relative_report_path(args.out_dir, r.file_key), args.out_dir)
        index_lines.append(f"| [`{r.file_key}`]({rel}) | {gt_total} | {miss_total} | {extra_total} |")
    index_lines.append("")
    (args.out_dir / "README.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")

    print(f"[OK] Wrote per-file diff reports to: {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
