#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import os
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
    # fields assigned to self.<x> anywhere in class
    instance_fields: Set[str]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _is_root_py(path_str: str) -> bool:
    return "/" not in path_str and path_str.endswith(".py")


def _iter_project_py(project_root: Path) -> List[Path]:
    files: List[Path] = []
    for p in project_root.glob("*.py"):
        if p.name.startswith("."):
            continue
        files.append(p)
    tts = project_root / "tts"
    if tts.is_dir():
        files.extend(sorted(tts.rglob("*.py")))
    return sorted(files)


def _module_to_file(project_root: Path, module: str) -> Optional[str]:
    """
    Only supports `tts.xxx` modules and root-level modules.
    Returns workspace-relative file path (posix).
    """
    if module.startswith("tts."):
        rel = Path("tts") / Path(*module.split(".")[1:])
        py = (project_root / rel).with_suffix(".py")
        if py.exists():
            return py.relative_to(project_root).as_posix()
    if module == "tts":
        init = project_root / "tts" / "__init__.py"
        if init.exists():
            return init.relative_to(project_root).as_posix()
    # root module
    py = (project_root / module).with_suffix(".py")
    if py.exists():
        return py.relative_to(project_root).as_posix()
    return None


def _simple_name(expr: ast.AST) -> Optional[str]:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        # only keep tail name (e.g. tts.ticket.Ticket -> Ticket)
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
        # forward ref: "TicketBookingSystem"
        return expr.value
    return None


def collect_classes(project_root: Path, files: List[Path]) -> Dict[Tuple[str, str], ClassInfo]:
    classes: Dict[Tuple[str, str], ClassInfo] = {}

    for path in files:
        rel = path.relative_to(project_root).as_posix()
        tree = ast.parse(_read(path), filename=rel)
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
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

                    # find self.<field> assignments in method
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
                                if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == "self":
                                    instance_fields.add(t.attr)

                # class var assignment inside class body
                if isinstance(item, ast.Assign):
                    for t in item.targets:
                        if isinstance(t, ast.Name):
                            class_vars.add(t.id)
                if isinstance(item, ast.AnnAssign):
                    if isinstance(item.target, ast.Name):
                        class_vars.add(item.target.id)

            classes[(rel, node.name)] = ClassInfo(
                file=rel,
                name=node.name,
                bases=bases,
                methods=methods,
                class_vars=class_vars,
                instance_fields=instance_fields,
            )

    return classes


def build_indexes(classes: Dict[Tuple[str, str], ClassInfo]) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    """
    Returns:
      - class_methods[class_name] -> set(method_names)
      - class_to_file[class_name] -> file path (first occurrence wins)
    """
    class_methods: Dict[str, Set[str]] = {}
    class_to_file: Dict[str, str] = {}
    for (_file, cls_name), info in classes.items():
        class_methods.setdefault(cls_name, set()).update(info.methods.keys())
        class_to_file.setdefault(cls_name, info.file)
    return class_methods, class_to_file


def resolve_base_class_name(base: str, class_to_file: Dict[str, str]) -> Optional[str]:
    return base if base in class_to_file else None


def inherited_fields(
    classes: Dict[Tuple[str, str], ClassInfo],
    class_to_file: Dict[str, str],
) -> Dict[str, Set[str]]:
    """
    Map class name -> instance fields including inherited (project-local) fields.
    """
    own: Dict[str, Set[str]] = {}
    bases: Dict[str, List[str]] = {}
    for (_file, cls_name), info in classes.items():
        own.setdefault(cls_name, set()).update(info.instance_fields)
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


def var_name_for_entity(file: str, kind: str, class_name: Optional[str], name: str) -> str:
    if kind == "File":
        # Represent the file as a module node inside the file folder.
        # This avoids DV8 showing both a folder `tts/x.py` and a separate leaf `tts/x.py (File)`.
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


