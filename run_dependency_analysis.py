#!/usr/bin/env python3
"""
NeoDepends Dependency Analysis Runner (Python)
Cross-platform dependency analysis tool - works on Windows, macOS, and Linux

This script prompts for inputs and runs the dependency analysis pipeline.
Replaces the Bash and PowerShell scripts for better cross-platform compatibility.
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    # Get script directory to find tools and neodepends binary
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    # Prompt for neodepends binary path (with default)
    default_neodepends = "./neodepends" if sys.platform != "win32" else ".\\neodepends.exe"
    neodepends_bin = input(f"Enter neodepends binary path [default: {default_neodepends}]: ").strip()
    if not neodepends_bin:
        neodepends_bin = default_neodepends

    # Validate neodepends binary exists
    if not Path(neodepends_bin).exists():
        print(f"Error: NeoDepends binary not found at: {neodepends_bin}", file=sys.stderr)
        sys.exit(1)

    # Prompt for input repository
    input_repo = input("Enter input repository path: ").strip()
    if not Path(input_repo).exists():
        print(f"Error: Input repository path does not exist: {input_repo}", file=sys.stderr)
        sys.exit(1)

    # Prompt for output location
    output_dir = input("Enter output directory path: ").strip()
    if not output_dir:
        print("Error: Output directory cannot be empty", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Prompt for language
    language = input("Enter language (python or java): ").strip().lower()
    if language not in ("python", "java"):
        print("Error: Language must be 'python' or 'java'", file=sys.stderr)
        sys.exit(1)

    # Auto-select resolver based on language
    if language == "python":
        model = "stackgraphs"
        print("Auto-selected resolver: stackgraphs (for Python)")
    elif language == "java":
        model = "depends"
        print("Auto-selected resolver: depends (for Java)")
    else:
        print(f"Error: Unsupported language: {language}", file=sys.stderr)
        sys.exit(1)

    # Build the command arguments
    cmd = [
        sys.executable,
        "tools/neodepends_python_export.py",
        "--neodepends-bin", neodepends_bin,
        "--input", input_repo,
        "--output-dir", output_dir,
        "--langs", language,
        "--resolver", model,
        "--dv8-hierarchy", "structured",
        "--filter-architecture"
    ]

    # For Python with stackgraphs, add stackgraphs-specific flags
    if language == "python" and model == "stackgraphs":
        cmd.extend([
            "--stackgraphs-python-mode", "ast",
            "--filter-stackgraphs-false-positives"
        ])

    print()
    print("Running dependency analysis with the following settings:")
    print(f"  NeoDepends binary: {neodepends_bin}")
    print(f"  Input repository: {input_repo}")
    print(f"  Output directory: {output_dir}")
    print(f"  Language: {language}")
    print(f"  Model/Resolver: {model}")
    print()
    print(f"Command: {' '.join(cmd)}")
    print()

    # Execute the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Analysis failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)

    # Determine the output filename based on resolver
    if model == "depends":
        resolver_name = "depends"
    elif model == "stackgraphs" and language == "python":
        resolver_name = "stackgraphs_ast"
    else:
        resolver_name = "stackgraphs"

    output_file = Path(output_dir) / f"dependencies.{resolver_name}.filtered.dv8-dsm-v3.json"

    print()
    print("=" * 80)
    print("Dependency analysis complete!")
    print()
    print(f"Results saved to: {output_dir}")
    print()
    print("To visualize results in DV8 Explorer, open:")
    print(f"  {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
