#!/usr/bin/env python3
"""
Heuristic Java dependency enhancement.

Adds missing dependencies that Depends often omits:
  - Constructor -> Field (Use) for "this.field =" assignments
  - Constructor -> Constructor (Call) for super(...) / this(...)

This operates purely on the existing NeoDepends DB and source text.
"""

import argparse
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Entity:
    id: bytes
    parent_id: Optional[bytes]
    name: str
    kind: str
    start_row: int
    end_row: int
    content_id: bytes


def _load_entities(conn: sqlite3.Connection) -> Dict[bytes, Entity]:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, parent_id, name, kind, start_row, end_row, content_id FROM entities"
    )
    out: Dict[bytes, Entity] = {}
    for row in cur.fetchall():
        out[row[0]] = Entity(
            id=row[0],
            parent_id=row[1],
            name=row[2],
            kind=row[3],
            start_row=row[4] or 0,
            end_row=row[5] or 0,
            content_id=row[6],
        )
    return out


def _load_contents(conn: sqlite3.Connection) -> Dict[bytes, str]:
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM contents")
    return {row[0]: row[1] for row in cur.fetchall()}


def _ancestor_file_id(entities: Dict[bytes, Entity], entity_id: bytes) -> Optional[bytes]:
    cur = entities.get(entity_id)
    seen: Set[bytes] = set()
    while cur is not None:
        if cur.id in seen:
            return None
        seen.add(cur.id)
        if cur.kind == "File":
            return cur.id
        if cur.parent_id is None:
            return None
        cur = entities.get(cur.parent_id)
    return None


def _strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*", "", text)
    return text


def _is_ctor_method(ent: Entity, class_ent: Entity) -> bool:
    # Depends sometimes records constructors as Method with name == class name or <init>.
    if ent.name == "<init>":
        return True
    return ent.name == class_ent.name


def _parse_param_names(signature: str) -> Set[str]:
    # Extract parameter list inside (...)
    m = re.search(r"\\(([^)]*)\\)", signature)
    if not m:
        return set()
    params = m.group(1).strip()
    if not params:
        return set()
    names: Set[str] = set()
    for part in params.split(","):
        part = part.strip()
        if not part:
            continue
        # Remove annotations and generics, keep last identifier
        tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", part)
        if tokens:
            names.add(tokens[-1])
    return names


def _extract_cast_assignments(block: str) -> Dict[str, str]:
    # Match: Type var = (CastType) expr;
    # Match: var = (CastType) expr;
    casts: Dict[str, str] = {}
    pattern_decl = re.compile(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(\s*([A-Za-z_][A-Za-z0-9_$.]*)\s*\)"
    )
    pattern_assign = re.compile(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(\s*([A-Za-z_][A-Za-z0-9_$.]*)\s*\)"
    )
    for m in pattern_decl.finditer(block):
        var = m.group(2)
        cast_type = m.group(3).split(".")[-1]
        casts[var] = cast_type
    for m in pattern_assign.finditer(block):
        var = m.group(1)
        cast_type = m.group(2).split(".")[-1]
        casts[var] = cast_type
    return casts


def _add_field_uses(
    *,
    block: str,
    fields: List[Entity],
    param_names: Set[str],
    src_id: bytes,
    cur: sqlite3.Cursor,
    existing: Set[Tuple[bytes, bytes, str]],
) -> int:
    added = 0
    for field in fields:
        fname = field.name
        if re.search(rf"\bthis\.{re.escape(fname)}\b", block):
            if _add_dep(cur, existing, src_id, field.id, "Use"):
                added += 1
            continue
        if fname in param_names:
            continue
        # Bare field usage (assignment/member/index), avoid obj.field
        if re.search(rf"(?<![\w$.]){re.escape(fname)}\s*(=|\.|\[)", block):
            if _add_dep(cur, existing, src_id, field.id, "Use"):
                added += 1
    return added


def _resolve_method_by_name(methods: List[Entity], name: str) -> Optional[Entity]:
    for method in methods:
        if method.name == name:
            return method
    return None


