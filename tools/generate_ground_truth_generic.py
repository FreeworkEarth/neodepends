#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple


KINDS = ("Import", "Extend", "Create", "Call", "Use")


@dataclass(frozen=True)
class MethodSig:
    name: str
    params: Dict[str, Optional[str]]  # param -> annotation name (simple)


@dataclass
class ClassInfo:
    file: str
    name: str
    bases: List[str]  # unresolved names
    methods: Dict[str, MethodSig]
    class_vars: Set[str]
    instance_fields: Set[str]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _iter_project_py(project_root: Path, *, exclude_init: bool) -> List[Path]:
    """
    Recursively collect Python files under `project_root`, skipping common junk directories.
    """
    skip_dir_names = {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        "site-packages",
        "node_modules",
        "dependencies_files_handcount",
    }

    out: List[Path] = []
    for p in project_root.rglob("*.py"):
        if any((part in skip_dir_names) or part.startswith("dependencies_files_handcount") for part in p.parts):
            continue
        if p.name.startswith("."):
            continue
        if exclude_init and p.name == "__init__.py":
            continue
        out.append(p)
    return sorted(out)

def _iter_class_defs(body: List[ast.stmt], *, prefix: str = "") -> Iterable[Tuple[str, ast.ClassDef]]:
    """
    Yield (full_class_name, ClassDef) for all classes, including nested classes.

    Nested classes are named `Outer.Inner` to match the DV8/handcount naming convention
    used elsewhere in this workspace.
    """
    for node in body:
        if not isinstance(node, ast.ClassDef):
            continue
        full = f"{prefix}.{node.name}" if prefix else node.name
        yield full, node
        yield from _iter_class_defs(node.body, prefix=full)


def _simple_name(expr: ast.AST) -> Optional[str]:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    return None


def _ann_name(expr: Optional[ast.AST]) -> Optional[str]:
    if expr is None:
        return None
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    if isinstance(expr, ast.Subscript):
        return _ann_name(expr.value)
    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return expr.value
    return None


def _module_to_file(project_root: Path, *, current_file: str, module: str, level: int) -> Optional[str]:
    """
    Best-effort import resolution:

    - Absolute: `a.b.c` -> `a/b/c.py` or `a/b/c/__init__.py`
    - Relative: `from .x import y` where `level>=1` resolves relative to current file's parent.
    """
    base_dir = project_root
    if level and level > 0:
        cur_path = project_root / current_file
        pkg_dir = cur_path.parent
        for _ in range(level - 1):
            pkg_dir = pkg_dir.parent
        base_dir = pkg_dir

    parts = [p for p in module.split(".") if p]
    candidate_py = base_dir.joinpath(*parts).with_suffix(".py")
    if candidate_py.exists():
        try:
            return candidate_py.relative_to(project_root).as_posix()
        except ValueError:
            return candidate_py.as_posix()

    candidate_pkg_init = base_dir.joinpath(*parts, "__init__.py")
    if candidate_pkg_init.exists():
        try:
            return candidate_pkg_init.relative_to(project_root).as_posix()
        except ValueError:
            return candidate_pkg_init.as_posix()

    return None


def var_name_for_entity(file: str, kind: str, class_name: Optional[str], name: str) -> str:
    if kind == "File":
        return f"{file}/module (Module)"
    if kind == "Function":
        return f"{file}/FUNCTIONS/{name} (Function)"
    if kind == "Class":
        return f"{file}/CLASSES/{name} (Class)"
    if kind == "Method":
        assert class_name is not None
        if name == "__init__":
            return f"{file}/CLASSES/{class_name}/CONSTRUCTORS/{name} (Constructor)"
        return f"{file}/CLASSES/{class_name}/METHODS/{name} (Method)"
    if kind == "Field":
        assert class_name is not None
        return f"{file}/CLASSES/{class_name}/FIELDS/{name} (Field)"
    raise ValueError(kind)


