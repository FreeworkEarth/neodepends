#!/bin/bash
# Build script for compiling Python scripts to standalone binaries using PyInstaller

set -euo pipefail

echo "=========================================="
echo "NeoDepends Binary Builder"
echo "=========================================="
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "[INFO] PyInstaller not found. Installing..."

    # Try installing with --user flag first (handles externally-managed environments)
    if python3 -m pip install --user pyinstaller 2>/dev/null; then
        echo "[OK] PyInstaller installed successfully"
        # Make sure user bin is in PATH
        export PATH="$HOME/.local/bin:$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin:$PATH"
    else
        echo "[ERROR] Failed to install PyInstaller"
        echo ""
        echo "Please install PyInstaller manually using one of these methods:"
        echo "  1. Using pipx (recommended):"
        echo "     brew install pipx"
        echo "     pipx install pyinstaller"
        echo ""
        echo "  2. Using pip with --user:"
        echo "     python3 -m pip install --user pyinstaller"
        echo ""
        echo "  3. Using Homebrew:"
        echo "     brew install pyinstaller"
        echo ""
        exit 1
    fi

    # Verify installation
    if ! command -v pyinstaller &> /dev/null; then
        echo "[ERROR] PyInstaller installed but not found in PATH"
        echo "Please run this script again or add ~/.local/bin to your PATH"
        exit 1
    fi
fi

echo "[1/1] Compiling neodepends (all-in-one binary)..."
cd "$(dirname "$0")"
pyinstaller --clean --noconfirm neodepends_analyze.spec

echo ""
echo "[2/2] Moving binary to dist directory..."
mkdir -p ../dist/binaries/bin
mv dist/dependency-analyzer ../dist/binaries/

# Copy neodepends-core and depends.jar into bin/ so the binary can find them locally
if [ -f "../target/release/neodepends" ]; then
    cp "../target/release/neodepends" "../dist/binaries/bin/neodepends-core"
    chmod +x "../dist/binaries/bin/neodepends-core"
    echo "[OK] Copied neodepends-core to dist/binaries/bin/"
elif [ -f "../target/aarch64-apple-darwin/release/neodepends" ]; then
    cp "../target/aarch64-apple-darwin/release/neodepends" "../dist/binaries/bin/neodepends-core"
    chmod +x "../dist/binaries/bin/neodepends-core"
    echo "[OK] Copied neodepends-core (aarch64) to dist/binaries/bin/"
else
    echo "[WARN] neodepends binary not found — run 'cargo build --release' first"
fi

if [ -f "../artifacts/depends.jar" ]; then
    cp "../artifacts/depends.jar" "../dist/binaries/bin/depends.jar"
    echo "[OK] Copied depends.jar to dist/binaries/bin/"
else
    echo "[WARN] artifacts/depends.jar not found — Java analysis will not work"
fi

echo ""
echo "=========================================="
echo "Build complete!"
echo "=========================================="
echo ""
echo "Binary created:"
echo "  - dist/binaries/dependency-analyzer"
echo ""
echo "This binary bundles:"
echo "  - Interactive dependency analysis tool"
echo "  - Complete neodepends_python_export pipeline"
echo "  - All Python post-processing logic"
echo ""
