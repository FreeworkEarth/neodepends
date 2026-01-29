# QuickStart script to run NeoDepends on all example projects (PowerShell)
# This script demonstrates how to use NeoDepends on both Python and Java projects
#
# Usage (from neodepends directory):
#   .\QuickStart_dependency_analysis_examples.ps1

$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Output directory
$OutputRoot = Join-Path $ScriptDir "RESULTS_QuickStart_Examples"

Write-Host "=== NeoDepends QuickStart Examples ==="
Write-Host "Output directory: $OutputRoot"
Write-Host ""

# Clean and create output directory
if (Test-Path $OutputRoot) {
    Remove-Item -Recurse -Force $OutputRoot
}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

# Detect if we're in a bundle or source build
if (Test-Path ".\neodepends.exe") {
    $NeodependsBin = ".\neodepends.exe"
} elseif (Test-Path ".\target\release\neodepends.exe") {
    $NeodependsBin = ".\target\release\neodepends.exe"
} else {
    Write-Host "ERROR: neodepends binary not found!" -ForegroundColor Red
    Write-Host "Please either:"
    Write-Host "  - Use a release bundle (neodepends.exe in root directory)"
    Write-Host "  - Build from source: cargo build --release"
    exit 1
}

Write-Host "Using NeoDepends binary: $NeodependsBin"
Write-Host ""

# Resolve Python executable (avoid reliance on py launcher in CI)
$PythonExe = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $PythonExe) {
    Write-Host "ERROR: python not found in PATH." -ForegroundColor Red
    Write-Host "Install Python or ensure actions/setup-python is configured."
    exit 1
}
$PythonExe = $PythonExe.Source

# Resolve toy example paths (multilang preferred)
$ToyRootResolved = $env:TOY_ROOT
if (-not $ToyRootResolved) {
    $Candidates = @(
        (Join-Path $ScriptDir "..\..\..\..\000_TOY_EXAMPLES\ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG"),
        (Join-Path $ScriptDir "..\..\..\000_TOY_EXAMPLES\ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG")
    )
    foreach ($c in $Candidates) {
        if (Test-Path $c) {
            $ToyRootResolved = (Resolve-Path $c).Path
            break
        }
    }
}

if (-not ($ToyRootResolved -and (Test-Path (Join-Path $ToyRootResolved "python\\first_godclass_antipattern")))) {
    $ToyRepoUrl = $env:TOY_REPO_URL
    if (-not $ToyRepoUrl) {
        $ToyRepoUrl = "https://github.com/FreeworkEarth/ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG.git"
    }
    $ToyCloneDir = Join-Path $env:TEMP "neodepends_toy"
    if (Get-Command git -ErrorAction SilentlyContinue) {
        if (Test-Path (Join-Path $ToyCloneDir ".git")) {
            git -C $ToyCloneDir fetch --depth 1 origin main | Out-Null
            git -C $ToyCloneDir reset --hard origin/main | Out-Null
        } else {
            if (Test-Path $ToyCloneDir) { Remove-Item -Recurse -Force $ToyCloneDir }
            git clone --depth 1 --branch main $ToyRepoUrl $ToyCloneDir | Out-Null
        }
    }
    if (Test-Path (Join-Path $ToyCloneDir "python\\first_godclass_antipattern")) {
        $ToyRootResolved = (Resolve-Path $ToyCloneDir).Path
    }
}

if ($ToyRootResolved -and (Test-Path (Join-Path $ToyRootResolved "python\\first_godclass_antipattern"))) {
    Write-Host "Using multilang TOY examples: $ToyRootResolved"
    $PythonToy1 = Join-Path $ToyRootResolved "python\\first_godclass_antipattern"
    $PythonToy2 = Join-Path $ToyRootResolved "python\\second_repository_refactored"
    $JavaToy1 = Join-Path $ToyRootResolved "java\\first_godclass_antipattern"
    $JavaToy2 = Join-Path $ToyRootResolved "java\\second_repository_refactored"
} else {
    $CanonicalRoot = Join-Path $ScriptDir "..\..\..\000_TOY_EXAMPLES\canonical_examples"
    if (Test-Path (Join-Path $CanonicalRoot "python\\first\\tts")) {
        Write-Host "Using canonical TOY examples: $CanonicalRoot"
        $PythonToy1 = Join-Path $CanonicalRoot "python\\first\\tts"
        $PythonToy2 = Join-Path $CanonicalRoot "python\\second\\tts"
        $JavaToy1 = Join-Path $CanonicalRoot "java\\first\\src"
        $JavaToy2 = Join-Path $CanonicalRoot "java\\second\\src"
    } else {
        Write-Host "ERROR: Toy examples not found." -ForegroundColor Red
        Write-Host "Set TOY_ROOT to the multilang repo: ARCH_ANALYSIS_TRAINTICKET_TOY_EXAMPLES_MULTILANG"
        exit 1
    }
}

