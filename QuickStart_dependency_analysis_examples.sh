#!/bin/bash
set -euo pipefail

# QuickStart script to run NeoDepends on all example projects
# This script demonstrates how to use NeoDepends on both Python and Java projects
#
# Usage (from neodepends directory):
#   chmod +x QuickStart_dependency_analysis_examples.sh
#   ./QuickStart_dependency_analysis_examples.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Output directory
OUTPUT_ROOT="${SCRIPT_DIR}/RESULTS_QuickStart_Examples"

echo "=== NeoDepends QuickStart Examples ==="
echo "Output directory: ${OUTPUT_ROOT}"
echo ""

# Clean and create output directory
rm -rf "${OUTPUT_ROOT}"
mkdir -p "${OUTPUT_ROOT}"

# Detect if we're in a bundle or source build
if [ -f "./neodepends" ]; then
    NEODEPENDS_BIN="./neodepends"
elif [ -f "./target/release/neodepends" ]; then
    NEODEPENDS_BIN="./target/release/neodepends"
else
    echo "ERROR: neodepends binary not found!"
    echo "Please either:"
    echo "  - Use a release bundle (neodepends in root directory)"
    echo "  - Build from source: cargo build --release"
    exit 1
fi

echo "Using NeoDepends binary: ${NEODEPENDS_BIN}"
echo ""

# Resolve toy example paths (multilang preferred)
TOY_ROOT_RESOLVED=""
if [ -n "${TOY_ROOT:-}" ] && [ -d "$TOY_ROOT" ]; then
    TOY_ROOT_RESOLVED="$TOY_ROOT"
else
    for candidate in \
        "$SCRIPT_DIR/../../../../000_TOY_EXAMPLES/ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG" \
        "$SCRIPT_DIR/../../../000_TOY_EXAMPLES/ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG"; do
        if [ -d "$candidate" ]; then
            TOY_ROOT_RESOLVED="$candidate"
            break
        fi
    done
fi

if [ -n "$TOY_ROOT_RESOLVED" ] && [ -d "$TOY_ROOT_RESOLVED/python/first_godclass_antipattern" ]; then
    echo "Using multilang TOY examples: $TOY_ROOT_RESOLVED"
    PYTHON_TOY_1="$TOY_ROOT_RESOLVED/python/first_godclass_antipattern"
    PYTHON_TOY_2="$TOY_ROOT_RESOLVED/python/second_repository_refactored"
    JAVA_TOY_1="$TOY_ROOT_RESOLVED/java/first_godclass_antipattern"
    JAVA_TOY_2="$TOY_ROOT_RESOLVED/java/second_repository_refactored"
else
    CANONICAL_ROOT="$SCRIPT_DIR/../../../000_TOY_EXAMPLES/canonical_examples"
    if [ -d "$CANONICAL_ROOT/python/first/tts" ]; then
        echo "Using canonical TOY examples: $CANONICAL_ROOT"
        PYTHON_TOY_1="$CANONICAL_ROOT/python/first/tts"
        PYTHON_TOY_2="$CANONICAL_ROOT/python/second/tts"
        JAVA_TOY_1="$CANONICAL_ROOT/java/first/src"
        JAVA_TOY_2="$CANONICAL_ROOT/java/second/src"
    else
        echo "ERROR: Toy examples not found."
        echo "Set TOY_ROOT to the multilang repo: ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG"
        exit 1
    fi
fi

# ============================================================================
# PYTHON EXAMPLES (using StackGraphs AST resolver)
# ============================================================================

PYTHON_FLAGS=(
    --resolver stackgraphs
    --stackgraphs-python-mode ast
    --dv8-hierarchy structured
    --filter-architecture
    --filter-stackgraphs-false-positives
)

echo "=== 1/4: Python Example - TrainTicketSystem TOY 1 ==="
python3 tools/neodepends_python_export.py \
    --neodepends-bin "${NEODEPENDS_BIN}" \
    --input "${PYTHON_TOY_1}" \
    --output-dir "${OUTPUT_ROOT}/python_toy_first" \
    "${PYTHON_FLAGS[@]}"
echo "✓ Python TOY 1 complete"
echo ""

echo "=== 2/4: Python Example - TrainTicketSystem TOY 2 ==="
python3 tools/neodepends_python_export.py \
    --neodepends-bin "${NEODEPENDS_BIN}" \
    --input "${PYTHON_TOY_2}" \
    --output-dir "${OUTPUT_ROOT}/python_toy_second" \
    "${PYTHON_FLAGS[@]}"
echo "✓ Python TOY 2 complete"
echo ""

# ============================================================================
# JAVA EXAMPLES (using Depends resolver)
# ============================================================================

echo "=== 3/4: Java Example - TrainTicketSystem TOY 1 ==="
mkdir -p "${OUTPUT_ROOT}/java_toy_first"

"${NEODEPENDS_BIN}" \
    --input "${JAVA_TOY_1}" \
    --output "${OUTPUT_ROOT}/java_toy_first/dependencies.db" \
    --format sqlite \
    --resources entities,deps,contents \
    --langs java \
    --depends \
    --depends-jar ./artifacts/depends.jar \
    --force

python3 tools/export_dv8_from_neodepends_db.py \
    --db "${OUTPUT_ROOT}/java_toy_first/dependencies.db" \
    --out "${OUTPUT_ROOT}/java_toy_first/dependencies.dv8-dsm-v3.json" \
    --name "Java TOY 1 (TrainTicketSystem)"

echo "✓ Java TOY 1 complete"
echo ""

echo "=== 4/4: Java Example - TrainTicketSystem TOY 2 ==="
mkdir -p "${OUTPUT_ROOT}/java_toy_second"

"${NEODEPENDS_BIN}" \
    --input "${JAVA_TOY_2}" \
    --output "${OUTPUT_ROOT}/java_toy_second/dependencies.db" \
    --format sqlite \
    --resources entities,deps,contents \
    --langs java \
    --depends \
    --depends-jar ./artifacts/depends.jar \
    --force

python3 tools/export_dv8_from_neodepends_db.py \
    --db "${OUTPUT_ROOT}/java_toy_second/dependencies.db" \
    --out "${OUTPUT_ROOT}/java_toy_second/dependencies.dv8-dsm-v3.json" \
    --name "Java TOY 2 (TrainTicketSystem)"

echo "✓ Java TOY 2 complete"
echo ""

# ============================================================================
# Summary
# ============================================================================

echo "=== QuickStart Complete! ==="
echo ""
echo "Results saved to: ${OUTPUT_ROOT}"
echo ""
echo "Python DV8 DSM files (open in DV8 Explorer):"
echo "  - ${OUTPUT_ROOT}/python_toy_first/dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json"
echo "  - ${OUTPUT_ROOT}/python_toy_second/dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json"
echo ""
echo "Java DV8 DSM files (open in DV8 Explorer):"
echo "  - ${OUTPUT_ROOT}/java_toy_first/dependencies.dv8-dsm-v3.json"
echo "  - ${OUTPUT_ROOT}/java_toy_second/dependencies.dv8-dsm-v3.json"
echo ""
echo "Next steps:"
echo "  1. Open any .dv8-dsm-v3.json file in DV8 Explorer for visualization"
echo "  2. See README.md for how to run on your own projects"
echo ""
