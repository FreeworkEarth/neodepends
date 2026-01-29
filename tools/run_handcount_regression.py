#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Case:
    name: str
    input_path: Path
    lang: str
    handcount: Optional[Path] = None
    normalize_professor: bool = False
    normalize_java: bool = False
    strip_prefixes: Optional[List[str]] = None
    exclude_prefixes: Optional[List[str]] = None
    enforce: bool = False  # fail on diff for this case


def _run(cmd: List[str], *, cwd: Path) -> None:
    print(f"[CMD] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd), check=True)


def _run_neodepends(
    *,
    repo_root: Path,
    neodepends_bin: Path,
    depends_jar: Path,
    out_dir: Path,
    case: Case,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "python3",
        str(repo_root / "tools" / "neodepends_python_export.py"),
        "--neodepends-bin",
        str(neodepends_bin),
        "--input",
        str(case.input_path),
        "--output-dir",
        str(out_dir),
        "--langs",
        case.lang,
        "--dv8-hierarchy",
        "structured",
        "--filter-architecture",
    ]
    if case.lang == "python":
        cmd += ["--resolver", "stackgraphs", "--stackgraphs-python-mode", "ast", "--filter-stackgraphs-false-positives"]
    else:
        cmd += ["--resolver", "depends", "--depends-jar", str(depends_jar)]

    _run(cmd, cwd=repo_root)
    return out_dir / "analysis-result.json"


def _run_compare(
    *,
    repo_root: Path,
    dv8_path: Path,
    handcount: Path,
    out_dir: Path,
    case: Case,
) -> Path:
    diff_json = out_dir / f"{case.name}.diff.json"
    diff_md = out_dir / f"{case.name}.diff.md"
    cmd = [
        "python3",
        str(repo_root / "tools" / "compare_dv8_to_ground_truth.py"),
        "--ground-truth",
        str(handcount),
        "--neodepends-dv8",
        str(dv8_path),
        "--out",
        str(diff_json),
        "--out-md",
        str(diff_md),
    ]
    if case.normalize_professor:
        cmd.append("--normalize-neodepends-professor")
    if case.normalize_java:
        cmd.append("--normalize-java-handcount")
    for p in case.strip_prefixes or []:
        cmd += ["--strip-prefix", p]
    for p in case.exclude_prefixes or []:
        cmd += ["--exclude-prefix", p]

    _run(cmd, cwd=repo_root)
    return diff_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--neodepends-bin", type=Path, default=Path("target/release/neodepends"))
    parser.add_argument("--depends-jar", type=Path, default=Path("artifacts/depends.jar"))
    parser.add_argument("--toy-root", type=Path, default=None, help="Path to toy examples repo (optional)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory for results")
    parser.add_argument(
        "--fail-on-diff",
        action="store_true",
        default=False,
        help="Fail if any compared case has missing/extra edges",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=None,
        help="Fail if (missing+extra)/ground_truth_count exceeds this threshold (e.g. 0.05 for 5%%)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    neodepends_bin = (repo_root / args.neodepends_bin).resolve()
    depends_jar = (repo_root / args.depends_jar).resolve()

    if not neodepends_bin.exists():
        raise SystemExit(f"NeoDepends binary not found: {neodepends_bin}")
    if not depends_jar.exists():
        raise SystemExit(f"depends.jar not found: {depends_jar}")

    if args.output_dir:
        out_base = Path(args.output_dir).expanduser().resolve()
    else:
        out_base = repo_root / "tests" / "test_output" / "handcount_regression"
    out_base.mkdir(parents=True, exist_ok=True)

    exclude_handcount = [
        "DEPS__GROUND_TRUTH_HANDCOUNT/",
        "DEPS_GROUND_TRUTH_HANDCOUNT/",
        "DEPS_GROUND_TRUTH_HANDCOUNTS/",
        "dependencies_files_handcount",
        "dependencies_files_handcount_v1",
        "dependencies_files_handcount_v2",
        "dependencies_files_handcount_v3",
        "src/dependencies_files_handcount",
        "src/dependencies_files_handcount_v1",
    ]

    cases: List[Case] = []

    if args.toy_root:
        toy_root = Path(args.toy_root).expanduser().resolve()
        gt_root = toy_root / "DEPS_GROUND_TRUTH_HANDCOUNT"
        cases.extend(
            [
                Case(
                    name="toy_python_first",
                    input_path=toy_root / "python/first_godclass_antipattern",
                    lang="python",
                    handcount=gt_root
                    / "python/first_godclass_antipattern/DEPS__GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json",
                    normalize_professor=True,
                    enforce=False,
                ),
                Case(
                    name="toy_python_second",
                    input_path=toy_root / "python/second_repository_refactored",
                    lang="python",
                    handcount=gt_root
                    / "python/second_repository_refactored/DEPS__GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json",
                    normalize_professor=True,
                    enforce=False,
                ),
                Case(
                    name="toy_java_first",
                    input_path=toy_root / "java/first_godclass_antipattern",
                    lang="java",
                    handcount=gt_root
                    / "java/first_godclass_antipattern/DEPS__GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json",
                    normalize_java=True,
                    enforce=False,
                ),
                Case(
                    name="toy_java_second",
                    input_path=toy_root / "java/second_repository_refactored",
                    lang="java",
                    handcount=gt_root
                    / "java/second_repository_refactored/DEPS__GROUND_TRUTH_HANDCOUNT/handcount_edges.heuristic.json",
                    normalize_java=True,
                    enforce=False,
                ),
            ]
        )

    cases.extend(
        [
            Case(
                name="survey",
                input_path=repo_root / "examples/examples_testing/Py/survey example/Survey3",
                lang="python",
                handcount=repo_root
                / "examples/examples_testing/Py/DEPS_GROUND_TRUTH_HANDCOUNTS/survey example/dependencies_files_handcount/handcount_edges.heuristic.json",
                normalize_professor=True,
                exclude_prefixes=exclude_handcount,
            ),
            Case(
                name="moviepy",
                input_path=repo_root / "examples/examples_testing/Py/moviepy example/moviepy/moviepy",
                lang="python",
                handcount=repo_root
                / "examples/examples_testing/Py/DEPS_GROUND_TRUTH_HANDCOUNTS/moviepy example/dependencies_files_handcount_v3/handcount_edges.heuristic.json",
                normalize_professor=True,
                strip_prefixes=["moviepy/"],
                exclude_prefixes=exclude_handcount,
            ),
            Case(
                name="large_single_file",
                input_path=repo_root / "examples/Large_Single_File_PYTHON_videoclip",
                lang="python",
                handcount=None,
                normalize_professor=True,
            ),
        ]
    )

    summary = []
    failures = []

    for case in cases:
        print(f"\n=== Running {case.name} ===")
        out_dir = out_base / case.name
        dv8_path = _run_neodepends(
            repo_root=repo_root,
            neodepends_bin=neodepends_bin,
            depends_jar=depends_jar,
            out_dir=out_dir,
            case=case,
        )
        if case.handcount:
            diff_json = _run_compare(
                repo_root=repo_root,
                dv8_path=dv8_path,
                handcount=case.handcount,
                out_dir=out_base,
                case=case,
            )
            diff = json.loads(diff_json.read_text())
            missing = len(diff.get("missing", []))
            extra = len(diff.get("extra", []))
            ground_truth_count = int(diff.get("ground_truth_count", 0) or 0)
            neodepends_count = int(diff.get("neodepends_count", 0) or 0)
            diff_ratio = None
            if ground_truth_count > 0:
                diff_ratio = (missing + extra) / ground_truth_count
            summary.append(
                {
                    "case": case.name,
                    "missing": missing,
                    "extra": extra,
                    "ground_truth_count": ground_truth_count,
                    "neodepends_count": neodepends_count,
                    "diff_ratio": diff_ratio,
                    "diff_json": str(diff_json),
                }
            )
            enforce = case.enforce or args.fail_on_diff
            if enforce and (missing > 0 or extra > 0):
                failures.append(case.name)
            if args.tolerance is not None and diff_ratio is not None and diff_ratio > args.tolerance:
                failures.append(case.name)
        else:
            summary.append({"case": case.name, "missing": None, "extra": None, "diff_json": None})

    summary_path = out_base / "handcount_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\n[OK] Summary: {summary_path}")

    if failures:
        print(f"[FAIL] Differences found in: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
