# ========================================
# MATRIX FULL STACK + AUTO ADD ADMIN
# ========================================
# Ana BASLAT.ps1 + Otomatik admin ekleme
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MATRIX + AUTO ADMIN BASLATILIYOR..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "C:\Users\Can Cakir\Desktop\www-backup"

# Ana BASLAT.ps1'i çalıştır
Write-Host "[1/2] Ana servisleri baslatiliyor..." -ForegroundColor Yellow
Write-Host ""

& "$projectPath\BASLAT.ps1"

Write-Host ""
Write-Host "[2/2] Otomatik admin ekleme baslatiliyor..." -ForegroundColor Yellow
Write-Host "   [YENI TERMINAL] Auto-add servisi acilacak..." -ForegroundColor Cyan
Write-Host ""

# Yeni terminal'de Auto-Add scriptini başlat
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$projectPath'; " +
    "Write-Host ''; " +
    "Write-Host '========================================' -ForegroundColor Green; " +
    "Write-Host '  OTOMATIK ADMIN EKLEME SERVISI        ' -ForegroundColor Green; " +
    "Write-Host '========================================' -ForegroundColor Green; " +
    "Write-Host ''; " +
    "Write-Host 'Bu servis her 60 saniyede yeni odalari kontrol eder' -ForegroundColor Yellow; " +
    "Write-Host 've admin kullanicisini otomatik ekler.' -ForegroundColor Yellow; " +
    "Write-Host ''; " +
    "Write-Host 'Durdurmak icin: Ctrl+C' -ForegroundColor Red; " +
    "Write-Host ''; " +
    ".\AUTO-ADD-ADMIN.ps1"
)

Start-Sleep -Seconds 2
Write-Host "   [OK] Auto-add servisi terminal'i acildi" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "TUM SERVISLER BASLATILDI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "CALISANLAR:" -ForegroundColor Cyan
Write-Host "  - Backend (Synapse, PostgreSQL, Redis)" -ForegroundColor White
Write-Host "  - Element Web (Port 8080)" -ForegroundColor White
Write-Host "  - Synapse Admin (Port 5173)" -ForegroundColor White
Write-Host "  - Otomatik Admin Ekleme Servisi" -ForegroundColor White
Write-Host ""
Write-Host "Her yeni oda olusturuldiginda admin otomatik eklenecek!" -ForegroundColor Yellow
Write-Host ""

