#!/bin/bash

# NeoDepends Release Script
# Creates complete release bundles for macOS and Windows

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Error: Version number required"
    echo "Usage: ./release.sh v0.0.14"
    exit 1
fi

# Check required files exist
echo "Checking required files..."
REQUIRED_FILES="setup.py README.md REQUIREMENTS.txt run_dependency_analysis.sh run_dependency_analysis.ps1 run_dependency_analysis.py QuickStart_dependency_analysis_examples.sh QuickStart_dependency_analysis_examples.ps1"

for file in $REQUIRED_FILES; do
    if [ ! -f "$file" ]; then
        echo "Error: Required file '$file' not found"
        exit 1
    fi
done

echo "✓ All required files found"

echo "Building NeoDepends $VERSION..."

# Clean and build binaries
cargo clean
cargo build --release --target aarch64-apple-darwin
cargo build --release --target x86_64-pc-windows-gnu

# Create release directory
rm -rf release
mkdir -p release

# Create temporary staging directories
MACOS_STAGING="release/neodepends-$VERSION-aarch64-macos"
WINDOWS_STAGING="release/neodepends-$VERSION-x86_64-win"

mkdir -p "$MACOS_STAGING"
mkdir -p "$WINDOWS_STAGING"

echo "Packaging macOS release..."

# macOS release
cp target/aarch64-apple-darwin/release/neodepends "$MACOS_STAGING/"
cp artifacts/depends.jar "$MACOS_STAGING/"
cp -r tools "$MACOS_STAGING/"
cp -r examples "$MACOS_STAGING/"
cp run_dependency_analysis.sh "$MACOS_STAGING/"
cp run_dependency_analysis.py "$MACOS_STAGING/"
cp QuickStart_dependency_analysis_examples.sh "$MACOS_STAGING/"
cp README.md "$MACOS_STAGING/"
cp REQUIREMENTS.txt "$MACOS_STAGING/"
cp setup.py "$MACOS_STAGING/"

# Create macOS zip
cd release
zip -r "neodepends-$VERSION-aarch64-macos.zip" "neodepends-$VERSION-aarch64-macos"
cd ..

echo "Packaging Windows release..."

# Windows release
cp target/x86_64-pc-windows-gnu/release/neodepends.exe "$WINDOWS_STAGING/"
cp artifacts/depends.jar "$WINDOWS_STAGING/"
cp -r tools "$WINDOWS_STAGING/"
cp -r examples "$WINDOWS_STAGING/"
cp run_dependency_analysis.ps1 "$WINDOWS_STAGING/"
cp run_dependency_analysis.py "$WINDOWS_STAGING/"
cp QuickStart_dependency_analysis_examples.ps1 "$WINDOWS_STAGING/"
cp README.md "$WINDOWS_STAGING/"
cp REQUIREMENTS.txt "$WINDOWS_STAGING/"
cp setup.py "$WINDOWS_STAGING/"

# Create Windows zip
cd release
zip -r "neodepends-$VERSION-x86_64-win.zip" "neodepends-$VERSION-x86_64-win"
cd ..

# Clean up staging directories
rm -rf "$MACOS_STAGING"
rm -rf "$WINDOWS_STAGING"

echo ""
echo "✓ Release bundles created:"
echo "  - release/neodepends-$VERSION-aarch64-macos.zip"
echo "  - release/neodepends-$VERSION-x86_64-win.zip"
echo ""
echo "Release contents:"
echo "  ✓ Binary (neodepends / neodepends.exe)"
echo "  ✓ depends.jar"
echo "  ✓ Python tools (13 files)"
echo "  ✓ Interactive scripts (.sh / .ps1)"
echo "  ✓ QuickStart scripts"
echo "  ✓ README.md"
echo "  ✓ REQUIREMENTS.txt"
echo "  ✓ setup.py"
echo "  ✓ Examples"
