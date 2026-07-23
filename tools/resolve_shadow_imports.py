#!/usr/bin/env python3
"""
Resolve stdlib-shadow imports in a NeoDepends database.

Python 3 uses absolute imports by default.  A file inside a package that says
``import logging`` gets the *stdlib* logging, not a project module named
``logging.py`` buried inside the package tree.  StackGraphs (and the enhancer's
``_module_to_file`` helper) cannot tell the difference — they match by name
anywhere in the tree, creating phantom Import edges.

This script walks every File→File Import/ImportLazy edge in the DB, identifies
edges whose target file has a base-module name that shadows a stdlib module,
then checks the *importing* source's AST to decide whether the import was
qualified (genuine project edge — keep) or bare (stdlib — drop).

Usage:
    python3 resolve_shadow_imports.py <db_path> <source_root> [--report shadow_report.json]

Must run AFTER enhancement (edge-schema v2 Import/ImportLazy classification)
and AFTER the false-positive filter.
"""

from __future__ import annotations

import argparse
import ast
import json
import sqlite3
import sys
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# 1. Build stdlib module name set
# ---------------------------------------------------------------------------

def _stdlib_module_names() -> FrozenSet[str]:
    """Return the set of top-level stdlib module names.

    Python ≥3.10 exposes ``sys.stdlib_module_names``.  For older runtimes we
    fall back to a curated list of the most common shadow-conflict names.
    """
    try:
        return frozenset(sys.stdlib_module_names)  # type: ignore[attr-defined]
    except AttributeError:
        # Fallback for Python 3.9 — the most commonly shadowed names.
        return frozenset({
            "abc", "asyncio", "base64", "calendar", "cgi", "cmd", "code",
            "codecs", "collections", "concurrent", "configparser", "contextlib",
            "copy", "csv", "dataclasses", "datetime", "decimal", "difflib",
            "email", "enum", "errno", "faulthandler", "filecmp", "fnmatch",
            "fractions", "functools", "gc", "getpass", "gettext", "glob",
            "gzip", "hashlib", "heapq", "html", "http", "imaplib", "inspect",
            "io", "ipaddress", "itertools", "json", "locale", "logging",
            "mailbox", "math", "mimetypes", "multiprocessing", "numbers",
            "operator", "os", "pathlib", "pickle", "platform", "pprint",
            "profile", "queue", "random", "re", "secrets", "select",
            "shutil", "signal", "smtplib", "socket", "sqlite3", "ssl",
            "statistics", "string", "struct", "subprocess", "sys",
            "tarfile", "tempfile", "textwrap", "threading", "time",
            "timeit", "token", "tokenize", "traceback", "types", "typing",
            "unicodedata", "unittest", "urllib", "uuid", "venv", "warnings",
            "weakref", "xml", "zipfile", "zipimport",
        })


# ---------------------------------------------------------------------------
# 2. Project shadow census
# ---------------------------------------------------------------------------

def _project_shadow_targets(
    file_names: List[str],
    src_root_prefix: Optional[str],
    stdlib_names: FrozenSet[str],
) -> Dict[str, str]:
    """Find project files whose innermost module name shadows a stdlib name.

    Returns ``{file_name: shadowed_stdlib_name}``.

    A file is a shadow candidate if:
    - its innermost module name (filename stem) matches a stdlib module, AND
    - it is NOT a top-level module at the source root (top-level shadows are
      legitimate Python behaviour — the classic beginner-bug scenario).

    For ``careship/logging.py``:  parts = ["careship", "logging"],
    innermost = "logging" (stdlib) → shadow candidate.

    For a flat layout ``logging.py`` at source root:  parts = ["logging"],
    len == 1 → NOT a candidate (real Python shadowing / beginner bug).
    """
    shadows: Dict[str, str] = {}

    for fname in file_names:
        # Strip src-root prefix to get the in-project path.
        rel = fname
        if src_root_prefix and fname.startswith(src_root_prefix):
            rel = fname[len(src_root_prefix):]

        # Skip __init__.py — package inits are resolved differently.
        if rel.endswith("/__init__.py"):
            continue

        # Derive path components as dotted module parts.
        parts = rel.replace("/", ".").removesuffix(".py").split(".")
        if not parts:
            continue

        # Top-level at src-root → only one component (e.g. ``logging.py``
        # directly in the source root).  This is real Python shadowing.
        if len(parts) == 1:
            continue  # legitimate top-level shadow — keep

        # A nested file whose filename matches a stdlib module name.
        # e.g. careship/logging.py → innermost = "logging" → shadow candidate.
        innermost = parts[-1]
        if innermost in stdlib_names:
            shadows[fname] = innermost

    return shadows


