# Matrix Full Stack Durdurma Scripti
# ====================================

Write-Host "=====================================" -ForegroundColor Red
Write-Host "Matrix Full Stack Durduruluyor..." -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Red
Write-Host ""

# 1. Node.js process'lerini durdur (Element Web ve Synapse Admin)
Write-Host "1. Frontend'ler durduruluyor..." -ForegroundColor Yellow

$nodePorts = @(8080, 5173)
foreach ($port in $nodePorts) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | 
               Select-Object -ExpandProperty OwningProcess -First 1
    
    if ($process) {
        $processName = Get-Process -Id $process -ErrorAction SilentlyContinue | 
                       Select-Object -ExpandProperty ProcessName
        Write-Host "   Port $port üzerindeki process durduruluyor ($processName - PID: $process)..." -ForegroundColor Yellow
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
        Write-Host "   ✓ Port $port temizlendi!" -ForegroundColor Green
    } else {
        Write-Host "   Port $port zaten boş." -ForegroundColor Gray
    }
}

Write-Host ""

# 2. Docker container'ları durdur
Write-Host "2. Backend durduruluyor..." -ForegroundColor Yellow
cd "C:\Users\Can Cakir\Downloads\www-backup"
docker-compose down

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "✓ Tüm servisler durduruldu!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Tekrar başlatmak için:" -ForegroundColor Cyan
Write-Host "  .\start-all.ps1" -ForegroundColor White
Write-Host ""