# ============================================================================
# PYTHON EXAMPLES (using StackGraphs AST resolver)
# ============================================================================

$PythonFlags = @(
    "--resolver", "stackgraphs",
    "--stackgraphs-python-mode", "ast",
    "--dv8-hierarchy", "structured",
    "--filter-architecture",
    "--filter-stackgraphs-false-positives"
)

Write-Host "=== 1/4: Python Example - TrainTicketSystem TOY 1 ==="
& $PythonExe tools\neodepends_python_export.py `
    --neodepends-bin $NeodependsBin `
    --input $PythonToy1 `
    --output-dir "$OutputRoot\python_toy_first" `
    @PythonFlags
if ($LASTEXITCODE -ne 0) { throw "Python TOY 1 failed (neodepends_python_export.py)" }
Write-Host "✓ Python TOY 1 complete"
Write-Host ""

Write-Host "=== 2/4: Python Example - TrainTicketSystem TOY 2 ==="
& $PythonExe tools\neodepends_python_export.py `
    --neodepends-bin $NeodependsBin `
    --input $PythonToy2 `
    --output-dir "$OutputRoot\python_toy_second" `
    @PythonFlags
if ($LASTEXITCODE -ne 0) { throw "Python TOY 2 failed (neodepends_python_export.py)" }
Write-Host "✓ Python TOY 2 complete"
Write-Host ""

# ============================================================================
# JAVA EXAMPLES (using Depends resolver)
# ============================================================================

Write-Host "=== 3/4: Java Example - TrainTicketSystem TOY 1 ==="
New-Item -ItemType Directory -Force -Path "$OutputRoot\java_toy_first" | Out-Null

& $NeodependsBin `
    --input $JavaToy1 `
    --output "$OutputRoot\java_toy_first\dependencies.db" `
    --format sqlite `
    --resources entities,deps,contents `
    --langs java `
    --depends `
    --depends-jar .\artifacts\depends.jar `
    --force

& $PythonExe tools\export_dv8_from_neodepends_db.py `
    --db "$OutputRoot\java_toy_first\dependencies.db" `
    --out "$OutputRoot\java_toy_first\dependencies.dv8-dsm-v3.json" `
    --name "Java TOY 1 (TrainTicketSystem)"
if ($LASTEXITCODE -ne 0) { throw "Java TOY 1 export failed (export_dv8_from_neodepends_db.py)" }

Write-Host "✓ Java TOY 1 complete"
Write-Host ""

Write-Host "=== 4/4: Java Example - TrainTicketSystem TOY 2 ==="
New-Item -ItemType Directory -Force -Path "$OutputRoot\java_toy_second" | Out-Null

& $NeodependsBin `
    --input $JavaToy2 `
    --output "$OutputRoot\java_toy_second\dependencies.db" `
    --format sqlite `
    --resources entities,deps,contents `
    --langs java `
    --depends `
    --depends-jar .\artifacts\depends.jar `
    --force

& $PythonExe tools\export_dv8_from_neodepends_db.py `
    --db "$OutputRoot\java_toy_second\dependencies.db" `
    --out "$OutputRoot\java_toy_second\dependencies.dv8-dsm-v3.json" `
    --name "Java TOY 2 (TrainTicketSystem)"
if ($LASTEXITCODE -ne 0) { throw "Java TOY 2 export failed (export_dv8_from_neodepends_db.py)" }

Write-Host "✓ Java TOY 2 complete"
Write-Host ""

# ============================================================================
# Summary
# ============================================================================

Write-Host "=== QuickStart Complete! ==="
Write-Host ""
Write-Host "Results saved to: $OutputRoot"
Write-Host ""
Write-Host "Python DV8 DSM files (open in DV8 Explorer):"
Write-Host "  - $OutputRoot\python_toy_first\dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json"
Write-Host "  - $OutputRoot\python_toy_second\dependencies.stackgraphs_ast.filtered.dv8-dsm-v3.json"
Write-Host ""
Write-Host "Java DV8 DSM files (open in DV8 Explorer):"
Write-Host "  - $OutputRoot\java_toy_first\dependencies.dv8-dsm-v3.json"
Write-Host "  - $OutputRoot\java_toy_second\dependencies.dv8-dsm-v3.json"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Open any .dv8-dsm-v3.json file in DV8 Explorer for visualization"
Write-Host "  2. See README.md for how to run on your own projects"
Write-Host ""