# ---------------------------------------------------------------------------
# 3. AST-based import verification
# ---------------------------------------------------------------------------

def _source_has_qualified_import(
    source_code: str,
    target_module_name: str,
    target_file_name: str,
) -> bool:
    """Check whether ``source_code`` imports ``target_module_name`` via a
    qualified or relative path (genuine project edge) rather than a bare
    ``import <name>`` (stdlib).

    Genuine patterns (keep the project edge):
    - ``from careship import logging``           — qualified: package.name
    - ``from careship.logging import setup``      — qualified: package.name.attr
    - ``from . import logging``                   — relative import
    - ``from .logging import setup_logging``       — relative import
    - ``import careship.logging``                 — qualified: dotted path starts with package

    Bare / stdlib patterns (phantom — drop):
    - ``import logging``                          — bare stdlib
    - ``import logging.handlers``                 — stdlib sub-module
    - ``from logging import getLogger``           — bare stdlib
    - ``from logging.handlers import Rotating``   — stdlib sub-module
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return False  # can't parse → conservative: treat as phantom

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # ``import careship.logging`` → genuine (first component != target)
                # ``import logging``          → bare stdlib
                # ``import logging.handlers`` → stdlib sub-module (first == target)
                parts = alias.name.split(".")
                # Genuine iff the dotted path has >1 part AND starts with
                # something other than the shadowed stdlib name.
                if len(parts) > 1 and parts[0] != target_module_name:
                    # e.g. "careship.logging" — first part is "careship", not "logging"
                    if target_module_name in parts[1:]:
                        return True

        elif isinstance(node, ast.ImportFrom):
            level = getattr(node, "level", 0) or 0

            if level > 0:
                # Relative import: ``from . import logging`` or
                # ``from .logging import X`` → genuine project edge.
                module = node.module or ""
                if module == target_module_name or module.endswith(f".{target_module_name}"):
                    return True
                for alias in node.names:
                    if alias.name == target_module_name:
                        return True

            elif node.module:
                # Absolute ``from X import Y``:
                mod_parts = node.module.split(".")

                if mod_parts[0] == target_module_name:
                    # ``from logging import getLogger`` → bare stdlib
                    # ``from logging.handlers import X`` → stdlib sub-module
                    # Both are phantom — the module path starts with the
                    # stdlib name, so Python resolves to stdlib, not project.
                    pass  # not genuine
                else:
                    # ``from careship import logging`` → genuine
                    # ``from careship.logging import setup`` → genuine
                    if target_module_name in mod_parts[1:]:
                        return True
                    for alias in node.names:
                        if alias.name == target_module_name:
                            return True

    return False


# ---------------------------------------------------------------------------
# 4. Main: resolve shadows in the DB
# ---------------------------------------------------------------------------

def resolve_shadow_imports(
    db_path: str,
    source_root: str,
    report_path: Optional[str] = None,
) -> dict:
    """Remove phantom stdlib-shadow Import/ImportLazy edges from the DB.

    Returns a report dict with statistics and per-edge actions.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    stdlib_names = _stdlib_module_names()

    # Load file entities.
    cursor.execute("SELECT id, name, content_id FROM entities WHERE kind = 'File'")
    file_rows = cursor.fetchall()
    file_name_by_id: Dict[bytes, str] = {}
    file_content_id_by_id: Dict[bytes, bytes] = {}
    for fid, fname, cid in file_rows:
        file_name_by_id[fid] = fname
        file_content_id_by_id[fid] = cid

    # Entity names in the DB are package-root-relative (e.g. "careship/logging.py").
    # The shadow census uses path depth (nested vs top-level) to decide candidates,
    # so no src-root prefix stripping is needed.
    src_root_prefix: Optional[str] = None

    # Build shadow census.
    shadow_targets = _project_shadow_targets(
        list(file_name_by_id.values()),
        src_root_prefix,
        stdlib_names,
    )

    if not shadow_targets:
        report = {"shadow_targets": {}, "edges_checked": 0, "edges_dropped": 0, "edges_kept": 0, "actions": []}
        if report_path:
            Path(report_path).parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
        conn.close()
        print("Shadow-import resolver: no shadow targets found.")
        return report

    print(f"Shadow-import resolver: {len(shadow_targets)} shadow target(s) found:")
    for fname, sname in sorted(shadow_targets.items()):
        print(f"  {fname} shadows stdlib '{sname}'")

    # Build reverse lookup: target_file_id → shadowed_stdlib_name.
    shadow_file_ids: Dict[bytes, str] = {}
    for fid, fname in file_name_by_id.items():
        if fname in shadow_targets:
            shadow_file_ids[fid] = shadow_targets[fname]

    # Find all Import/ImportLazy edges targeting shadow files.
    placeholders = ",".join("?" for _ in shadow_file_ids)
    cursor.execute(
        f"""
        SELECT src, tgt, kind, rowid
        FROM deps
        WHERE kind IN ('Import', 'ImportLazy')
          AND tgt IN ({placeholders})
        """,
        list(shadow_file_ids.keys()),
    )
    candidate_edges = cursor.fetchall()

    # Content cache to avoid re-reading.
    content_cache: Dict[bytes, str] = {}

    def _get_content(content_id: bytes) -> str:
        if content_id not in content_cache:
            cursor.execute("SELECT content FROM contents WHERE id = ?", (content_id,))
            row = cursor.fetchone()
            content_cache[content_id] = row[0] if row else ""
        return content_cache[content_id]

    edges_checked = 0
    edges_dropped = 0
    edges_kept = 0
    actions: List[dict] = []
    rowids_to_delete: List[int] = []

    for src_id, tgt_id, dep_kind, rowid in candidate_edges:
        # Only consider File→File edges (entity-level edges are not our concern).
        src_name = file_name_by_id.get(src_id)
        tgt_name = file_name_by_id.get(tgt_id)
        if src_name is None or tgt_name is None:
            continue

        stdlib_name = shadow_file_ids.get(tgt_id)
        if stdlib_name is None:
            continue

        edges_checked += 1

        # Get source file content and check AST.
        src_cid = file_content_id_by_id.get(src_id)
        if src_cid is None:
            # No content → can't verify → conservative: keep
            edges_kept += 1
            actions.append({
                "src": src_name, "tgt": tgt_name, "kind": dep_kind,
                "stdlib": stdlib_name, "action": "keep", "reason": "no source content",
            })
            continue

        source_code = _get_content(src_cid)
        if not source_code.strip():
            edges_kept += 1
            actions.append({
                "src": src_name, "tgt": tgt_name, "kind": dep_kind,
                "stdlib": stdlib_name, "action": "keep", "reason": "empty source",
            })
            continue

        has_qualified = _source_has_qualified_import(source_code, stdlib_name, tgt_name)

        if has_qualified:
            edges_kept += 1
            actions.append({
                "src": src_name, "tgt": tgt_name, "kind": dep_kind,
                "stdlib": stdlib_name, "action": "keep", "reason": "qualified/relative import",
            })
        else:
            edges_dropped += 1
            rowids_to_delete.append(rowid)
            actions.append({
                "src": src_name, "tgt": tgt_name, "kind": dep_kind,
                "stdlib": stdlib_name, "action": "drop", "reason": "bare import (stdlib)",
            })

    # Delete phantom edges.
    if rowids_to_delete:
        for rid in rowids_to_delete:
            cursor.execute("DELETE FROM deps WHERE rowid = ?", (rid,))
        conn.commit()

    conn.close()

    print(f"Shadow-import resolver: checked {edges_checked}, dropped {edges_dropped}, kept {edges_kept}")

    report = {
        "shadow_targets": shadow_targets,
        "edges_checked": edges_checked,
        "edges_dropped": edges_dropped,
        "edges_kept": edges_kept,
        "actions": actions,
    }

    if report_path:
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Shadow report written to {report_path}")

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("db_path", help="Path to the NeoDepends SQLite database")
    ap.add_argument("source_root", help="Source root of the analysed project")
    ap.add_argument(
        "--report",
        default=None,
        help="Path to write shadow_report.json (optional)",
    )
    args = ap.parse_args()

    resolve_shadow_imports(args.db_path, args.source_root, args.report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
