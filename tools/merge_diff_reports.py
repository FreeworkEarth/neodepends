#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


Edge = Tuple[str, str, str]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def _edges(items: List[List[str]]) -> List[Edge]:
    out: List[Edge] = []
    for it in items:
        if isinstance(it, list) and len(it) == 3:
            out.append((str(it[0]), str(it[1]), str(it[2])))
    return out


def _fmt_edge(e: Edge) -> str:
    s, t, k = e
    return f"- `{k}`: `{s}` -> `{t}`"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--diff-json", type=Path, action="append", required=True)
    args = parser.parse_args()

    diffs: List[Dict[str, Any]] = []
    for p in args.diff_json:
        d = _read_json(p)
        d["_path"] = str(p)
        diffs.append(d)

    lines: List[str] = []
    lines.append("# Diff Summary (All Resolvers)")
    lines.append("")
    lines.append("This file concatenates the complete Missing/Extra edge lists for multiple resolver runs.")
    lines.append("")

    for d in diffs:
        name = Path(d.get("neodepends_dv8", d["_path"])).parent.name
        missing = _edges(d.get("missing") or [])
        extra = _edges(d.get("extra") or [])

        lines.append(f"## {name}")
        lines.append("")
        lines.append(f"- Diff JSON: `{d['_path']}`")
        lines.append(f"- NeoDepends DV8: `{d.get('neodepends_dv8','')}`")
        lines.append(f"- Ground truth: `{d.get('ground_truth','')}`")
        lines.append(f"- Missing: `{len(missing)}`")
        lines.append(f"- Extra: `{len(extra)}`")
        lines.append("")

        lines.append(f"### Missing ({len(missing)})")
        lines.append("")
        if missing:
            for e in missing:
                lines.append(_fmt_edge(e))
        else:
            lines.append("- (none)")
        lines.append("")

        lines.append(f"### Extra ({len(extra)})")
        lines.append("")
        if extra:
            for e in extra:
                lines.append(_fmt_edge(e))
        else:
            lines.append("- (none)")
        lines.append("")

    out = args.out_md.expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

