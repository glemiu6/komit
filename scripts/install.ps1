# scripts/install.ps1
$ErrorActionPreference = "Stop"

$Repo = "glemiu6/komit"
$BinaryName = "komit-windows-x86_64.exe"
$InstallDir = "$env:LOCALAPPDATA\komit"
$BinaryPath = "$InstallDir\komit.exe"

function Get-LatestVersion{
    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -TimeoutSec 5
        if ($response.tag_name) {
            return $response.tag_name.TrimStart("v")
        }
    }catch{}

    try {
        $response = Invoke-RestMethod -Uri "https://pypi.org/pypi/komit/json" -TimeoutSec 5
        return $response.info.version
    }
    catch {
        Write-Host "ERROR: Could not fetch latest version." -ForegroundColor Red
        exit 1
    }

}


function Add-ToPath {
    $currentPath = [Environment]::GetEnvironmentVariable("Path","User")
    if ($currentPath -notlike "*$InstallDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$InstallDir", "User")
        Write-Host "Added $InstallDir to PATH. Please restart your terminal." -ForegroundColor Green
    } else {
        Write-Host "$InstallDir is already in PATH." -ForegroundColor Cyan
    }
    
}

function Install-Komit {
    $version = Get-LatestVersion
    Write-Host "Installing komit v$version..." -ForegroundColor Cyan

    if (-Not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir | Out-Null
        Write-Host "Created installation directory at $InstallDir" -ForegroundColor Green
    }

    $downloadUrl = "https://github.com/$Repo/releases/download/v$version/$BinaryName"
    Write-Host "Downloading from $downloadUrl..."
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $BinaryPath -UseBasicParsing -TimeoutSec 30
    } catch{
        Write-Host "ERROR: Failed to download binary: $_" -ForegroundColor Red
        exit 1
    }

    Add-ToPath
    if (Test-Path $BinaryPath) {
        Write-Host "`nkomit v$version installed successfully!" -ForegroundColor Green
        Write-Host "Run 'komit --help' to get started." -ForegroundColor Cyan
        Write-Host "`nOptional: Set up git alias by running:" -ForegroundColor Yellow
        Write-Host "  git config --global alias.ai '!komit'" -ForegroundColor Cyan
    } else {
        Write-Host "ERROR: Installation failed: $_" -ForegroundColor Red
        exit 1
    }
}

Install-Komit