def collect_classes(project_root: Path, files: List[Path]) -> Dict[Tuple[str, str], ClassInfo]:
    classes: Dict[Tuple[str, str], ClassInfo] = {}

    for path in files:
        rel = path.relative_to(project_root).as_posix()
        tree = ast.parse(_read(path), filename=rel)
        for full_name, node in _iter_class_defs(tree.body):
            bases = [n for n in (_simple_name(b) for b in node.bases) if n]
            methods: Dict[str, MethodSig] = {}
            class_vars: Set[str] = set()
            instance_fields: Set[str] = set()

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    params: Dict[str, Optional[str]] = {}
                    args = item.args.args or []
                    for a in args:
                        if a.arg in {"self", "cls"}:
                            continue
                        params[a.arg] = _ann_name(a.annotation)
                    methods[item.name] = MethodSig(name=item.name, params=params)

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
                                    instance_fields.add(t.attr)

                if isinstance(item, ast.Assign):
                    for t in item.targets:
                        if isinstance(t, ast.Name):
                            class_vars.add(t.id)
                if isinstance(item, ast.AnnAssign):
                    if isinstance(item.target, ast.Name):
                        class_vars.add(item.target.id)

            classes[(rel, full_name)] = ClassInfo(
                file=rel,
                name=full_name,
                bases=bases,
                methods=methods,
                class_vars=class_vars,
                instance_fields=instance_fields,
            )

    return classes


def build_indexes(classes: Dict[Tuple[str, str], ClassInfo]) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    class_methods: Dict[str, Set[str]] = {}
    class_to_file: Dict[str, str] = {}
    for (_file, cls_name), info in classes.items():
        class_methods.setdefault(cls_name, set()).update(info.methods.keys())
        class_to_file.setdefault(cls_name, info.file)
    return class_methods, class_to_file


def inherited_fields(classes: Dict[Tuple[str, str], ClassInfo], class_to_file: Dict[str, str]) -> Dict[str, Set[str]]:
    own: Dict[str, Set[str]] = {}
    bases: Dict[str, List[str]] = {}
    for (_file, cls_name), info in classes.items():
        # Treat both instance attributes (self.x assigned in methods) and class-level attributes
        # (including annotated dataclass fields) as "fields" for the purposes of Use edges.
        #
        # This avoids systematically undercounting field-uses in common patterns like:
        #   @dataclass
        #   class Foo:
        #       x: int = 0
        #       def bar(self): return self.x
        own.setdefault(cls_name, set()).update(info.instance_fields | info.class_vars)
        bases.setdefault(cls_name, []).extend([b for b in info.bases if b in class_to_file])

    memo: Dict[str, Set[str]] = {}

    def dfs(c: str, stack: Set[str]) -> Set[str]:
        if c in memo:
            return memo[c]
        if c in stack:
            return set(own.get(c, set()))
        stack.add(c)
        out = set(own.get(c, set()))
        for b in bases.get(c, []):
            out |= dfs(b, stack)
        stack.remove(c)
        memo[c] = out
        return out

    return {c: dfs(c, set()) for c in own.keys()}


def _first_resolvable_base(cls: str, bases_by_class: Dict[str, List[str]]) -> Optional[str]:
    for b in bases_by_class.get(cls, []):
        return b
    return None


def _find_field_owner(
    cls: str, field: str, *, own_fields_by_class: Dict[str, Set[str]], bases_by_class: Dict[str, List[str]]
) -> Optional[str]:
    if field in own_fields_by_class.get(cls, set()):
        return cls
    seen: Set[str] = set()
    queue: List[str] = list(bases_by_class.get(cls, []))
    while queue:
        b = queue.pop(0)
        if b in seen:
            continue
        seen.add(b)
        if field in own_fields_by_class.get(b, set()):
            return b
        queue.extend(bases_by_class.get(b, []))
    return None


