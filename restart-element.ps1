# Element Web'i Yeniden Baslat
# ===============================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Element Web Yeniden Baslatiliyor..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Port 8080'i durdur
Write-Host "1. Mevcut Element Web durduruluyor..." -ForegroundColor Yellow
$process = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | 
           Select-Object -ExpandProperty OwningProcess -First 1

if ($process) {
    Write-Host "   Port 8080 temizleniyor (PID: $process)..." -ForegroundColor Yellow
    Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "   OK Durduruldu!" -ForegroundColor Green
} else {
    Write-Host "   Zaten durmus." -ForegroundColor Gray
}

Write-Host ""
Write-Host "2. Element Web yeniden baslatiliyor..." -ForegroundColor Yellow
Write-Host "   Yeni terminal penceresi acilacak!" -ForegroundColor Cyan
Write-Host ""

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Can Cakir\Downloads\www-backup\www\element-web'; Write-Host 'Element Web config.json ile baslatiliyor...' -ForegroundColor Green; yarn start"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "OK Element Web baslatildi!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Tarayicida ac (30 saniye bekle):" -ForegroundColor Cyan
Write-Host "  http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "Giris bilgileri:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: Admin@2024!Guclu" -ForegroundColor White
Write-Host "  Homeserver: Otomatik yuklendi (localhost:8008)" -ForegroundColor White
Write-Host ""

