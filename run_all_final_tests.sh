#!/bin/bash
set -euo pipefail

# Bash script to run all final tests for neodepends release
# Usage: 
# cd "/Users/chrisharing/Desktop/RA Software Architecture Analsysis/AGENT/TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/00_NEODEPENDS/neodepends"

# Make script executable
# chmod +x run_all_final_tests.sh

# Run all tests (outputs to FINAL_TESTS_3_DSMV3)
#./run_all_final_tests.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
EXAMPLES_ROOT="/Users/chrisharing/Desktop/RA Software Architecture Analsysis/AGENT/TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/EXAMPLES_CHRIS"
MOVIEPY_ROOT="/Users/chrisharing/Desktop/RA Software Architecture Analsysis/AGENT/TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/Examples/Python Examples/moviepy example/moviepy"
SURVEY_ROOT="/Users/chrisharing/Desktop/RA Software Architecture Analsysis/AGENT/TEST_AUTO/00_CORE/NEODEPENDS_DEICIDE/Examples/Python Examples/survey example/Survey3"
OUTPUT_ROOT="${EXAMPLES_ROOT}/RESULTS/FINAL_TESTS_4_DSMV3"

echo "=== NeoDepends Final Tests ==="
echo "Output directory: ${OUTPUT_ROOT}"
echo ""

# Clean and create output directory
rm -rf "${OUTPUT_ROOT}"
mkdir -p "${OUTPUT_ROOT}"

# Python export common flags (structured hierarchy, handcount-aligned filtering)
PYTHON_FLAGS=(
  --resolver stackgraphs
  --stackgraphs-python-mode ast
  --dv8-hierarchy structured
  --filter-architecture
  --filter-stackgraphs-false-positives
)

echo "=== 1/6: Python Toy First (with utils.py) ==="
python3 tools/neodepends_python_export.py \
  --input "${EXAMPLES_ROOT}/TrainTicketSystem_TOY_PYTHON_FIRST/tts" \
  --output-dir "${OUTPUT_ROOT}/python_toy_first/stackgraphs" \
  "${PYTHON_FLAGS[@]}"
echo "✓ Python Toy First complete"
echo ""

echo "=== 2/6: Python Toy Second ==="
python3 tools/neodepends_python_export.py \
  --input "${EXAMPLES_ROOT}/TrainTicketSystem_TOY_PYTHON_SECOND/tts" \
  --output-dir "${OUTPUT_ROOT}/python_toy_second/stackgraphs" \
  "${PYTHON_FLAGS[@]}"
echo "✓ Python Toy Second complete"
echo ""

echo "=== 3/6: MoviePy (video folder only) ==="
python3 tools/neodepends_python_export.py \
  --input "${MOVIEPY_ROOT}/moviepy/video" \
  --output-dir "${OUTPUT_ROOT}/moviepy_video/stackgraphs" \
  "${PYTHON_FLAGS[@]}"
echo "✓ MoviePy video complete"
echo ""

echo "=== 4/6: Survey3 ==="
python3 tools/neodepends_python_export.py \
  --input "${SURVEY_ROOT}/src" \
  --output-dir "${OUTPUT_ROOT}/survey3/stackgraphs" \
  "${PYTHON_FLAGS[@]}"
echo "✓ Survey3 complete"
echo ""

echo "=== 5/6: Java Toy First (with TicketUtils.java) ==="
mkdir -p "${OUTPUT_ROOT}/java_toy_first/stackgraphs"

./target/release/neodepends \
  --input "${EXAMPLES_ROOT}/TrainTicketSystem_TOY_JAVA_FIRST/src" \
  --output "${OUTPUT_ROOT}/java_toy_first/stackgraphs/dependencies.stackgraphs.db" \
  --format sqlite \
  --resources entities,deps,contents \
  --langs java \
  --depends \
  --depends-jar ./artifacts/depends.jar \
  --force

python3 tools/export_dv8_from_neodepends_db.py \
  --db "${OUTPUT_ROOT}/java_toy_first/stackgraphs/dependencies.stackgraphs.db" \
  --out "${OUTPUT_ROOT}/java_toy_first/stackgraphs/dependencies.stackgraphs.dv8-dsm-v3.json" \
  --name "Java Toy First (depends)"
echo "✓ Java Toy First complete"
echo ""

echo "=== 6/6: Java Toy Second ==="
mkdir -p "${OUTPUT_ROOT}/java_toy_second/stackgraphs"

./target/release/neodepends \
  --input "${EXAMPLES_ROOT}/TrainTicketSystem_TOY_JAVA_SECOND/src" \
  --output "${OUTPUT_ROOT}/java_toy_second/stackgraphs/dependencies.stackgraphs.db" \
  --format sqlite \
  --resources entities,deps,contents \
  --langs java \
  --depends \
  --depends-jar ./artifacts/depends.jar \
  --force

python3 tools/export_dv8_from_neodepends_db.py \
  --db "${OUTPUT_ROOT}/java_toy_second/stackgraphs/dependencies.stackgraphs.db" \
  --out "${OUTPUT_ROOT}/java_toy_second/stackgraphs/dependencies.stackgraphs.dv8-dsm-v3.json" \
  --name "Java Toy Second (depends)"
echo "✓ Java Toy Second complete"
echo ""

echo "=== All tests complete! ==="
echo "Results saved to: ${OUTPUT_ROOT}"
echo ""
echo "Summary:"
find "${OUTPUT_ROOT}" -name "*.dv8-dsm-v3.json" -exec echo "  - {}" \;
