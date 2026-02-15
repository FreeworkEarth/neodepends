"""
pipeline_errors.py — Centralised error handling for neodepends_python_export.py.

Message design rules
--------------------
User-actionable errors  — things the user can fix themselves (wrong path, missing
                          file, bad flag). Message says exactly what to do next.

Developer errors        — internal failures the user cannot fix (corrupt DB after
                          enhancement, unexpected subprocess output, etc.). Message
                          says "contact the development team" and points to the dev
                          log so the team has what they need to debug.

Function naming
---------------
check_*   Hard abort: raise a typed exception. Caller lets it propagate to the
          top-level handler which prints the message and exits 1.
warn_*    Non-fatal: print to stderr, pipeline continues with degraded output.
safe_*    Never raise: return a result dict (possibly with an 'error' key).
wrap_*    Convert a low-level exception into a typed pipeline exception.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# Typed exceptions
# ---------------------------------------------------------------------------

class PipelineError(RuntimeError):
    """Base class for all pipeline errors. Always has a clean user_message."""

    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


class PreflightError(PipelineError):
    """Raised before any output directories are created."""


class ExecutionError(PipelineError):
    """Raised during subprocess execution (neodepends binary or scripts)."""


class EnhancementError(PipelineError):
    """Raised during the enhancement / filtering stage."""


class ExportError(PipelineError):
    """Raised during the DV8 / per-file DB export stage."""


# ---------------------------------------------------------------------------
# Helpers for composing consistent messages
# ---------------------------------------------------------------------------

_CONTACT = (
    "If this keeps happening, contact the development team and share the dev log\n"
    "       — it contains the full diagnostic output they need."
)

def _user_msg(what: str, how_to_fix: str) -> str:
    """Compose a user-actionable message."""
    return f"{what}\n       {how_to_fix}"

def _dev_msg(what: str, detail: str, dev_log_note: bool = True) -> str:
    """Compose a developer-contact message."""
    lines = [what]
    if detail:
        lines.append(f"       Detail: {detail}")
    if dev_log_note:
        lines.append(f"       {_CONTACT}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Top-level handler — call this from main() around run_one()
# ---------------------------------------------------------------------------

def handle_pipeline_error(exc: BaseException, dev_log_path: Optional[Path] = None) -> int:
    """
    Print a clean error message to stderr and return exit code 1.
    Used as the single top-level except handler.
    """
    if isinstance(exc, PipelineError):
        sys.stderr.write(f"\nError: {exc.user_message}\n")
    elif isinstance(exc, FileNotFoundError):
        sys.stderr.write(f"\nError: {exc}\n")
    elif isinstance(exc, PermissionError):
        sys.stderr.write(f"\nError: {exc}\n")
    else:
        sys.stderr.write(
            f"\nUnexpected error ({type(exc).__name__}): {exc}\n"
            f"       {_CONTACT}\n"
        )

    if dev_log_path is not None:
        sys.stderr.write(f"       Dev log: {dev_log_path}\n")
    sys.stderr.write("\n")
    return 1


# ---------------------------------------------------------------------------
# Stage 1 — Pre-flight checks (run BEFORE output dirs are created)
# ---------------------------------------------------------------------------

def check_binary_executable(binary: Path) -> None:
    """Raise PreflightError if the NeoDepends binary is missing or not executable."""
    if not binary.exists():
        raise PreflightError(
            _dev_msg(
                "The NeoDepends analysis engine could not be found.",
                f"Expected at: {binary}",
            )
        )
    if not os.access(binary, os.X_OK):
        raise PreflightError(
            _dev_msg(
                "The NeoDepends analysis engine exists but cannot be run.",
                f"File: {binary} — missing execute permission.",
            )
        )


def check_langs(langs: Sequence[str], raw_value: str) -> None:
    """Raise PreflightError if langs list is empty."""
    if not langs:
        raise PreflightError(
            _dev_msg(
                "No language was specified for the analysis.",
                f"Language value received: {raw_value!r}",
            )
        )


def check_input_inside_project_root(focus_path: Path, project_root: Path) -> None:
    """Raise PreflightError if focus_path is not under project_root."""
    try:
        focus_path.resolve().relative_to(project_root.resolve())
    except ValueError:
        raise PreflightError(
            _dev_msg(
                "The input repository path is not inside the detected project root.",
                f"Input:        {focus_path.resolve()}\n"
                f"       Project root: {project_root.resolve()}",
            )
        )


def check_enhance_script(enhance_script: Path, langs: Sequence[str], no_enhance: bool) -> None:
    """Raise PreflightError if Python enhancement is needed but the script is missing."""
    if "python" in langs and not no_enhance and not enhance_script.exists():
        raise PreflightError(
            _dev_msg(
                "A required post-processing script for Python analysis is missing.",
                f"Expected at: {enhance_script}",
            )
        )


def check_filter_script(
    filter_script: Path,
    filter_enabled: bool,
    resolver: str,
) -> None:
    """Raise PreflightError if StackGraphs FP filtering is requested but script is missing."""
    if filter_enabled and resolver == "stackgraphs" and not filter_script.exists():
        raise PreflightError(
            _dev_msg(
                "A required post-processing script for Python analysis is missing.",
                f"Expected at: {filter_script}",
            )
        )


def check_output_dir_not_dangling_symlink(output_dir: Path) -> None:
    """Raise PreflightError if --output-dir is a dangling symlink."""
    if output_dir.is_symlink() and not output_dir.exists():
        raise PreflightError(
            _user_msg(
                f"The output directory path cannot be used: {output_dir}",
                "The path exists as a broken link. Choose a different output directory\n"
                "       or delete the broken link at that location and run again.",
            )
        )


def warn_no_source_files(focus_path: Path, langs: Sequence[str]) -> None:
    """Print a warning (no raise) if the input directory appears empty for the given langs."""
    ext_map = {"python": "*.py", "java": "*.java"}
    for lang in langs:
        pattern = ext_map.get(lang)
        if pattern and not any(focus_path.rglob(pattern)):
            sys.stderr.write(
                f"  !!  Warning: no {lang} source files found in the input repository.\n"
                f"       Path checked: {focus_path}\n"
                f"       The analysis will still run but the result will be empty.\n"
                f"       Make sure the input repository path is correct.\n"
            )


# ---------------------------------------------------------------------------
# Stage 2 — NeoDepends binary execution
# ---------------------------------------------------------------------------

def check_db_created(db_path: Path, project_root: Path, resolver: str) -> None:
    """Raise ExecutionError if neodepends exited 0 but wrote no DB file."""
    if not db_path.exists():
        raise ExecutionError(
            _user_msg(
                "The analysis finished without errors but produced no output.",
                "Make sure the input repository contains source files for the selected\n"
                "       language, and that there is enough disk space in the output directory.",
            )
        )


def check_db_non_empty(db_path: Path, focus_prefix: Optional[str], project_root: Path) -> None:
    """Raise ExecutionError if the DB was created but contains 0 entities."""
    try:
        con = sqlite3.connect(f"file:{db_path.resolve()}?immutable=1", uri=True)
        count = con.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        con.close()
    except sqlite3.DatabaseError as exc:
        raise ExecutionError(
            _dev_msg(
                "The output database could not be read after the scan completed.",
                str(exc),
            )
        ) from exc

    if count == 0:
        raise ExecutionError(
            _user_msg(
                "The analysis completed but found no code in the input repository.\n"
                f"       Input scanned: {project_root}",
                "Make sure the input repository path points to the actual source code\n"
                "       and that the selected language matches the files in that directory.",
            )
        )


def wrap_subprocess_error(exc: Exception, step_name: str, script: Optional[Path] = None) -> ExecutionError:
    """Convert a CalledProcessError into a typed ExecutionError with a user-readable message."""
    rc = getattr(exc, "returncode", "?")

    # Scripts the user can fix themselves (config / path issues)
    user_fixable_steps = {
        f"NeoDepends (depends)",
        f"NeoDepends (stackgraphs)",
    }
    if step_name in user_fixable_steps:
        msg = _user_msg(
            "The dependency analysis engine encountered an error.",
            "Check that the input repository path is correct and accessible,\n"
            "       and that the selected language matches the source code in that directory.\n"
            "       The dev log contains the full output for more details.",
        )
    else:
        # Internal scripts — user cannot fix, needs dev support
        detail = f"script: {script}" if script else f"step: {step_name}"
        msg = _dev_msg(
            "An internal processing step failed unexpectedly.",
            detail,
        )
    return ExecutionError(msg)


# ---------------------------------------------------------------------------
# Stage 3 — Enhancement / filtering
# ---------------------------------------------------------------------------

def check_filtered_db_valid(filtered_db: Path, original_db: Path) -> None:
    """Raise EnhancementError if the FP-filter output DB is missing, empty, or corrupt."""
    if not filtered_db.exists() or filtered_db.stat().st_size == 0:
        raise EnhancementError(
            _dev_msg(
                "A post-processing step produced no output database.",
                f"Expected output at: {filtered_db}",
            )
        )
    try:
        con = sqlite3.connect(str(filtered_db))
        con.execute("SELECT count(*) FROM sqlite_master").fetchone()
        con.close()
    except sqlite3.DatabaseError as exc:
        raise EnhancementError(
            _dev_msg(
                "A post-processing step produced a database that cannot be read.",
                f"File: {filtered_db} | SQLite: {exc}",
            )
        ) from exc


def check_db_integrity_after_enhancement(db_path: Path) -> None:
    """Raise EnhancementError if the DB's deps table is inaccessible after enhancement."""
    try:
        con = sqlite3.connect(f"file:{db_path.resolve()}?immutable=1", uri=True)
        con.execute("SELECT count(*) FROM deps").fetchone()
        con.close()
    except sqlite3.DatabaseError as exc:
        raise EnhancementError(
            _dev_msg(
                "The dependency database is not readable after the enhancement step.",
                f"File: {db_path} | SQLite: {exc}",
            )
        ) from exc