def _constructor_block(content: str, start_row: int, end_row: int) -> str:
    lines = content.splitlines()
    if start_row <= 0 or end_row <= 0:
        return ""
    start = max(0, start_row - 1)
    end = min(len(lines), end_row)
    return "\n".join(lines[start:end])


def _add_dep(
    cur: sqlite3.Cursor,
    existing: Set[Tuple[bytes, bytes, str]],
    src: bytes,
    tgt: bytes,
    kind: str,
) -> bool:
    key = (src, tgt, kind)
    if key in existing:
        return False
    cur.execute(
        "INSERT INTO deps (src, tgt, kind, row, commit_id) VALUES (?, ?, ?, 0, NULL)",
        (src, tgt, kind),
    )
    existing.add(key)
    return True


def enhance_java_dependencies(db_path: Path, source_root: Optional[Path] = None) -> Tuple[int, int, int]:
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    entities = _load_entities(conn)
    contents = _load_contents(conn)

    # Build maps
    file_ids = {eid for eid, ent in entities.items() if ent.kind == "File"}
    file_content_by_id: Dict[bytes, str] = {}
    for fid in file_ids:
        content = contents.get(entities[fid].content_id, "")
        file_content_by_id[fid] = content or ""

    fields_by_class: Dict[bytes, List[Entity]] = {}
    ctors_by_class: Dict[bytes, List[Entity]] = {}
    methods_by_class: Dict[bytes, List[Entity]] = {}
    class_by_file_and_name: Dict[Tuple[bytes, str], bytes] = {}
    class_by_name: Dict[str, List[bytes]] = {}
    for ent in entities.values():
        if ent.kind == "Field" and ent.parent_id in entities and entities[ent.parent_id].kind == "Class":
            fields_by_class.setdefault(ent.parent_id, []).append(ent)
        if ent.kind == "Constructor" and ent.parent_id in entities and entities[ent.parent_id].kind == "Class":
            ctors_by_class.setdefault(ent.parent_id, []).append(ent)
        if ent.kind == "Method" and ent.parent_id in entities and entities[ent.parent_id].kind == "Class":
            class_ent = entities[ent.parent_id]
            if _is_ctor_method(ent, class_ent):
                ctors_by_class.setdefault(ent.parent_id, []).append(ent)
            else:
                methods_by_class.setdefault(ent.parent_id, []).append(ent)
        if ent.kind == "Class":
            file_id = _ancestor_file_id(entities, ent.id)
            if file_id is not None:
                class_by_file_and_name[(file_id, ent.name)] = ent.id
            class_by_name.setdefault(ent.name, []).append(ent.id)

    # Inheritance map from Extend deps
    cur.execute("SELECT src, tgt FROM deps WHERE kind = 'Extend'")
    base_by_class: Dict[bytes, bytes] = {}
    for child_id, parent_id in cur.fetchall():
        if child_id in entities and parent_id in entities:
            if entities[child_id].kind == "Class" and entities[parent_id].kind == "Class":
                base_by_class.setdefault(child_id, parent_id)

    # Existing deps
    cur.execute("SELECT src, tgt, kind FROM deps")
    existing = {(row[0], row[1], row[2]) for row in cur.fetchall()}

    added_use = 0
    added_call = 0
    added_create = 0

    all_class_ids = set(fields_by_class) | set(ctors_by_class) | set(methods_by_class)
    for class_id in all_class_ids:
        fields = fields_by_class.get(class_id, [])
        ctors = ctors_by_class.get(class_id, [])
        methods = methods_by_class.get(class_id, [])
        file_id = _ancestor_file_id(entities, class_id)
        if file_id is None:
            continue
        content = file_content_by_id.get(file_id, "")
        if not content:
            continue

        blocks: Dict[bytes, str] = {}

        for method in methods + ctors:
            block = _constructor_block(content, method.start_row, method.end_row)
            if not block:
                continue
            block = _strip_comments(block)
            blocks[method.id] = block

            signature = block.split("{", 1)[0]
            param_names = _parse_param_names(signature)
            if fields:
                added_use += _add_field_uses(
                    block=block,
                    fields=fields,
                    param_names=param_names,
                    src_id=method.id,
                    cur=cur,
                    existing=existing,
                )

            # Polymorphic calls after separate-line casts:
            #   var = (CastType) question; var.method(...)
            casts = _extract_cast_assignments(block)
            if casts:
                for m in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(", block):
                    recv = m.group(1)
                    callee = m.group(2)
                    if recv in {"this", "super"}:
                        continue
                    cast_type = casts.get(recv)
                    if not cast_type:
                        continue
                    tgt_class_id = class_by_file_and_name.get((file_id, cast_type))
                    if tgt_class_id is None:
                        candidates = class_by_name.get(cast_type) or []
                        if len(candidates) == 1:
                            tgt_class_id = candidates[0]
                    if tgt_class_id is None:
                        continue
                    tgt_method = _resolve_method_by_name(methods_by_class.get(tgt_class_id, []), callee)
                    if tgt_method is None:
                        continue
                    if _add_dep(cur, existing, method.id, tgt_method.id, "Call"):
                        added_call += 1

        # Constructor chaining calls (explicit + implicit)
        for ctor in ctors:
            block = blocks.get(ctor.id, "")
            if not block:
                continue
            has_super = re.search(r"\bsuper\s*\(", block) is not None
            has_this = re.search(r"\bthis\s*\(", block) is not None
            if has_super:
                base_id = base_by_class.get(class_id)
                if base_id is not None:
                    base_ctors = ctors_by_class.get(base_id, [])
                    if base_ctors:
                        if _add_dep(cur, existing, ctor.id, base_ctors[0].id, "Call"):
                            added_call += 1
            if has_this:
                # Call another constructor in same class (if present and not self)
                for other in ctors:
                    if other.id != ctor.id:
                        if _add_dep(cur, existing, ctor.id, other.id, "Call"):
                            added_call += 1
                        break
            if not has_super and not has_this:
                # Implicit super() call if the class has a base class.
                base_id = base_by_class.get(class_id)
                if base_id is not None:
                    base_ctors = ctors_by_class.get(base_id, [])
                    if base_ctors:
                        if _add_dep(cur, existing, ctor.id, base_ctors[0].id, "Call"):
                            added_call += 1

    # Add Create edges for `new ClassName(...)` in methods/constructors
    for class_id, methods in methods_by_class.items():
        file_id = _ancestor_file_id(entities, class_id)
        if file_id is None:
            continue
        content = file_content_by_id.get(file_id, "")
        if not content:
            continue
        for method in methods + ctors_by_class.get(class_id, []):
            block = _constructor_block(content, method.start_row, method.end_row)
            if not block:
                continue
            block = _strip_comments(block)
            for m in re.finditer(r"\bnew\s+([A-Za-z_][A-Za-z0-9_$.]*)", block):
                raw = m.group(1).split("<", 1)[0]
                simple = raw.split(".")[-1]
                tgt_id = class_by_file_and_name.get((file_id, simple))
                if tgt_id is None:
                    candidates = class_by_name.get(simple) or []
                    if len(candidates) == 1:
                        tgt_id = candidates[0]
                if tgt_id is None:
                    continue
                if _add_dep(cur, existing, method.id, tgt_id, "Create"):
                    added_create += 1

    conn.commit()
    conn.close()
    return added_use, added_call, added_create


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", type=Path)
    parser.add_argument("source_root", type=Path, nargs="?")
    args = parser.parse_args()

    if not args.db_path.exists():
        print(f"Error: DB not found: {args.db_path}")
        return 1

    added_use, added_call, added_create = enhance_java_dependencies(args.db_path, args.source_root)
    print(f"[OK] Added Java deps: Use={added_use}, Call={added_call}, Create={added_create}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
