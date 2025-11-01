# Matrix Full Stack Durum Kontrolu
# ==================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Matrix Full Stack Durum Raporu" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Backend Docker Container'lari
Write-Host "BACKEND (Docker):" -ForegroundColor Yellow
Write-Host ""

$containers = @("matrix-synapse", "matrix-postgres", "matrix-redis", "synapse-admin-ui")
foreach ($name in $containers) {
    $status = docker ps --filter "name=$name" --filter "status=running" -q
    if ($status) {
        Write-Host "   [OK] $name" -ForegroundColor Green
    } else {
        Write-Host "   [X]  $name (Stopped)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "FRONTEND (Node.js):" -ForegroundColor Yellow
Write-Host ""

# Element Web
$port8080 = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if ($port8080) {
    Write-Host "   [OK] Element Web (Port 8080)" -ForegroundColor Green
} else {
    Write-Host "   [X]  Element Web (Port 8080)" -ForegroundColor Red
}

# Synapse Admin
$port5173 = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
if ($port5173) {
    Write-Host "   [OK] Synapse Admin (Port 5173)" -ForegroundColor Green
} else {
    Write-Host "   [X]  Synapse Admin (Port 5173)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "ERISIM ADRESLERI:" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Backend API:      http://localhost:8008" -ForegroundColor White
Write-Host "Element Web:      http://localhost:8080" -ForegroundColor White
Write-Host "Synapse Admin:    http://localhost:5173" -ForegroundColor White
Write-Host "Docker Admin:     http://localhost:8082" -ForegroundColor White

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Komutlar:" -ForegroundColor Yellow
Write-Host "  Baslat:   .\start-all.ps1" -ForegroundColor White
Write-Host "  Durdur:   .\stop-all.ps1" -ForegroundColor White
Write-Host "  Durum:    .\status.ps1" -ForegroundColor White
Write-Host ""
