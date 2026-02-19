#!/usr/bin/env python3
"""
NeoDepends Dependency Analysis Runner
Cross-platform dependency analysis tool - works on Windows, macOS, and Linux

This script:
1. Checks for required dependencies (Python, neodepends binary, Java)
2. Prompts for analysis parameters
3. Runs the dependency analysis pipeline

This binary bundles the entire neodepends Python export pipeline internally.
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

# Add tools directory to path so we can import neodepends_python_export
sys.path.insert(0, str(Path(__file__).parent / "tools"))


def print_header():
    """Print welcome header"""
    print()
    print("=" * 70)
    print("NeoDepends - Dependency Analysis Tool")
    print("=" * 70)
    print()
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()


def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("[ERROR] Python 3.7 or higher is required")
        print(f"        Current version: {sys.version}")
        return False
    return True


def find_neodepends_binary():
    """Find the neodepends-core binary in common locations"""
    # When running as a PyInstaller frozen bundle, __file__ points to the temp
    # extraction folder (_MEIxxxxx), not the installed directory. sys.executable
    # always points to the actual dependency-analyzer binary on disk.
    if getattr(sys, "frozen", False):
        script_dir = Path(sys.executable).parent.resolve()
    else:
        script_dir = Path(__file__).parent.resolve()

    if platform.system() == "Windows":
        candidates = [
            script_dir / "bin" / "neodepends-core.exe",  # Release bundle location
            script_dir / "neodepends.exe",  # Flat layout
            script_dir / "target" / "release" / "neodepends.exe",  # Development
            "bin/neodepends-core.exe",
            "neodepends.exe"  # Fallback
        ]
        default = "./bin/neodepends-core.exe"
    else:
        candidates = [
            script_dir / "bin" / "neodepends-core",  # Release bundle location
            script_dir / "neodepends",  # Flat layout
            script_dir / "target" / "release" / "neodepends",  # Development
            "bin/neodepends-core",
            "neodepends"  # Fallback
        ]
        default = "./bin/neodepends-core"

    # Check if any candidate exists
    for candidate in candidates:
        try:
            candidate_path = Path(candidate)
            if candidate_path.exists():
                resolved = candidate_path.resolve()
                return str(resolved), True
        except (OSError, RuntimeError):
            continue

    # Return default as absolute path (may not exist - caller will validate)
    try:
        return str(Path(default).resolve()), False
    except (OSError, RuntimeError):
        return default, False


def remove_macos_quarantine(binary_path):
    """Remove macOS quarantine attribute from binary."""
    if platform.system() != "Darwin":
        return

    try:
        result = subprocess.run(
            ["xattr", "-p", "com.apple.quarantine", binary_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[INFO] Removing macOS quarantine from: {binary_path}")
            remove_result = subprocess.run(
                ["xattr", "-d", "com.apple.quarantine", binary_path],
                capture_output=True, text=True
            )
            if remove_result.returncode == 0:
                print("[OK] Quarantine removed successfully")
            else:
                print("[WARNING] Could not remove quarantine automatically")
                print(f"         Run: xattr -d com.apple.quarantine {binary_path}")
    except (FileNotFoundError, Exception):
        pass


def check_java():
    """Check if Java is installed (needed for Java dependency analysis)"""
    try:
        result = subprocess.run(
            ["java", "-version"],
            check=True, capture_output=True, text=True
        )
        version_output = result.stderr.split('\n')[0] if result.stderr else "unknown"
        return True, version_output
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None


def run_dependency_checks():
    """Run all dependency checks and report status"""
    print("Checking dependencies...")
    print()

    # Check Python version
    if not check_python_version():
        print("[FAILED] Python version check")
        return False
    print("[OK] Python version")

    # Check for neodepends-core binary
    neodepends_path, found = find_neodepends_binary()
    if found:
        print(f"[OK] NeoDepends core binary found: {neodepends_path}")
        remove_macos_quarantine(neodepends_path)
    else:
        print("[ERROR] NeoDepends core binary not found")
        print()
        print("Please ensure the neodepends-core binary is in one of these locations:")
        print("  - bin/neodepends-core")
        print("  - ./target/release/neodepends (development)")
        print()
        return False

    # Check for Java (optional)
    java_available, java_version = check_java()
    if java_available:
        print(f"[OK] Java available: {java_version}")
    else:
        print("[INFO] Java not found - Java dependency analysis will not be available")
        print("       (Only needed if analyzing Java projects)")

    print()
    print("-" * 70)
    print()

    return neodepends_path


def run_analysis(neodepends_bin, input_repo=None, output_dir=None, language=None, binary_path=None):
    """Run the dependency analysis."""
    interactive_mode = (input_repo is None or output_dir is None or language is None)

    original_cwd = Path.cwd()
    script_dir = Path(__file__).parent.resolve()

    print("Dependency Analysis Configuration")
    print()

    if binary_path:
        neodepends_bin = binary_path

    if not Path(neodepends_bin).exists():
        print(f"[ERROR] Binary not found at: {neodepends_bin}")
        return False

    # Use provided input repo or prompt
    if input_repo is None:
        input_repo = input("Enter input repository path: ").strip()
    if not input_repo:
        print("[ERROR] Input repository path cannot be empty")
        return False

    # Resolve input_repo to absolute path (relative to original CWD, not script dir)
    try:
        input_repo_path = Path(input_repo)
        if not input_repo_path.is_absolute():
            input_repo_path = (original_cwd / input_repo_path).resolve()
        else:
            input_repo_path = input_repo_path.resolve()

        if not input_repo_path.exists():
            print(f"[ERROR] Input repository path does not exist: {input_repo_path}")
            return False
        input_repo = str(input_repo_path)
    except (OSError, RuntimeError) as e:
        print(f"[ERROR] Failed to resolve input repository path '{input_repo}': {e}")
        return False

    # Use provided output dir or prompt
    if output_dir is None:
        output_dir = input("Enter output directory path: ").strip()
    if not output_dir:
        print("[ERROR] Output directory cannot be empty")
        return False

    # Resolve output_dir to absolute path (relative to original CWD)
    try:
        output_dir_path = Path(output_dir)
        if not output_dir_path.is_absolute():
            output_dir_path = (original_cwd / output_dir_path).resolve()
        else:
            output_dir_path = output_dir_path.resolve()
        output_dir = str(output_dir_path)
        output_dir_path.mkdir(parents=True, exist_ok=True)
    except (OSError, RuntimeError) as e:
        print(f"[ERROR] Failed to create output directory '{output_dir}': {e}")
        return False

    # Now it's safe to change directory
    os.chdir(script_dir)

    # Use provided language or prompt
    if language is None:
        language = input("Enter language (python or java): ").strip().lower()
    else:
        language = language.lower()
    if language not in ("python", "java"):
        print("[ERROR] Language must be 'python' or 'java'")
        return False

    # Auto-select resolver based on language
    if language == "python":
        model = "stackgraphs"
        print("Auto-selected resolver: stackgraphs (for Python)")
    elif language == "java":
        model = "depends"
        print("Auto-selected resolver: depends (for Java)")

        java_available, _ = check_java()
        if not java_available:
            print()
            print("[ERROR] Java is required for Java dependency analysis")
            print("        Please install Java 11 or higher and try again")
            return False
    else:
        print(f"[ERROR] Unsupported language: {language}")
        return False

    # Build the command arguments for the export pipeline
    export_args = [
        "--neodepends-bin", neodepends_bin,
        "--input", input_repo,
        "--output-dir", output_dir,
        "--langs", language,
        "--resolver", model,
        "--dv8-hierarchy", "structured",
        "--filter-architecture"
    ]

    if language == "python" and model == "stackgraphs":
        export_args.extend([
            "--stackgraphs-python-mode", "ast",
            "--filter-stackgraphs-false-positives"
        ])

    print()
    print("=" * 70)
    print("Running dependency analysis with the following settings:")
    print(f"  NeoDepends binary: {neodepends_bin}")
    print(f"  Input repository: {input_repo}")
    print(f"  Output directory: {output_dir}")
    print(f"  Language: {language}")
    print(f"  Resolver: {model}")
    print("=" * 70)
    print()

    # Import and run the export pipeline directly (bundled in this binary)
    try:
        import neodepends_python_export
        original_argv = sys.argv
        sys.argv = ["neodepends_python_export"] + export_args

        exit_code = neodepends_python_export.main()

        sys.argv = original_argv

        if exit_code != 0:
            print()
            print(f"[ERROR] Analysis failed with exit code {exit_code}")
            return False
    except Exception as e:
        print()
        print(f"[ERROR] Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    output_file = Path(output_dir) / "analysis-result.json"
    data_folder = Path(output_dir) / "data"

    print()
    print("=" * 70)
    print("Dependency analysis complete!")
    print()
    print(f"Results saved to: {output_dir}")
    print()
    print("Main result file:")
    print(f"  {output_file}")
    print()
    print("Database and raw data:")
    print(f"  {data_folder}/")
    print()
    print("To view the results:")
    print("  1. Open DV8 Explorer")
    print("  2. Click 'Open a Matrix'")
    print("  3. Select JSON format")
    print(f"  4. Navigate to and select: {output_file}")
    print("=" * 70)
    print()

    if interactive_mode:
        input("Press Enter to exit...")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="NeoDepends - Dependency Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompts for all inputs)
  %(prog)s

  # Non-interactive mode (for CI/automation)
  %(prog)s --input /path/to/repo --output results --language python

  # Custom binary path
  %(prog)s --binary ./bin/neodepends-core --input ./src --output ./out --language java
        """
    )
    parser.add_argument('--binary', '--bin', dest='binary_path',
                        help='Path to neodepends-core binary (overrides auto-detection)')
    parser.add_argument('--input', '-i', dest='input_repo',
                        help='Input repository path to analyze')
    parser.add_argument('--output', '-o', dest='output_dir',
                        help='Output directory for results')
    parser.add_argument('--language', '-l', dest='language',
                        choices=['python', 'java'],
                        help='Language to analyze (python or java)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress header and non-error output')

    args = parser.parse_args()

    if not args.quiet:
        print_header()

    neodepends_bin = run_dependency_checks()
    if not neodepends_bin:
        print("[FAILED] Dependency checks failed")
        print("Please resolve the issues above and try again")
        sys.exit(1)

    if not args.quiet:
        print("All dependency checks passed!")
        print()

    if not run_analysis(
        neodepends_bin,
        input_repo=args.input_repo,
        output_dir=args.output_dir,
        language=args.language,
        binary_path=args.binary_path
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