def compute_edges(
    project_root: Path,
    files: List[Path],
    *,
    profile: str,
) -> Tuple[Dict[str, Dict[str, Set[Tuple[str, str, str]]]], List[Tuple[str, str, str]]]:
    classes = collect_classes(project_root, files)
    class_methods, class_to_file = build_indexes(classes)
    fields_by_class = inherited_fields(classes, class_to_file)
    bases_by_class: Dict[str, List[str]] = {}
    own_fields_by_class: Dict[str, Set[str]] = {}
    for (_f, cls), info in classes.items():
        bases_by_class.setdefault(cls, []).extend([b for b in info.bases if b in class_to_file])
        own_fields_by_class.setdefault(cls, set()).update(info.instance_fields)
        own_fields_by_class.setdefault(cls, set()).update(info.class_vars)

    method_param_types: Dict[Tuple[str, str, str], Dict[str, str]] = {}
    for (f, cls), info in classes.items():
        for mname, sig in info.methods.items():
            tmap: Dict[str, str] = {}
            for param, ann in sig.params.items():
                if ann and ann in class_to_file:
                    tmap[param] = ann
            method_param_types[(f, cls, mname)] = tmap

    edges_by_file: Dict[str, Dict[str, Set[Tuple[str, str, str]]]] = {}

    def add_edge(src_file: str, kind: str, src: str, tgt: str) -> None:
        edges_by_file.setdefault(src_file, {}).setdefault(kind, set()).add((src, tgt, kind))

    def method_var(cls: str, method: str) -> Optional[str]:
        if cls not in class_to_file:
            return None
        if method not in class_methods.get(cls, set()):
            return None
        return var_name_for_entity(class_to_file[cls], "Method", cls, method)

    def resolve_method_var_in_hierarchy(start_cls: str, method: str) -> Optional[str]:
        direct = method_var(start_cls, method)
        if direct:
            return direct
        seen: Set[str] = set()
        queue: List[str] = list(bases_by_class.get(start_cls, []))
        while queue:
            b = queue.pop(0)
            if b in seen:
                continue
            seen.add(b)
            v = method_var(b, method)
            if v:
                return v
            queue.extend(bases_by_class.get(b, []))
        return None

    def _guess_class_from_var(var: str) -> Optional[str]:
        camel = "".join(p.capitalize() for p in var.split("_") if p)
        return camel if camel in class_to_file else None

    def _unique_method_owner(method: str) -> Optional[str]:
        owners = [cls for cls, methods in class_methods.items() if method in methods]
        if len(owners) == 1:
            return owners[0]
        return None

    for path in files:
        src_file = path.relative_to(project_root).as_posix()
        tree = ast.parse(_read(path), filename=src_file)
        src_file_var = var_name_for_entity(src_file, "File", None, src_file)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    tgt_file = _module_to_file(project_root, current_file=src_file, module=alias.name, level=0)
                    if tgt_file:
                        tgt_var = var_name_for_entity(tgt_file, "File", None, tgt_file)
                        add_edge(src_file, "Import", src_file_var, tgt_var)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                tgt_file = _module_to_file(project_root, current_file=src_file, module=mod, level=int(node.level or 0))
                if tgt_file:
                    tgt_var = var_name_for_entity(tgt_file, "File", None, tgt_file)
                    add_edge(src_file, "Import", src_file_var, tgt_var)

        for cls_name, node in _iter_class_defs(tree.body):
            src_class_var = var_name_for_entity(src_file, "Class", None, cls_name)
            for b in node.bases:
                base = _simple_name(b)
                if not base or base not in class_to_file:
                    continue
                tgt_class_var = var_name_for_entity(class_to_file[base], "Class", None, base)
                add_edge(src_file, "Extend", src_class_var, tgt_class_var)

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                src_func = var_name_for_entity(src_file, "Function", None, node.name)
                _extract_body_edges(
                    project_root=project_root,
                    src_file=src_file,
                    src_entity_var=src_func,
                    body=node.body,
                    current_class=None,
                    class_to_file=class_to_file,
                    class_methods=class_methods,
                    fields_by_class=fields_by_class,
                    bases_by_class=bases_by_class,
                    own_fields_by_class=own_fields_by_class,
                    method_param_types=None,
                    add_edge=add_edge,
                    method_var=method_var,
                    profile=profile,
                    guess_class_from_var=_guess_class_from_var,
                    unique_method_owner=_unique_method_owner,
                    resolve_method_var_in_hierarchy=resolve_method_var_in_hierarchy,
                )

        for cls_name, node in _iter_class_defs(tree.body):
            for item in node.body:
                if not isinstance(item, ast.FunctionDef):
                    continue
                src_method = var_name_for_entity(src_file, "Method", cls_name, item.name)
                _extract_body_edges(
                    project_root=project_root,
                    src_file=src_file,
                    src_entity_var=src_method,
                    body=item.body,
                    current_class=cls_name,
                    class_to_file=class_to_file,
                    class_methods=class_methods,
                    fields_by_class=fields_by_class,
                    bases_by_class=bases_by_class,
                    own_fields_by_class=own_fields_by_class,
                    method_param_types=method_param_types.get((src_file, cls_name, item.name), {}),
                    add_edge=add_edge,
                    method_var=method_var,
                    profile=profile,
                    guess_class_from_var=_guess_class_from_var,
                    unique_method_owner=_unique_method_owner,
                    resolve_method_var_in_hierarchy=resolve_method_var_in_hierarchy,
                )

    all_edges: List[Tuple[str, str, str]] = []
    for f, by_kind in edges_by_file.items():
        for _k, edges in by_kind.items():
            all_edges.extend(sorted(edges))
    return edges_by_file, all_edges


