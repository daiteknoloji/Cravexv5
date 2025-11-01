# Matrix Full Stack Baslatma Scripti
# =====================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Matrix Full Stack Baslatiliyor..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Backend'i kontrol et
Write-Host "1. Backend kontrolu yapiliyor..." -ForegroundColor Yellow
$synapseRunning = docker ps --filter "name=matrix-synapse" --filter "status=running" -q
if ($synapseRunning) {
    Write-Host "   OK Backend zaten calisiyor!" -ForegroundColor Green
} else {
    Write-Host "   Backend baslatiliyor..." -ForegroundColor Yellow
    cd "C:\Users\Can Cakir\Desktop\www-backup"
    docker-compose up -d
    Start-Sleep -Seconds 10
    Write-Host "   OK Backend baslatildi!" -ForegroundColor Green
}

Write-Host ""
Write-Host "2. Frontend'ler baslatiliyor..." -ForegroundColor Yellow
Write-Host "   NOT: Iki yeni terminal penceresi acilacak!" -ForegroundColor Cyan
Write-Host ""

# 2. Element Web için yeni terminal aç
Write-Host "   - Element Web baslatiliyor (Port 8080)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Can Cakir\Desktop\www-backup\www\element-web'; Write-Host 'Element Web baslatiliyor...' -ForegroundColor Green; yarn start"

# Biraz bekle
Start-Sleep -Seconds 2

# 3. Synapse Admin için yeni terminal aç
Write-Host "   - Synapse Admin baslatiliyor (Port 5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Can Cakir\Desktop\www-backup\www\admin'; Write-Host 'Synapse Admin baslatiliyor...' -ForegroundColor Green; yarn start"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "OK Tum servisler baslatildi!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Erisim Bilgileri:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:" -ForegroundColor White
Write-Host "   http://localhost:8008" -ForegroundColor Gray
Write-Host ""
Write-Host "Element Web (Mesajlasma):" -ForegroundColor White
Write-Host "   http://localhost:8080" -ForegroundColor Gray
Write-Host "   (30-60 saniye icinde hazir olacak)" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Synapse Admin (Yonetim):" -ForegroundColor White
Write-Host "   http://localhost:5173" -ForegroundColor Gray
Write-Host "   (5-10 saniye icinde hazir olacak)" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Docker Admin Panel:" -ForegroundColor White
Write-Host "   http://localhost:8082" -ForegroundColor Gray
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Giris Bilgileri:" -ForegroundColor Yellow
Write-Host "Username: admin" -ForegroundColor White
Write-Host "Password: Admin@2024!Guclu" -ForegroundColor White
Write-Host "Homeserver: http://localhost:8008" -ForegroundColor White
Write-Host ""
Write-Host "Durdurmak icin terminal pencerelerini kapat!" -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Cyan
