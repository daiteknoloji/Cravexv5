# =============================================
# ŞİFRELİ ODALARI SİL
# =============================================
# m.room.encryption event'i olan tüm odaları siler
# =============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "  ŞİFRELİ ODALARI SİLME" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Admin token al
Write-Host "[1/3] Admin token aliniyor..." -ForegroundColor Yellow

$body = @{
    type = "m.login.password"
    user = "@admin:localhost"
    password = "Admin@2024!Guclu"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                        -Method Post `
                                        -Body $body `
                                        -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "      Token alindi!" -ForegroundColor Green
} catch {
    Write-Host "      HATA: Token alinamadi!" -ForegroundColor Red
    exit
}

$headers = @{
    "Authorization" = "Bearer $token"
}

Write-Host ""
Write-Host "[2/3] Sifreli odalar bulunuyor..." -ForegroundColor Yellow

# Şifreli odaları bul
$sql = @"
SELECT DISTINCT r.room_id, r.creator, 
    (SELECT COUNT(*) FROM events WHERE room_id = r.room_id AND type = 'm.room.encrypted') as sifreli_mesaj
FROM rooms r
WHERE EXISTS (SELECT 1 FROM events WHERE room_id = r.room_id AND type = 'm.room.encryption');
"@

try {
    $result = docker exec matrix-postgres psql -U synapse_user -d synapse -t -A -c $sql
    
    if (-not $result) {
        Write-Host "      Sifreli oda bulunamadi!" -ForegroundColor Green
        Write-Host ""
        exit
    }
    
    $encryptedRooms = @()
    $totalEncryptedMessages = 0
    
    foreach ($line in $result) {
        if ($line -match '^([^|]+)\|([^|]*)\|(\d+)') {
            $roomId = $matches[1].Trim()
            $creator = $matches[2].Trim()
            $msgCount = [int]$matches[3]
            
            $encryptedRooms += [PSCustomObject]@{
                RoomId = $roomId
                Creator = $creator
                EncryptedMessages = $msgCount
            }
            
            $totalEncryptedMessages += $msgCount
        }
    }
    
    Write-Host "      Bulunan sifreli oda: $($encryptedRooms.Count)" -ForegroundColor Yellow
    Write-Host "      Toplam sifreli mesaj: $totalEncryptedMessages" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "SILINECEK ODALAR:" -ForegroundColor Red
    Write-Host ""
    
    foreach ($room in $encryptedRooms) {
        Write-Host "  - $($room.RoomId)" -ForegroundColor White
        Write-Host "    Olusturan: $($room.Creator)" -ForegroundColor Gray
        Write-Host "    Sifreli mesaj: $($room.EncryptedMessages)" -ForegroundColor Gray
        Write-Host ""
    }
    
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "UYARI: Bu odalar KALICI OLARAK silinecek!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Devam etmek istiyor musun? (EVET/hayir): " -NoNewline -ForegroundColor Yellow
    $confirm = Read-Host
    
    if ($confirm -ne "EVET") {
        Write-Host ""
        Write-Host "Islem iptal edildi." -ForegroundColor Yellow
        Write-Host ""
        exit
    }
    
    Write-Host ""
    Write-Host "[3/3] Odalar siliniyor..." -ForegroundColor Yellow
    Write-Host ""
    
    $successCount = 0
    $failCount = 0
    
    foreach ($room in $encryptedRooms) {
        $roomId = $room.RoomId
        
        Write-Host "  Siliniyor: $roomId" -ForegroundColor Gray
        
        try {
            # Synapse Admin API ile oda silme
            $deleteUrl = "http://localhost:8008/_synapse/admin/v1/rooms/$roomId"
            $deleteBody = @{
                block = $false  # Odayı tamamen sil
                purge = $true   # Veritabanından da temizle
            } | ConvertTo-Json
            
            $response = Invoke-RestMethod -Uri $deleteUrl `
                                           -Method Delete `
                                           -Headers $headers `
                                           -Body $deleteBody `
                                           -ContentType "application/json"
            
            Write-Host "    [OK] Silindi!" -ForegroundColor Green
            $successCount++
            
        } catch {
            Write-Host "    [HATA] Silinemedi: $($_.Exception.Message)" -ForegroundColor Red
            $failCount++
        }
        
        Start-Sleep -Milliseconds 500
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "TAMAMLANDI!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Basarili: $successCount oda" -ForegroundColor Green
    Write-Host "Basarisiz: $failCount oda" -ForegroundColor Red
    Write-Host ""
    Write-Host "Toplam $totalEncryptedMessages sifreli mesaj silindi." -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host "      HATA: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""

