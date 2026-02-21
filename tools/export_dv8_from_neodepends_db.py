#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DV8_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class Entity:
    id: bytes
    parent_id: Optional[bytes]
    name: str
    kind: str


Edge = Tuple[str, str, str]  # (src, tgt, kind)


def _read_entities(con: sqlite3.Connection) -> Dict[bytes, Entity]:
    cur = con.cursor()
    rows = cur.execute("SELECT id, parent_id, name, kind FROM entities").fetchall()
    entities: Dict[bytes, Entity] = {}
    for entity_id, parent_id, name, kind in rows:
        entities[entity_id] = Entity(id=entity_id, parent_id=parent_id, name=str(name), kind=str(kind))
    return entities


def _find_ancestor(
    entities: Dict[bytes, Entity], entity_id: bytes, *, kind: str
) -> Optional[Entity]:
    cur_id: Optional[bytes] = entity_id
    while cur_id is not None:
        e = entities.get(cur_id)
        if e is None:
            return None
        if e.kind == kind:
            return e
        cur_id = e.parent_id
    return None


def _file_name_for_entity(entities: Dict[bytes, Entity], entity_id: bytes) -> str:
    f = _find_ancestor(entities, entity_id, kind="File")
    return f.name if f else "(Unknown File)"


def _class_name_for_entity(entities: Dict[bytes, Entity], entity_id: bytes) -> Optional[str]:
    c = _find_ancestor(entities, entity_id, kind="Class")
    return c.name if c else None


def _var_name(
    entities: Dict[bytes, Entity], entity_id: bytes, *, dv8_hierarchy: str
) -> Optional[str]:
    e = entities.get(entity_id)
    if e is None:
        return None

    file_name = _file_name_for_entity(entities, entity_id)

    if e.kind == "File":
        return f"{e.name}/self (File)"

    class_name = _class_name_for_entity(entities, entity_id)

    if e.kind == "Class":
        return f"{file_name}/{e.name}/self (Class)"

    if e.kind in {"Method", "Constructor", "Field", "Function"}:
        if not class_name:
            # Module-level function or field (no class parent)
            if e.kind == "Function":
                return f"{file_name}/functions/{e.name} (Function)"
            if e.kind == "Field":
                return f"{file_name}/fields/{e.name} (Field)"
            # Fallback for other kinds without class
            return f"{file_name}/{e.name} ({e.kind})"
        # Class member
        if e.kind == "Method":
            return f"{file_name}/{class_name}/methods/{e.name} (Method)"
        if e.kind == "Constructor":
            return f"{file_name}/{class_name}/constructors/{e.name} (Constructor)"
        if e.kind == "Field":
            return f"{file_name}/{class_name}/fields/{e.name} (Field)"
        if e.kind == "Function":
            # Should not happen: Function inside a class should be Method
            return f"{file_name}/{class_name}/methods/{e.name} (Function)"

    # Fallback: keep it addressable in the matrix.
    return f"{file_name}/{e.name} ({e.kind})"


def _read_edges(
    con: sqlite3.Connection,
    *,
    entities: Dict[bytes, Entity],
    kinds: Sequence[str],
    dv8_hierarchy: str,
) -> List[Edge]:
    cur = con.cursor()
    wanted = set(kinds)
    rows = cur.execute("SELECT src, tgt, kind FROM deps").fetchall()
    out: List[Edge] = []
    for src_id, tgt_id, kind in rows:
        kind = str(kind)
        if kind not in wanted:
            continue
        src = _var_name(entities, src_id, dv8_hierarchy=dv8_hierarchy)
        tgt = _var_name(entities, tgt_id, dv8_hierarchy=dv8_hierarchy)
        if not src or not tgt:
            continue
        out.append((src, tgt, kind))
    return out


def _dv8_from_edges(*, name: str, edges: Iterable[Edge]) -> Dict[str, Any]:
    variables: List[str] = []
    index: Dict[str, int] = {}

    def idx(v: str) -> int:
        if v in index:
            return index[v]
        index[v] = len(variables)
        variables.append(v)
        return index[v]

    cells_map: Dict[Tuple[int, int], Dict[str, float]] = {}
    for src, tgt, kind in edges:
        s = idx(src)
        t = idx(tgt)
        key = (s, t)
        values = cells_map.setdefault(key, {})
        values[kind] = values.get(kind, 0.0) + 1.0

    cells = [{"src": s, "dest": t, "values": values} for (s, t), values in sorted(cells_map.items())]
    return {"@schemaVersion": DV8_SCHEMA_VERSION, "name": name, "variables": variables, "cells": cells}


def main() -> int:
    ap = argparse.ArgumentParser(description="Export a DV8 dependency JSON from a NeoDepends SQLite DB.")
    ap.add_argument("--db", type=Path, required=True, help="NeoDepends sqlite DB")
    ap.add_argument("--out", type=Path, required=True, help="Output DV8 dependency json path")
    ap.add_argument("--name", default="neodepends (dv8 export)", help="Matrix name")
    ap.add_argument(
        "--kinds",
        default="Import,Extend,Create,Call,Use,Parameter,Cast",
        help="Comma-separated dep kinds to include (default: Import,Extend,Create,Call,Use,Parameter,Cast)",
    )
    ap.add_argument(
        "--dv8-hierarchy",
        choices=["structured"],
        default="structured",
        help="DV8 hierarchy mode (currently: structured).",
    )
    args = ap.parse_args()

    db = args.db.expanduser().resolve()
    out = args.out.expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    kinds = [k.strip() for k in (args.kinds or "").split(",") if k.strip()]
    if not kinds:
        raise SystemExit("No --kinds specified")

    con = sqlite3.connect(str(db))
    try:
        entities = _read_entities(con)
        edges = _read_edges(con, entities=entities, kinds=kinds, dv8_hierarchy=args.dv8_hierarchy)
    finally:
        con.close()

    dv8 = _dv8_from_edges(name=args.name, edges=edges)
    out.write_text(json.dumps(dv8, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

