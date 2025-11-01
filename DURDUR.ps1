# ========================================
# MATRIX FULL STACK - DURDURMA
# ========================================
# Bu script tum servisleri durdurur
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "  MATRIX FULL STACK DURDURULUYOR...   " -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

$projectPath = "C:\Users\Can Cakir\Desktop\www-backup"

Write-Host "[1/2] Frontend servisleri durduruluyor..." -ForegroundColor Yellow
Write-Host ""

# Element Web'i durdur (Port 8080)
$elementProcess = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue |
                  Select-Object -ExpandProperty OwningProcess -First 1

if ($elementProcess) {
    Write-Host "   Element Web durduruluyor (Port 8080, PID: $elementProcess)..." -ForegroundColor Gray
    Stop-Process -Id $elementProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Write-Host "   [OK] Element Web durduruldu" -ForegroundColor Green
} else {
    Write-Host "   [INFO] Element Web zaten durmus" -ForegroundColor Gray
}

# Synapse Admin'i durdur (Port 5173)
$adminProcess = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty OwningProcess -First 1

if ($adminProcess) {
    Write-Host "   Synapse Admin durduruluyor (Port 5173, PID: $adminProcess)..." -ForegroundColor Gray
    Stop-Process -Id $adminProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Write-Host "   [OK] Synapse Admin durduruldu" -ForegroundColor Green
} else {
    Write-Host "   [INFO] Synapse Admin zaten durmus" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[2/2] Backend servisleri durduruluyor..." -ForegroundColor Yellow
Write-Host ""

Set-Location $projectPath

Write-Host "   Docker container'lari durduruluyor..." -ForegroundColor Gray
docker-compose down

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  TUM SERVISLER DURDURULDU!           " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Tekrar baslatmak icin:" -ForegroundColor Cyan
Write-Host "  .\BASLAT.ps1" -ForegroundColor White
Write-Host ""