def _extract_body_edges(
    *,
    project_root: Path,
    src_file: str,
    src_entity_var: str,
    body: List[ast.stmt],
    current_class: Optional[str],
    class_to_file: Dict[str, str],
    class_methods: Dict[str, Set[str]],
    fields_by_class: Dict[str, Set[str]],
    bases_by_class: Dict[str, List[str]],
    own_fields_by_class: Dict[str, Set[str]],
    method_param_types: Optional[Dict[str, str]],
    add_edge: Any,
    method_var: Any,
    profile: str,
    guess_class_from_var: Any,
    unique_method_owner: Any,
    resolve_method_var_in_hierarchy: Any,
) -> None:
    env: Dict[str, str] = {}
    if method_param_types:
        env.update(method_param_types)

    self_field_type: Dict[str, str] = {}

    for stmt in ast.walk(ast.Module(body=body, type_ignores=[])):
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            var = stmt.targets[0].id
            if isinstance(stmt.value, ast.Call):
                cname = _simple_name(stmt.value.func)
                if cname and cname in class_to_file:
                    env[var] = cname
            if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Attribute):
                if isinstance(stmt.value.func.value, ast.Name):
                    base = stmt.value.func.value.id
                    if base in class_to_file and stmt.value.func.attr == "get_instance":
                        env[var] = base

        if (
            isinstance(stmt, ast.Assign)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Attribute)
            and isinstance(stmt.targets[0].value, ast.Name)
            and stmt.targets[0].value.id == "self"
            and isinstance(stmt.value, ast.Name)
            and method_param_types
            and stmt.value.id in method_param_types
        ):
            self_field_type[stmt.targets[0].attr] = method_param_types[stmt.value.id]

    for node in ast.walk(ast.Module(body=body, type_ignores=[])):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
            if current_class and node.attr in fields_by_class.get(current_class, set()):
                owner = _find_field_owner(
                    current_class, node.attr, own_fields_by_class=own_fields_by_class, bases_by_class=bases_by_class
                )
                if owner:
                    tgt = var_name_for_entity(class_to_file[owner], "Field", owner, node.attr)
                    add_edge(src_file, "Use", src_entity_var, tgt)

        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in class_to_file
            and node.attr in own_fields_by_class.get(node.value.id, set())
        ):
            tgt = var_name_for_entity(class_to_file[node.value.id], "Field", node.value.id, node.attr)
            add_edge(src_file, "Use", src_entity_var, tgt)

        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name):
            cname = node.func.id
            if cname in class_to_file:
                tgt = var_name_for_entity(class_to_file[cname], "Class", None, cname)
                add_edge(src_file, "Create", src_entity_var, tgt)
            continue

        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            receiver = node.func.value

            if (
                isinstance(receiver, ast.Call)
                and isinstance(receiver.func, ast.Name)
                and receiver.func.id == "super"
                and current_class
            ):
                base = _first_resolvable_base(current_class, bases_by_class)
                if base:
                    tgt = method_var(base, attr)
                    if tgt:
                        add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            if isinstance(receiver, ast.Name) and receiver.id == "self" and current_class:
                tgt = resolve_method_var_in_hierarchy(current_class, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            if isinstance(receiver, ast.Name) and receiver.id in class_to_file:
                tgt = method_var(receiver.id, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            if isinstance(receiver, ast.Name) and receiver.id in env:
                cls = env[receiver.id]
                tgt = method_var(cls, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            if profile != "strict" and isinstance(receiver, ast.Name):
                guessed = guess_class_from_var(receiver.id)
                owner = guessed or unique_method_owner(attr)
                if owner:
                    tgt = method_var(owner, attr)
                    if tgt:
                        add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            if (
                isinstance(receiver, ast.Attribute)
                and isinstance(receiver.value, ast.Name)
                and receiver.value.id == "self"
                and receiver.attr in self_field_type
            ):
                cls = self_field_type[receiver.attr]
                tgt = method_var(cls, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue


def _var_sort_key(var: str) -> Tuple[int, str, int, str, str]:
    if var.startswith("(External "):
        return (9, var, 9, "", var)

    file_path = var
    if ".py/" in var:
        file_path = var.split(".py/", 1)[0] + ".py"
    elif var.endswith(".py"):
        file_path = var

    file_group = 0 if "/" in file_path else 1

    if var.endswith("/module (Module)"):
        type_rank = 0
    elif "/FUNCTIONS/" in var:
        type_rank = 1
    elif "/CLASSES/" in var and var.endswith(" (Class)") and "/FIELDS/" not in var and "/METHODS/" not in var and "/CONSTRUCTORS/" not in var:
        type_rank = 2
    elif "/CONSTRUCTORS/" in var:
        type_rank = 3
    elif "/METHODS/" in var:
        type_rank = 4
    elif "/FIELDS/" in var:
        type_rank = 5
    else:
        type_rank = 8

    class_name = ""
    if "/CLASSES/" in var:
        after = var.split("/CLASSES/", 1)[1]
        class_name = after.split("/", 1)[0].replace(" (Class)", "")

    leaf = var.rsplit("/", 1)[-1]
    member_name = leaf.split(" (", 1)[0]

    return (file_group, file_path, type_rank, class_name, member_name)


def dv8_from_edges(*, name: str, edges: Iterable[Tuple[str, str, str]], collapse_to_use: bool) -> Dict[str, Any]:
    variables: List[str] = []
    idx: Dict[str, int] = {}
    cells_map: Dict[Tuple[int, int], Dict[str, float]] = {}

    def ensure(v: str) -> int:
        if v in idx:
            return idx[v]
        idx[v] = len(variables)
        variables.append(v)
        return idx[v]

    for src, tgt, kind in edges:
        k = "Use" if collapse_to_use else kind
        s = ensure(src)
        t = ensure(tgt)
        key = (s, t)
        vals = cells_map.setdefault(key, {})
        vals[k] = float(vals.get(k, 0.0) + 1.0)

    # reorder variables deterministically
    order = sorted(range(len(variables)), key=lambda i: _var_sort_key(variables[i]))
    old_to_new = {old: new for new, old in enumerate(order)}
    new_vars = [variables[i] for i in order]

    new_cells = []
    for (s, t), vals in cells_map.items():
        new_cells.append({"src": old_to_new[s], "dest": old_to_new[t], "values": vals})
    new_cells.sort(key=lambda c: (c["src"], c["dest"]))

    return {"@schemaVersion": "1.0", "name": name, "variables": new_vars, "cells": new_cells}


def dv8_file_level(*, name: str, edges: Iterable[Tuple[str, str, str]], all_files: List[str]) -> Dict[str, Any]:
    variables = [f"{f}/module (Module)" for f in all_files]
    idx = {v: i for i, v in enumerate(variables)}
    cells_map: Dict[Tuple[int, int], Dict[str, float]] = {}

    def file_of(var: str) -> Optional[str]:
        if ".py/" in var:
            return var.split(".py/")[0] + ".py"
        if var.endswith(".py"):
            return var
        return None

    for src, tgt, kind in edges:
        sf = file_of(src)
        tf = file_of(tgt)
        if not sf or not tf:
            continue
        s = idx.get(f"{sf}/module (Module)")
        t = idx.get(f"{tf}/module (Module)")
        if s is None or t is None:
            continue
        key = (s, t)
        vals = cells_map.setdefault(key, {})
        vals[kind] = float(vals.get(kind, 0.0) + 1.0)

    cells = [{"src": s, "dest": t, "values": vals} for (s, t), vals in sorted(cells_map.items())]
    return {"@schemaVersion": "1.0", "name": name, "variables": variables, "cells": cells}


def write_md_files(
    *, out_dir: Path, all_files: Iterable[str], edges_by_file: Dict[str, Dict[str, Set[Tuple[str, str, str]]]]
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for file in sorted(all_files):
        by_kind = edges_by_file.get(file, {})
        md_rel = Path(file).with_suffix(".md")
        md_path = out_dir / md_rel
        md_path.parent.mkdir(parents=True, exist_ok=True)

        lines: List[str] = [f"# `{file}`", ""]
        totals = {k: len(by_kind.get(k, set())) for k in KINDS}
        lines.append("## Totals (unique edges, internal-only)")
        lines.append("")
        for k in KINDS:
            lines.append(f"- {k}: {totals.get(k, 0)}")
        lines.append(f"- Total: {sum(totals.values())}")
        lines.append("")

        for k in KINDS:
            edges = sorted(by_kind.get(k, set()))
            if not edges:
                continue
            lines.append(f"## {k} edges")
            lines.append("")
            for src, tgt, _kind in edges:
                lines.append(f"- {src} -> {tgt}")
            lines.append("")

        md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--profile", choices=["strict", "heuristic"], default="heuristic")
    parser.add_argument("--exclude-init", action="store_true", default=True)
    parser.add_argument("--include-init", dest="exclude_init", action="store_false")
    args = parser.parse_args()

    project_root = args.project_root.expanduser().resolve()
    out_dir = args.out_dir.expanduser().resolve()
    files = _iter_project_py(project_root, exclude_init=bool(args.exclude_init))
    rel_files = [p.relative_to(project_root).as_posix() for p in files]

    edges_by_file, all_edges = compute_edges(project_root, files, profile=args.profile)

    write_md_files(out_dir=out_dir, all_files=rel_files, edges_by_file=edges_by_file)

    suffix = "" if args.profile == "strict" else f".{args.profile}"
    (out_dir / f"handcount_edges{suffix}.json").write_text(json.dumps(all_edges, indent=2), encoding="utf-8")

    dv8_use = dv8_from_edges(name=f"handcount ({args.profile}, collapsed Use)", edges=all_edges, collapse_to_use=True)
    (out_dir / f"handcount_full{suffix}.dv8-dependency.json").write_text(json.dumps(dv8_use, indent=2), encoding="utf-8")

    dv8_kinds = dv8_from_edges(name=f"handcount ({args.profile}, typed)", edges=all_edges, collapse_to_use=False)
    (out_dir / f"handcount_full_typed{suffix}.dv8-dependency.json").write_text(json.dumps(dv8_kinds, indent=2), encoding="utf-8")

    dv8_files = dv8_file_level(
        name=f"handcount ({args.profile}, file-level typed)", edges=all_edges, all_files=sorted(rel_files)
    )
    (out_dir / f"handcount_filelevel{suffix}.dv8-dependency.json").write_text(json.dumps(dv8_files, indent=2), encoding="utf-8")

    print(f"[OK] Wrote md + DV8 DSMs into: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
