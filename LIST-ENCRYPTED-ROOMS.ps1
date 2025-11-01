# =============================================
# ŞİFRELİ ODALARI LİSTELE VE ANALİZ ET
# =============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ŞİFRELİ ODA ANALİZİ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# PostgreSQL'den şifreli mesajları olan odaları bul
Write-Host "[1/2] Şifreli mesaj içeren odalar bulunuyor..." -ForegroundColor Yellow
Write-Host ""

$sql = @"
SELECT 
    r.room_id,
    r.creator,
    COUNT(CASE WHEN e.type = 'm.room.encrypted' THEN 1 END) as sifreli_mesaj,
    COUNT(CASE WHEN e.type = 'm.room.message' THEN 1 END) as sifresiz_mesaj,
    MAX(e.origin_server_ts) as son_mesaj_ts
FROM rooms r
LEFT JOIN events e ON r.room_id = e.room_id
WHERE e.type IN ('m.room.message', 'm.room.encrypted')
GROUP BY r.room_id, r.creator
HAVING COUNT(CASE WHEN e.type = 'm.room.encrypted' THEN 1 END) > 0
ORDER BY sifreli_mesaj DESC;
"@

$result = docker exec matrix-postgres psql -U synapse_user -d synapse -t -A -c $sql

if (-not $result) {
    Write-Host "SONUC: Şifreli mesaj içeren oda bulunamadı!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tüm mesajlar zaten şifresiz! ✅" -ForegroundColor Green
    exit
}

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  ŞİFRELİ ODA RAPORU" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

$encryptedRooms = @()
$totalEncrypted = 0
$totalUnencrypted = 0

foreach ($line in $result) {
    if ($line -match '^([^|]+)\|([^|]+)\|(\d+)\|(\d+)\|(\d+)') {
        $roomId = $matches[1]
        $creator = $matches[2]
        $encrypted = [int]$matches[3]
        $unencrypted = [int]$matches[4]
        $lastMsg = [int]$matches[5]
        
        $lastDate = [DateTimeOffset]::FromUnixTimeMilliseconds($lastMsg).LocalDateTime
        
        $encryptedRooms += [PSCustomObject]@{
            RoomId = $roomId
            Creator = $creator
            EncryptedCount = $encrypted
            UnencryptedCount = $unencrypted
            LastMessage = $lastDate
        }
        
        $totalEncrypted += $encrypted
        $totalUnencrypted += $unencrypted
    }
}

Write-Host "Toplam şifreli oda sayısı: $($encryptedRooms.Count)" -ForegroundColor Red
Write-Host "Toplam şifreli mesaj: $totalEncrypted" -ForegroundColor Red
Write-Host "Toplam şifresiz mesaj: $totalUnencrypted" -ForegroundColor Green
Write-Host ""

Write-Host "DETAYLAR:" -ForegroundColor Yellow
Write-Host ""

foreach ($room in $encryptedRooms) {
    Write-Host "Oda: $($room.RoomId)" -ForegroundColor White
    Write-Host "  Yaratıcı: $($room.Creator)" -ForegroundColor Gray
    Write-Host "  Şifreli: $($room.EncryptedCount) mesaj" -ForegroundColor Red
    Write-Host "  Şifresiz: $($room.UnencryptedCount) mesaj" -ForegroundColor Green
    Write-Host "  Son mesaj: $($room.LastMessage)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "ÖNERİLER:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Eski şifreli odaları kullanıcılara duyur" -ForegroundColor White
Write-Host "2. Kullanıcılar yeni odalar oluştursun (şifresiz)" -ForegroundColor White
Write-Host "3. Eski odaları arşivle veya sil" -ForegroundColor White
Write-Host ""

Write-Host "UYARI:" -ForegroundColor Red
Write-Host "Şifreli mesajlar decrypt EDİLEMEZ!" -ForegroundColor Red
Write-Host "Odaları silmeden önce kullanıcıları bilgilendir!" -ForegroundColor Yellow
Write-Host ""

