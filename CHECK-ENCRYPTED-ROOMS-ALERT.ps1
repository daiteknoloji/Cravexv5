# =============================================
# ŞİFRELİ ODA UYARI SİSTEMİ
# =============================================
# Her 5 dakikada şifreli oda oluşturulup oluşturulmadığını kontrol eder
# Oluşturulmuşsa UYARI verir!
# =============================================

param(
    [int]$IntervalSeconds = 300  # 5 dakika
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "  ŞİFRELİ ODA UYARI SİSTEMİ" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Kontrol Araligi: $IntervalSeconds saniye" -ForegroundColor Yellow
Write-Host "Servis baslatildi... (Durdurmak icin Ctrl+C)" -ForegroundColor Green
Write-Host ""

# Son kontrol zamanı
$lastCheckTime = (Get-Date).AddHours(-1)

while ($true) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] Şifreli oda kontrolü yapılıyor..." -ForegroundColor Cyan
    
    # PostgreSQL'den son 5 dakikada oluşturulan şifreli odaları bul
    $sql = @"
SELECT 
    r.room_id,
    r.creator,
    to_timestamp(e.origin_server_ts/1000) as sifreli_acilma_zamani
FROM rooms r
JOIN events e ON r.room_id = e.room_id
WHERE e.type = 'm.room.encryption'
  AND e.origin_server_ts > EXTRACT(EPOCH FROM TIMESTAMP 'now' - INTERVAL '5 minutes') * 1000
ORDER BY e.origin_server_ts DESC;
"@

    try {
        $result = docker exec matrix-postgres psql -U synapse_user -d synapse -t -A -c $sql 2>$null
        
        if ($result) {
            $encryptedRooms = @()
            foreach ($line in $result) {
                if ($line -match '^([^|]+)\|([^|]+)\|(.+)') {
                    $roomId = $matches[1].Trim()
                    $creator = $matches[2].Trim()
                    $time = $matches[3].Trim()
                    
                    $encryptedRooms += [PSCustomObject]@{
                        RoomId = $roomId
                        Creator = $creator
                        Time = $time
                    }
                }
            }
            
            if ($encryptedRooms.Count -gt 0) {
                Write-Host ""
                Write-Host "========================================" -ForegroundColor Red
                Write-Host "  ⚠️  UYARI: ŞİFRELİ ODA BULUNDU! ⚠️" -ForegroundColor Red
                Write-Host "========================================" -ForegroundColor Red
                Write-Host ""
                
                foreach ($room in $encryptedRooms) {
                    Write-Host "Oda ID: $($room.RoomId)" -ForegroundColor Yellow
                    Write-Host "Olusturan: $($room.Creator)" -ForegroundColor Yellow
                    Write-Host "Zaman: $($room.Time)" -ForegroundColor Yellow
                    Write-Host ""
                }
                
                Write-Host "========================================" -ForegroundColor Red
                Write-Host "AKSIYON GEREKLİ:" -ForegroundColor Red
                Write-Host "1. Kullanıcıyı uyarın" -ForegroundColor White
                Write-Host "2. Odayı silin" -ForegroundColor White
                Write-Host "3. Kullanıcıya yeni oda oluşturmasını söyleyin" -ForegroundColor White
                Write-Host "========================================" -ForegroundColor Red
                Write-Host ""
                
                # Sistem bildirimi (Windows)
                Add-Type -AssemblyName System.Windows.Forms
                [System.Windows.Forms.MessageBox]::Show(
                    "ŞİFRELİ ODA OLUŞTURULDU!`n`nKullanıcı: $($encryptedRooms[0].Creator)`n`nHemen kontrol edin!",
                    "⚠️ UYARI",
                    [System.Windows.Forms.MessageBoxButtons]::OK,
                    [System.Windows.Forms.MessageBoxIcon]::Warning
                )
            } else {
                Write-Host "              ✅ Şifreli oda bulunamadı" -ForegroundColor Green
            }
        } else {
            Write-Host "              ✅ Şifreli oda bulunamadı" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "              ❌ Kontrol hatası: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "              Bir sonraki kontrol: $IntervalSeconds saniye sonra..." -ForegroundColor DarkGray
    Write-Host ""
    
    Start-Sleep -Seconds $IntervalSeconds
}

