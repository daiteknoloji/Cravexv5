# ===========================================
# OTOMATIK ADMIN EKLEME - BACKEND BEKLER
# ===========================================
# Backend hazir olana kadar bekler
# ===========================================

param(
    [int]$IntervalSeconds = 60,
    [string]$AdminUser = "@admin:localhost"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OTOMATIK ADMIN EKLEME SERVISI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Admin: $AdminUser" -ForegroundColor Yellow
Write-Host "Kontrol Araligi: $IntervalSeconds saniye" -ForegroundColor Yellow
Write-Host ""

# Backend hazir mi kontrol et
Write-Host "[BASLANGIC] Backend kontrol ediliyor..." -ForegroundColor Gray

$backendReady = $false
$maxRetries = 30
$retryCount = 0

while (-not $backendReady -and $retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8008/health" -UseBasicParsing -ErrorAction Stop -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "              Backend hazir!" -ForegroundColor Green
        }
    } catch {
        $retryCount++
        Write-Host "              Backend bekleniyor... ($retryCount/$maxRetries)" -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
}

if (-not $backendReady) {
    Write-Host ""
    Write-Host "HATA: Backend baslamadi!" -ForegroundColor Red
    Write-Host "Lutfen once backend'i baslat: .\BASLAT.ps1" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host ""

# Admin token al
Write-Host "[BASLANGIC] Admin token aliniyor..." -ForegroundColor Gray

$body = @{
    type = "m.login.password"
    user = $AdminUser
    password = "Admin@2024!Guclu"
} | ConvertTo-Json

$tokenReceived = $false
$tokenRetries = 0

while (-not $tokenReceived -and $tokenRetries -lt 10) {
    try {
        $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                            -Method Post `
                                            -Body $body `
                                            -ContentType "application/json" `
                                            -ErrorAction Stop
        $token = $loginResponse.access_token
        $tokenReceived = $true
        Write-Host "              Token alindi!" -ForegroundColor Green
        Write-Host ""
    } catch {
        $tokenRetries++
        Write-Host "              Token bekleniyor... ($tokenRetries/10)" -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
}

if (-not $tokenReceived) {
    Write-Host ""
    Write-Host "HATA: Token alinamadi!" -ForegroundColor Red
    Write-Host "Admin kullanicisi olusturulmus mu kontrol et." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

$headers = @{
    "Authorization" = "Bearer $token"
}

Write-Host "Servis baslatildi... (Durdurmak icin Ctrl+C)" -ForegroundColor Green
Write-Host ""

# Admin'in üye olduğu odaları takip et
$joinedRooms = @()

# İlk çalıştırmada mevcut odaları al
try {
    $syncResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/sync?timeout=0" `
                                       -Method Get `
                                       -Headers $headers
    
    if ($syncResponse.rooms.join) {
        $joinedRooms = @($syncResponse.rooms.join.PSObject.Properties.Name)
    }
    
    Write-Host "[BASLANGIC] Mevcut $($joinedRooms.Count) odada admin zaten uye" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "UYARI: Baslangic kontrolu basarisiz, devam ediliyor..." -ForegroundColor Yellow
    Write-Host ""
}

# Ana döngü
$iteration = 0
while ($true) {
    $iteration++
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    Write-Host "[$timestamp] Kontrol #$iteration - Yeni odalar aranıyor..." -ForegroundColor Cyan
    
    try {
        # Tüm odaları admin API'den al
        $allRoomsResponse = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms?limit=1000" `
                                               -Method Get `
                                               -Headers $headers
        
        $allRoomIds = @($allRoomsResponse.rooms | ForEach-Object { $_.room_id })
        
        Write-Host "              Toplam oda sayisi: $($allRoomIds.Count)" -ForegroundColor Gray
        
        # Admin'in üye olmadığı odaları bul
        $newRooms = @($allRoomIds | Where-Object { $_ -notin $joinedRooms })
        
        if ($newRooms.Count -gt 0) {
            Write-Host "              YENI ODA BULUNDU: $($newRooms.Count) oda" -ForegroundColor Yellow
            Write-Host ""
            
            foreach ($roomId in $newRooms) {
                try {
                    # Oda bilgilerini al
                    $roomInfo = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms/$roomId" `
                                                   -Method Get `
                                                   -Headers $headers
                    
                    $roomName = $roomInfo.name
                    if (-not $roomName) { $roomName = "(Isimsiz oda)" }
                    
                    Write-Host "              -> Odaya katiliniyor: $roomName" -ForegroundColor White
                    Write-Host "                 ID: $roomId" -ForegroundColor DarkGray
                    
                    # Admin API ile zorla ekle
                    $joinBody = @{
                        user_id = $AdminUser
                    } | ConvertTo-Json
                    
                    $joinResponse = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/join/$roomId" `
                                                       -Method Post `
                                                       -Headers $headers `
                                                       -Body $joinBody `
                                                       -ContentType "application/json"
                    
                    Write-Host "                 [OK] Admin eklendi!" -ForegroundColor Green
                    
                    # Başarılı ise listeye ekle
                    $joinedRooms += $roomId
                    
                } catch {
                    $errorMsg = $_.Exception.Message
                    if ($errorMsg -like "*already*" -or $errorMsg -like "*M_FORBIDDEN*") {
                        Write-Host "                 [INFO] Zaten uye veya erisim yok" -ForegroundColor Gray
                        $joinedRooms += $roomId  # Tekrar denemesin
                    } else {
                        Write-Host "                 [HATA] Eklenemedi: $errorMsg" -ForegroundColor Red
                    }
                }
                
                Write-Host ""
                Start-Sleep -Milliseconds 500  # Rate limit
            }
            
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "Yeni odalara admin ekleme tamamlandi!" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            
        } else {
            Write-Host "              Yeni oda yok" -ForegroundColor Gray
        }
        
    } catch {
        Write-Host "              [HATA] Kontrol basarisiz: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "              Bir sonraki kontrol: $IntervalSeconds saniye sonra..." -ForegroundColor DarkGray
    Write-Host ""
    
    # Bekle
    Start-Sleep -Seconds $IntervalSeconds
}