def warn_no_enhance(ulog: Any) -> None:
    """Warn user that --no-enhance was set and output will be incomplete."""
    ulog.warn(
        "Running in reduced mode: some dependency types will be missing from the result.\n"
        "       This is a debug setting — contact the development team if you did not\n"
        "       intend to run in this mode."
    )


# ---------------------------------------------------------------------------
# Stage 4 — DV8 export & summary
# ---------------------------------------------------------------------------

def warn_empty_entities(ulog: Any, project_root: Path, focus_prefix: Optional[str]) -> None:
    """Warn user that 0 entities were loaded; all DV8 exports will be empty."""
    ulog.warn(
        "No source code was found in the input repository — result files will be empty.\n"
        f"       Input scanned: {project_root}\n"
        "       Make sure the input repository path is correct and the language\n"
        "       selection matches the source code in that directory."
    )


def check_output_writable(out_path: Path) -> None:
    """Raise ExportError if the output path's parent cannot be created or written to."""
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    except PermissionError as exc:
        raise ExportError(
            _user_msg(
                f"Cannot write results to the output directory: {out_path.parent}",
                "Check that you have permission to write to that location,\n"
                "       or choose a different output directory and run again.",
            )
        ) from exc


def safe_summarize_db(db_path: Path) -> Dict[str, Any]:
    """
    Return the DB summary dict, or a dict with an 'error' key if the DB is
    unavailable. Never raises — a summary failure should not abort a completed run.
    """
    if not db_path.exists():
        return {"error": f"DB not found: {db_path}"}
    try:
        con = sqlite3.connect(f"file:{db_path.resolve()}?immutable=1", uri=True)
        cur = con.cursor()
        entities_total = cur.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        deps_total = cur.execute("SELECT COUNT(*) FROM deps").fetchone()[0]

        kind_counts: Dict[str, int] = {}
        for (kind,) in cur.execute("SELECT DISTINCT kind FROM entities").fetchall():
            kind_counts[kind] = cur.execute(
                "SELECT COUNT(*) FROM entities WHERE kind = ?", (kind,)
            ).fetchone()[0]

        deps_by_kind: Dict[str, int] = {}
        for row in cur.execute("SELECT kind, COUNT(*) FROM deps GROUP BY kind").fetchall():
            deps_by_kind[row[0]] = row[1]

        breakdown: List[Dict[str, Any]] = []
        for row in cur.execute(
            "SELECT e1.kind, e2.kind, d.kind, COUNT(*) "
            "FROM deps d "
            "JOIN entities e1 ON e1.id = d.src "
            "JOIN entities e2 ON e2.id = d.tgt "
            "GROUP BY e1.kind, e2.kind, d.kind"
        ).fetchall():
            breakdown.append(
                {"src_kind": row[0], "tgt_kind": row[1], "dep_kind": row[2], "count": row[3]}
            )
        con.close()
        return {
            "entities_total": entities_total,
            "deps_total": deps_total,
            "files_total": kind_counts.get("File", 0),
            "classes_total": kind_counts.get("Class", 0),
            "methods_total": kind_counts.get("Method", 0),
            "fields_total": kind_counts.get("Field", 0),
            "deps_by_kind": deps_by_kind,
            "breakdown": breakdown,
        }
    except sqlite3.DatabaseError as exc:
        return {"error": f"Could not query DB: {exc}"}


def safe_summarize_dv8_dir(dv8_dir: Path) -> Dict[str, Any]:
    """
    Return the DV8 directory summary. Skips unreadable / malformed files rather
    than crashing. Never raises.
    """
    totals: Dict[str, int] = {}
    per_file: Dict[str, Dict[str, int]] = {}

    if not dv8_dir.exists():
        return {"totals": totals, "per_file": per_file}

    parse_errors = 0
    for path in sorted(dv8_dir.glob("*.dv8-dependency.json")):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            parse_errors += 1
            continue
        file_counts: Dict[str, int] = {}
        for cell in obj.get("cells", []):
            for kind, val in cell.get("values", {}).items():
                totals[kind] = totals.get(kind, 0) + int(val)
                file_counts[kind] = file_counts.get(kind, 0) + int(val)
        per_file[path.name] = file_counts

    result: Dict[str, Any] = {"totals": totals, "per_file": per_file}
    if parse_errors:
        result["parse_errors"] = parse_errors
    return result
