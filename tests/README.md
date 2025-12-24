# NeoDepends Test Suite

Comprehensive test suite for NeoDepends v0.0.15-pyfork that validates all bug fixes from v0.0.14.

## Quick Start

**macOS / Linux:**
```bash
cd /path/to/neodepends
chmod +x tests/run_all_tests.sh
./tests/run_all_tests.sh
```

**Windows:**
```powershell
cd C:\path\to\neodepends
.\tests\run_all_tests.ps1
```

## What Gets Tested

### 1. Unicode Fix ✅
- Verifies `tools/enhance_python_deps.py` has no Unicode arrow characters (`→`)
- Confirms all arrows replaced with ASCII (`->`)

### 2. Auto-Resolver ✅
- Checks both `run_dependency_analysis.sh` and `run_dependency_analysis.ps1`
- Validates auto-selection logic:
  - Python → `stackgraphs`
  - Java → `depends`

### 3. Documentation ✅
- Verifies README includes "Windows Script Requirements" section
- Confirms Git Bash download link present

### 4. Folder Structure ✅
- Runs Python analysis on TOY example
- Validates new output structure:
  ```
  output/
  ├── dependencies.stackgraphs_ast.db              ✅ Root
  ├── dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json  ✅ Root
  └── details/                                      ✅ NEW
      ├── dependencies.stackgraphs_ast.file.dv8-dsm-v3.json
      ├── dv8_deps/
      ├── per_file_dbs/
      ├── raw/ and raw_filtered/
      └── run_summary.json
  ```

### 5. Enhancement Script Output ✅
- Verifies enhancement script uses ASCII arrows in output
- Confirms no Unicode arrows in console output

### 6. QuickStart Examples ✅
- Runs all 4 example projects (2 Python, 2 Java)
- Validates DV8 files created
- Checks `details/` folders present

### 7. JSON Validation ✅
- Validates all generated JSON files are syntactically correct

## Test Output

Test results are saved to `tests/test_output/`:
- `python_test/` - Python analysis output
- `python_test.log` - Python analysis console output
- `quickstart.log` - QuickStart examples console output

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

## CI/CD Integration

These tests can be run in GitHub Actions. See `.github/workflows/test.yml` for the workflow configuration.

## Requirements

- Python 3.x
- `neodepends` binary (either in root or at `target/release/neodepends`)
- For Java tests: Java runtime installed

## Test Coverage

| Test Category | Tests | Description |
|--------------|-------|-------------|
| Unicode Fix | 1 | No `→` in source files |
| Auto-Resolver | 4 | Both scripts have auto-selection for both languages |
| Documentation | 2 | README has Windows requirements section |
| Folder Structure | 9 | Correct file placement in root vs details/ |
| Script Output | 2 | ASCII arrows in console output |
| QuickStart | 6 | All 4 examples run + details/ folders created |
| JSON Validation | 1 | All JSON files valid |
| **TOTAL** | **25** | **Complete coverage of v0.0.15 changes** |

## Notes

- Tests use existing example projects in `examples/`
- QuickStart test overwrites `RESULTS_QuickStart_Examples/`
- Test output in `tests/test_output/` can be deleted after testing
