# ========================================
# SİFRELEMESİZ YENİDEN BAŞLATMA
# ========================================
# Bu script servisleri yeniden başlatır
# Artık E2EE kapalı olacak!
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SİFRELEMESİZ YENİDEN BAŞLATMA       " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Proje dizinine git
$projectPath = "C:\Users\Can Cakir\Desktop\www-backup"
Set-Location $projectPath

Write-Host "[1/4] Mevcut servisleri durduruluyor..." -ForegroundColor Yellow
Write-Host ""

# Backend'i durdur
docker-compose down

Write-Host "   [OK] Docker servisleri durduruldu" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Yeni ayarlarla başlatılıyor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "   NOT: Artık E2EE kapalı!" -ForegroundColor Cyan
Write-Host "   - encryption_enabled_by_default_for_room_type: off" -ForegroundColor Gray
Write-Host "   - force_disable_encryption: true" -ForegroundColor Gray
Write-Host ""

# Backend'i başlat
docker-compose up -d

Write-Host "   [OK] Docker servisleri başlatıldı" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Synapse'in başlaması bekleniyor..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$maxRetries = 10
$retryCount = 0
$healthy = $false

while (-not $healthy -and $retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8008/health" -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $healthy = $true
        }
    } catch {
        Start-Sleep -Seconds 3
        $retryCount++
        Write-Host "   Bekleniyor... ($retryCount/$maxRetries)" -ForegroundColor Gray
    }
}

if ($healthy) {
    Write-Host "   [OK] Synapse hazır!" -ForegroundColor Green
} else {
    Write-Host "   [UYARI] Synapse yavaş başladı, ama devam ediliyor..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] Frontend'leri yeniden başlatmanız gerekiyor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. Element Web terminal'ini KAPAT" -ForegroundColor White
Write-Host "   2. Synapse Admin terminal'ini KAPAT" -ForegroundColor White
Write-Host "   3. .\BASLAT.ps1 ile tekrar başlat" -ForegroundColor Cyan
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  BACKEND YENİDEN BAŞLATILDI!         " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "ÖNEMLİ NOTLAR:" -ForegroundColor Yellow
Write-Host "==============" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. MEVCUT ŞİFRELİ ODALAR:" -ForegroundColor Cyan
Write-Host "     - Eski odalar hala şifreli kalacak" -ForegroundColor White
Write-Host "     - Onları göremezsin (Matrix protokolü gereği)" -ForegroundColor White
Write-Host ""
Write-Host "  2. YENİ ODALAR:" -ForegroundColor Cyan
Write-Host "     - Bundan sonra oluşturulan odalar ŞİFRELENMEYECEK" -ForegroundColor White
Write-Host "     - Admin tüm mesajları görebilecek!" -ForegroundColor Green
Write-Host ""
Write-Host "  3. MEVCUT ODALARI GÖRMEK İÇİN:" -ForegroundColor Cyan
Write-Host "     - .\force-add-admin-to-room.ps1 -RoomId '!odaID:localhost'" -ForegroundColor White
Write-Host "     - Eklendikten SONRA yazılan mesajları görebilirsin" -ForegroundColor White
Write-Host "     - Geçmiş şifreli mesajları ASLA göremezsin" -ForegroundColor Red
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Devam etmek için Frontend'leri başlat: " -NoNewline -ForegroundColor White
Write-Host ".\BASLAT.ps1" -ForegroundColor Green
Write-Host ""




