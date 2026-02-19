# Build script for compiling Python scripts to standalone binaries using PyInstaller
# Windows PowerShell version

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "NeoDepends Binary Builder" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
try {
    pyinstaller --version | Out-Null
} catch {
    Write-Host "[INFO] PyInstaller not found. Installing..." -ForegroundColor Yellow

    # Try installing with --user flag
    try {
        python -m pip install --user pyinstaller 2>&1 | Out-Null
        Write-Host "[OK] PyInstaller installed successfully" -ForegroundColor Green

        # Add user scripts directory to PATH for this session
        $userScripts = python -c "import site; print(site.USER_SITE.replace('site-packages', 'Scripts'))" 2>$null
        if ($userScripts) {
            $env:PATH = "$userScripts;$env:PATH"
        }
    } catch {
        Write-Host "[ERROR] Failed to install PyInstaller" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install PyInstaller manually using one of these methods:"
        Write-Host "  1. Using pip with --user:"
        Write-Host "     python -m pip install --user pyinstaller"
        Write-Host ""
        Write-Host "  2. Using pipx:"
        Write-Host "     pip install pipx"
        Write-Host "     pipx install pyinstaller"
        Write-Host ""
        exit 1
    }

    # Verify installation
    try {
        pyinstaller --version | Out-Null
    } catch {
        Write-Host "[ERROR] PyInstaller installed but not found in PATH" -ForegroundColor Red
        Write-Host "Please run this script again or restart your terminal"
        exit 1
    }
}

Write-Host "[1/1] Compiling neodepends (all-in-one binary)..." -ForegroundColor Green
Set-Location $PSScriptRoot
pyinstaller --clean --noconfirm neodepends_analyze.spec

Write-Host ""
Write-Host "[2/2] Moving binary to dist directory..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path ..\dist\binaries | Out-Null
Move-Item -Force dist\dependency-analyzer.exe ..\dist\binaries\

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Build complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Binary created:"
Write-Host "  - dist\binaries\dependency-analyzer.exe"
Write-Host ""
Write-Host "This binary bundles:"
Write-Host "  - Interactive dependency analysis tool"
Write-Host "  - Complete neodepends_python_export pipeline"
Write-Host "  - All Python post-processing logic"
Write-Host ""
