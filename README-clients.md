# Dependency Analyzer

Analyze dependencies between entities (classes, functions, files) in your source code.

## Quick Start

### Interactive Mode

1. **Run the analyzer**:

   **macOS**: If blocked, run `xattr -d com.apple.quarantine ./dependency-analyzer` first

   **Windows**: If you see "Windows protected your PC", click "More info" then "Run anyway"

   **macOS/Linux**:
   ```bash
   ./dependency-analyzer
   ```

   **Windows**:
   ```powershell
   .\dependency-analyzer.exe
   ```

2. **Follow the prompts**:
   - Enter path to your code repository
   - Enter output directory name
   - Choose language: `python` or `java`

3. **View results**:
   - Open `analysis-result.json` in the output directory to view the dependency dsm
   - The `data/` folder contains database files and raw data

### Command Line Mode

For path autocomplete or automation, use command-line arguments:

**macOS/Linux**:
```bash
./dependency-analyzer --input /path/to/repo --output ./results --language python
```

**Windows**:
```powershell
.\dependency-analyzer.exe --input C:\path\to\repo --output .\results --language python
```

Replace `python` with `java` for Java projects.

## Requirements

- Python 3.7+ (must be in PATH)
- Java 11+ (only needed for analyzing Java projects)

## Supported Languages

- Python
- Java

## Output

The tool generates dependency graphs in DV8-compatible JSON format, showing relationships between:
- Files
- Classes
- Methods/Functions
- Fields/Variables
