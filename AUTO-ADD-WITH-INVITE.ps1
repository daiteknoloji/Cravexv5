# ===========================================
# OTOMATIK ADMIN EKLEME - DAVET İLE
# ===========================================
# Public odalar: Direkt join
# Private odalar: Oda sahibine "admin'i davet et" bildirimi gönder
# ===========================================

param(
    [int]$IntervalSeconds = 60,
    [string]$AdminUser = "@admin:localhost"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OTOMATIK ADMIN EKLEME (DAVET İLE)" -ForegroundColor Cyan
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

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                        -Method Post `
                                        -Body $body `
                                        -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "              Token alindi!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "HATA: Token alinamadi!" -ForegroundColor Red
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
                    $creator = $roomInfo.creator
                    
                    Write-Host "              -> Odaya katiliniyor: $roomName" -ForegroundColor White
                    Write-Host "                 ID: $roomId" -ForegroundColor DarkGray
                    Write-Host "                 Olusturan: $creator" -ForegroundColor DarkGray
                    
                    # Önce admin join dene
                    $joinBody = @{
                        user_id = $AdminUser
                    } | ConvertTo-Json
                    
                    $joinUrl = "http://localhost:8008/_synapse/admin/v1/join/${roomId}"
                    
                    try {
                        $joinResponse = Invoke-RestMethod -Uri $joinUrl `
                                                           -Method Post `
                                                           -Headers $headers `
                                                           -Body $joinBody `
                                                           -ContentType "application/json"
                        
                        Write-Host "                 [OK] Admin eklendi!" -ForegroundColor Green
                        $joinedRooms += $roomId
                        
                    } catch {
                        $errorMsg = $_.Exception.Message
                        
                        # 403 = Private oda, davet gerekli
                        if ($errorMsg -like "*403*" -or $errorMsg -like "*Forbidden*") {
                            Write-Host "                 [PRIVATE ODA] Davet gerekli" -ForegroundColor Yellow
                            
                            # Oda yaratıcısına admin adına davet gönder
                            try {
                                # Creator'ın token'ı olmadığı için direkt invite gönderemeyiz
                                # Alternatif: Server notice gönder
                                Write-Host "                 [BİLDİRİM] Oda sahibine mesaj gönderiliyor..." -ForegroundColor Cyan
                                
                                # Server notices için ayrı bir endpoint gerekir
                                # Şimdilik sadece logla
                                Write-Host "                 [TODO] Oda sahibine 'admin@localhost'u davet etmesi için bildirim gönderilecek" -ForegroundColor DarkGray
                                
                                # Atlananları da listeye ekle (tekrar denemesin)
                                $joinedRooms += $roomId
                                
                            } catch {
                                Write-Host "                 [UYARI] Bildirim gonderilemedi" -ForegroundColor Yellow
                                $joinedRooms += $roomId
                            }
                            
                        } elseif ($errorMsg -like "*404*" -or $errorMsg -like "*Not Found*") {
                            Write-Host "                 [ATLA] Oda bulunamadi (silinmis)" -ForegroundColor DarkGray
                            $joinedRooms += $roomId
                            
                        } elseif ($errorMsg -like "*already*") {
                            Write-Host "                 [INFO] Zaten uye" -ForegroundColor Gray
                            $joinedRooms += $roomId
                            
                        } else {
                            Write-Host "                 [HATA] $errorMsg" -ForegroundColor Red
                        }
                    }
                    
                } catch {
                    Write-Host "                 [HATA] Oda bilgisi alinamadi: $($_.Exception.Message)" -ForegroundColor Red
                }
                
                Write-Host ""
                Start-Sleep -Milliseconds 500
            }
            
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "Kontrol tamamlandi!" -ForegroundColor Green
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
    
    Start-Sleep -Seconds $IntervalSeconds
}

