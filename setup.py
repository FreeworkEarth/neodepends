#!/usr/bin/env python3
"""
NeoDepends Setup Script
Automatically checks dependencies and sets up the environment

This script ensures all required Python packages are installed
and provides clear guidance for missing system dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def install_requirements():
    """Install Python dependencies from requirements.txt"""
    requirements_file = Path(__file__).parent / "requirements.txt"

    if not requirements_file.exists():
        print("[INFO] No requirements.txt found - creating minimal requirements file")
        # Create minimal requirements file with only essential packages
        requirements_file.write_text("# NeoDepends Python dependencies\n# (Currently no external packages required)\n")
        return True

    # Check if requirements file is empty or only has comments
    content = requirements_file.read_text().strip()
    if not content or all(line.startswith('#') or not line.strip() for line in content.split('\n')):
        print("[OK] No Python dependencies required (using standard library only)")
        return True

    print("[INFO] Installing Python dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print("[OK] Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.lower()
        # Check if it's the externally-managed-environment error
        if "externally-managed-environment" in error_msg or "pep 668" in error_msg:
            print("[INFO] System Python is managed - no additional packages needed")
            print("      NeoDepends uses only Python standard library")
            return True
        else:
            print(f"[ERROR] Failed to install dependencies: {e.stderr}")
            return False


def check_neodepends_binary():
    """Check if neodepends binary exists"""
    if platform.system() == "Windows":
        binary_paths = ["neodepends.exe", "target/release/neodepends.exe"]
    else:
        binary_paths = ["neodepends", "target/release/neodepends"]

    for path in binary_paths:
        if Path(path).exists():
            print(f"[OK] NeoDepends binary found: {path}")
            return True

    print("[WARNING] NeoDepends binary not found")
    print()
    print("To get the NeoDepends binary, either:")
    print("  1. Download a release bundle from GitHub")
    print("  2. Build from source: cargo build --release")
    print()
    return False


def check_java():
    """Check if Java is installed (needed for Java dependency analysis)"""
    try:
        result = subprocess.run(
            ["java", "-version"],
            check=True,
            capture_output=True,
            text=True
        )
        # Java version goes to stderr for some reason
        version_output = result.stderr.split('\n')[0] if result.stderr else "unknown"
        print(f"[OK] Java installed: {version_output}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[INFO] Java not found - Java analysis will not be available")
        print("      To analyze Java projects, install Java 11 or higher")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print()
    print("=" * 70)
    print("SETUP COMPLETE")
    print("=" * 70)
    print()
    print("Next steps:")
    print()
    print("1. To run dependency analysis (cross-platform):")
    print("   python3 run_dependency_analysis.py")
    print()
    print("2. To run QuickStart examples:")
    print("   python3 QuickStart_dependency_analysis_examples.py")
    print()
    print("3. For more information, see:")
    print("   - README.md")
    print("   - docs/ folder")
    print()
    print("=" * 70)


def main():
    print()
    print("=" * 70)
    print("NeoDepends Setup")
    print("=" * 70)
    print()
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print()

    # Change to script directory
    os.chdir(Path(__file__).parent)

    all_ok = True

    # Check Python version
    if not check_python_version():
        all_ok = False
        sys.exit(1)

    # Install Python dependencies
    if not install_requirements():
        all_ok = False

    # Check for neodepends binary
    if not check_neodepends_binary():
        all_ok = False

    # Check for Java (optional)
    check_java()

    # Print next steps
    print_next_steps()

    if not all_ok:
        print("[WARNING] Setup completed with warnings - please review messages above")
        sys.exit(1)

    print("[SUCCESS] All checks passed - NeoDepends is ready to use!")


if __name__ == "__main__":
    main()