def compute_edges(
    project_root: Path,
    files: List[Path],
    *,
    profile: str,
) -> Tuple[Dict[str, Dict[str, Set[Tuple[str, str, str]]]], List[Tuple[str, str, str]]]:
    """
    Returns:
      - edges_by_file[file][kind] -> set of (src_var, tgt_var, kind)
      - all_edges -> list of all edges (src_var, tgt_var, kind)
    """
    classes = collect_classes(project_root, files)
    class_methods, class_to_file = build_indexes(classes)
    fields_by_class = inherited_fields(classes, class_to_file)
    bases_by_class: Dict[str, List[str]] = {}
    own_fields_by_class: Dict[str, Set[str]] = {}
    for (_f, cls), info in classes.items():
        bases_by_class.setdefault(cls, []).extend([b for b in info.bases if b in class_to_file])
        # "own" means defined in the class body, not inherited.
        own_fields_by_class.setdefault(cls, set()).update(info.instance_fields)
        own_fields_by_class.setdefault(cls, set()).update(info.class_vars)

    # Build method parameter type map for each class method.
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

    # helper: resolve a method name on a class to a var string
    def method_var(cls: str, method: str) -> Optional[str]:
        if cls not in class_to_file:
            return None
        if method not in class_methods.get(cls, set()):
            return None
        return var_name_for_entity(class_to_file[cls], "Method", cls, method)

    def resolve_method_var_in_hierarchy(start_cls: str, method: str) -> Optional[str]:
        # Resolve a method defined on the class or inherited from project-local bases.
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
        # heuristic: passenger -> Passenger, station_manager -> StationManager
        camel = "".join(p.capitalize() for p in var.split("_") if p)
        return camel if camel in class_to_file else None

    def _unique_method_owner(method: str) -> Optional[str]:
        # heuristic: if exactly one internal class has this method name, assume it's the owner.
        owners = [cls for cls, methods in class_methods.items() if method in methods]
        if len(owners) == 1:
            return owners[0]
        return None

    # For each file parse and extract edges.
    for path in files:
        src_file = path.relative_to(project_root).as_posix()
        tree = ast.parse(_read(path), filename=src_file)

        # Index internal file var (for Import edges).
        src_file_var = var_name_for_entity(src_file, "File", None, src_file)

        # 1) Imports (File -> File)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod = alias.name
                    tgt_file = _module_to_file(project_root, mod)
                    if tgt_file:
                        tgt_var = var_name_for_entity(tgt_file, "File", None, tgt_file)
                        add_edge(src_file, "Import", src_file_var, tgt_var)
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                mod = node.module
                tgt_file = _module_to_file(project_root, mod)
                if tgt_file:
                    tgt_var = var_name_for_entity(tgt_file, "File", None, tgt_file)
                    add_edge(src_file, "Import", src_file_var, tgt_var)

        # 2) Class inheritance edges (Class -> Class)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                src_class_var = var_name_for_entity(src_file, "Class", None, node.name)
                for b in node.bases:
                    base = _simple_name(b)
                    if not base:
                        continue
                    resolved = resolve_base_class_name(base, class_to_file)
                    if resolved:
                        tgt_class_var = var_name_for_entity(class_to_file[resolved], "Class", None, resolved)
                        add_edge(src_file, "Extend", src_class_var, tgt_class_var)

        # 3) Function + method bodies (Create/Call/Use)
        # We extract for:
        # - module-level functions
        # - class methods

        # module-level functions
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

        # class methods
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            cls_name = node.name
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

    # flatten
    all_edges: List[Tuple[str, str, str]] = []
    for f, by_kind in edges_by_file.items():
        for k, edges in by_kind.items():
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
    """
    Walk a function/method body and add Create/Call/Use edges when resolvable.
    """

    # Very small local type environment: var -> class name
    env: Dict[str, str] = {}
    if method_param_types:
        env.update(method_param_types)

    # Track field types inferred from "self.field = param" patterns.
    self_field_type: Dict[str, str] = {}

    # Pre-scan assignments for simple env bindings within this body.
    for stmt in ast.walk(ast.Module(body=body, type_ignores=[])):
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            var = stmt.targets[0].id
            if isinstance(stmt.value, ast.Call):
                cname = _simple_name(stmt.value.func)
                if cname and cname in class_to_file:
                    env[var] = cname
            # pattern: var = ClassName.get_instance()
            if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Attribute):
                if isinstance(stmt.value.func.value, ast.Name):
                    base = stmt.value.func.value.id
                    if base in class_to_file and stmt.value.func.attr == "get_instance":
                        env[var] = base

        # pattern: self.field = param
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

    # Calls / Creates
    for node in ast.walk(ast.Module(body=body, type_ignores=[])):
        # Use: any self.<field> access (load/store) if field resolvable
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
            if current_class and node.attr in fields_by_class.get(current_class, set()):
                owner = _find_field_owner(
                    current_class,
                    node.attr,
                    own_fields_by_class=own_fields_by_class,
                    bases_by_class=bases_by_class,
                )
                if owner:
                    tgt = var_name_for_entity(class_to_file[owner], "Field", owner, node.attr)
                    add_edge(src_file, "Use", src_entity_var, tgt)

        # Use: ClassName.<field> where ClassName is project-local and field exists on that class.
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

        # Create: C(...)
        if isinstance(node.func, ast.Name):
            cname = node.func.id
            if cname in class_to_file:
                tgt = var_name_for_entity(class_to_file[cname], "Class", None, cname)
                add_edge(src_file, "Create", src_entity_var, tgt)
            continue

        # Call: obj.m(...)
        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            receiver = node.func.value

            # super().m(...)
            if (
                isinstance(receiver, ast.Call)
                and isinstance(receiver.func, ast.Name)
                and receiver.func.id == "super"
                and current_class
            ):
                # choose first resolvable base class
                base = _first_resolvable_base(current_class, bases_by_class)
                if base:
                    tgt = method_var(base, attr)
                    if tgt:
                        add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            # self.m(...)
            if isinstance(receiver, ast.Name) and receiver.id == "self" and current_class:
                tgt = resolve_method_var_in_hierarchy(current_class, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            # ClassName.m(...)
            if isinstance(receiver, ast.Name) and receiver.id in class_to_file:
                tgt = method_var(receiver.id, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            # var.m(...) where var has inferred type
            if isinstance(receiver, ast.Name) and receiver.id in env:
                cls = env[receiver.id]
                tgt = method_var(cls, attr)
                if tgt:
                    add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            # Heuristic mode: attempt to resolve untyped `var.m(...)` calls.
            if profile != "strict" and isinstance(receiver, ast.Name):
                guessed = guess_class_from_var(receiver.id)
                owner = guessed or unique_method_owner(attr)
                if owner:
                    tgt = method_var(owner, attr)
                    if tgt:
                        add_edge(src_file, "Call", src_entity_var, tgt)
                continue

            # self.field.m(...) where self.field has inferred type from __init__ param annotations
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


def _first_resolvable_base(cls: str, bases_by_class: Dict[str, List[str]]) -> Optional[str]:
    # Best-effort: pick the first project-local base class listed in the class definition.
    for b in bases_by_class.get(cls, []):
        return b
    return None


def _find_field_owner(
    cls: str,
    field: str,
    *,
    own_fields_by_class: Dict[str, Set[str]],
    bases_by_class: Dict[str, List[str]],
) -> Optional[str]:
    # Owner = nearest class in the inheritance chain that *defines* the field.
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

    # If we can't find an owner, don't invent one.
    return None


def write_md_files(
    *,
    out_dir: Path,
    all_files: Iterable[str],
    edges_by_file: Dict[str, Dict[str, Set[Tuple[str, str, str]]]],
) -> None:
    """
    Overwrite per-file markdown with rule-based results.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "tts").mkdir(parents=True, exist_ok=True)

    # Prune stale generated md files for modules that no longer exist.
    expected_tts_md_stems: Set[str] = set()
    for f in all_files:
        if f.startswith("tts/") and f.endswith(".py"):
            expected_tts_md_stems.add(Path(f).stem)
    for md in (out_dir / "tts").glob("*.md"):
        if md.stem not in expected_tts_md_stems:
            try:
                md.unlink()
            except PermissionError:
                # Some environments disallow deleting files via runtime scripts.
                # Leaving stale files is better than failing the whole generation.
                pass

    for file in sorted(all_files):
        by_kind = edges_by_file.get(file, {})
        if file == "main.py":
            rel_md = "main.md"
        elif file.startswith("tts/"):
            rel_md = f"tts/{Path(file).stem}.md"
        else:
            rel_md = f"{Path(file).stem}.md"
        md_path = out_dir / rel_md

        lines: List[str] = [f"# `{file}`", ""]

        totals = {k: len(by_kind.get(k, set())) for k in KINDS}
        total_all = sum(totals.values())

        lines.append("## Totals (unique edges, internal-only)")
        lines.append("")
        for k in KINDS:
            lines.append(f"- {k}: {totals.get(k, 0)}")
        lines.append(f"- Total: {total_all}")
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


def dv8_from_edges(
    *,
    name: str,
    edges: Iterable[Tuple[str, str, str]],
    collapse_to_use: bool,
) -> Dict[str, Any]:
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

    cells = [{"src": s, "dest": t, "values": vals} for (s, t), vals in sorted(cells_map.items())]
    return {"@schemaVersion": "1.0", "name": name, "variables": variables, "cells": cells}

def dv8_file_level(
    *,
    name: str,
    edges: Iterable[Tuple[str, str, str]],
) -> Dict[str, Any]:
    """
    File-level DSM:
    - Variables are file paths only (e.g. `tts/route.py`, `main.py`)
    - Cells aggregate all dependency kinds between files into a single Use count
    """
    variables: List[str] = []
    idx: Dict[str, int] = {}
    cells_map: Dict[Tuple[int, int], Dict[str, float]] = {}

    def ensure(v: str) -> int:
        if v in idx:
            return idx[v]
        idx[v] = len(variables)
        variables.append(v)
        return idx[v]

    def file_of(var: str) -> Optional[str]:
        # var names start with "<file>/" for everything we emit.
        if "/tts/" in var:
            # shouldn't happen; keep generic split.
            pass
        # Extract the leading "<something>.py"
        if ".py/" in var:
            return var.split(".py/")[0] + ".py"
        if var.endswith(".py"):
            return var
        return None

    for src, tgt, _kind in edges:
        sf = file_of(src)
        tf = file_of(tgt)
        if not sf or not tf:
            continue
        s = ensure(sf)
        t = ensure(tf)
        key = (s, t)
        vals = cells_map.setdefault(key, {})
        vals["Use"] = float(vals.get("Use", 0.0) + 1.0)

    cells = [{"src": s, "dest": t, "values": vals} for (s, t), vals in sorted(cells_map.items())]
    return {"@schemaVersion": "1.0", "name": name, "variables": variables, "cells": cells}


def _dv8_reorder(obj: Dict[str, Any], *, sort_key: Callable[[str], Any]) -> Dict[str, Any]:
    variables: List[str] = list(obj.get("variables") or [])
    if not variables:
        return obj

    order = sorted(range(len(variables)), key=lambda i: sort_key(variables[i]))
    old_to_new = {old: new for new, old in enumerate(order)}
    new_vars = [variables[i] for i in order]

    new_cells = []
    for cell in obj.get("cells") or []:
        new_cells.append(
            {
                "src": old_to_new[int(cell["src"])],
                "dest": old_to_new[int(cell["dest"])],
                "values": cell.get("values") or {},
            }
        )
    new_cells.sort(key=lambda c: (c["src"], c["dest"]))

    return {
        "@schemaVersion": obj.get("@schemaVersion", "1.0"),
        "name": obj.get("name", ""),
        "variables": new_vars,
        "cells": new_cells,
    }


def _handcount_var_sort_key(var: str) -> Tuple[int, str, int, str, str]:
    # Keep consistent with NeoDepends `--align-handcount` ordering:
    # package files first, then root files; within file: module, functions, classes, constructors, methods, fields.
    if var.startswith("(External "):
        return (9, var, 9, "", var)

    file_path = var
    if ".py/" in var:
        file_path = var.split(".py/", 1)[0] + ".py"
    elif var.endswith(".py"):
        file_path = var

    file_group = 0 if "/" in file_path else 1  # pkg-first

    if var.endswith("/module (Module)") or var == file_path:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--profile", choices=["strict", "heuristic"], default="strict")
    args = parser.parse_args()

    project_root = args.project_root.expanduser().resolve()
    out_dir = args.out_dir.expanduser().resolve()
    profile = args.profile

    files = _iter_project_py(project_root)
    all_file_names = [p.relative_to(project_root).as_posix() for p in files]
    edges_by_file, all_edges = compute_edges(project_root, files, profile=profile)

    # Write per-file md
    write_md_files(out_dir=out_dir, all_files=all_file_names, edges_by_file=edges_by_file)

    suffix = "" if profile == "strict" else f".{profile}"
    edges_path = out_dir / f"handcount_edges{suffix}.json"
    edges_path.write_text(json.dumps(all_edges, indent=2), encoding="utf-8")

    # DV8 DSMs
    dv8_use = dv8_from_edges(name=f"handcount ({profile}, collapsed Use)", edges=all_edges, collapse_to_use=True)
    dv8_use = _dv8_reorder(dv8_use, sort_key=_handcount_var_sort_key)
    (out_dir / f"handcount_full{suffix}.dv8-dependency.json").write_text(json.dumps(dv8_use, indent=2), encoding="utf-8")

    dv8_kinds = dv8_from_edges(name=f"handcount ({profile}, typed)", edges=all_edges, collapse_to_use=False)
    dv8_kinds = _dv8_reorder(dv8_kinds, sort_key=_handcount_var_sort_key)
    (out_dir / f"handcount_full_typed{suffix}.dv8-dependency.json").write_text(json.dumps(dv8_kinds, indent=2), encoding="utf-8")

    dv8_files = dv8_file_level(name=f"handcount ({profile}, file-level collapsed Use)", edges=all_edges)
    dv8_files = _dv8_reorder(dv8_files, sort_key=_handcount_var_sort_key)
    (out_dir / f"handcount_filelevel{suffix}.dv8-dependency.json").write_text(json.dumps(dv8_files, indent=2), encoding="utf-8")

    print(f"[OK] Wrote md + DV8 DSMs into: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
