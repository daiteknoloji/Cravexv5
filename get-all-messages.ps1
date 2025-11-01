# Tum Odalarin Mesajlarini Al
# =============================

param(
    [string]$Token = ""
)

if ($Token -eq "" -and (Test-Path "admin-token.txt")) {
    $Token = Get-Content "admin-token.txt"
    Write-Host "Token dosyadan okundu." -ForegroundColor Gray
} elseif ($Token -eq "") {
    Write-Host "HATA: Token bulunamadi!" -ForegroundColor Red
    Write-Host "Kullanim: .\get-all-messages.ps1 -Token 'YOUR_TOKEN'" -ForegroundColor Yellow
    Write-Host "Veya once: .\get-admin-token.ps1" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TUM ODALARIN MESAJLARI ALINIYOR..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$headers = @{
    "Authorization" = "Bearer $Token"
}

# 1. Tum odalari listele
Write-Host "[1/2] Odalar listeleniyor..." -ForegroundColor Yellow
try {
    $roomsResponse = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms" `
                                        -Method Get `
                                        -Headers $headers
    
    $rooms = $roomsResponse.rooms
    Write-Host "   Toplam $($rooms.Count) oda bulundu." -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "   HATA: Odalar alinamadi!" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 2. Her oda icin mesajlari al
Write-Host "[2/2] Mesajlar aliniyor..." -ForegroundColor Yellow
Write-Host ""

$allMessages = @()

foreach ($room in $rooms) {
    $roomId = $room.room_id
    $roomName = if ($room.name) { $room.name } else { $room.canonical_alias }
    if (-not $roomName) { $roomName = $roomId }
    
    Write-Host "   Oda: $roomName" -ForegroundColor Cyan
    Write-Host "   ID: $roomId" -ForegroundColor Gray
    
    try {
        # Odanin event'lerini al
        $eventsUrl = "http://localhost:8008/_synapse/admin/v2/rooms/$roomId/messages"
        $eventsResponse = Invoke-RestMethod -Uri $eventsUrl -Method Get -Headers $headers
        
        $messageCount = $eventsResponse.chunk.Count
        Write-Host "   Mesaj Sayisi: $messageCount" -ForegroundColor Green
        
        # Mesajlari sakla
        foreach ($event in $eventsResponse.chunk) {
            if ($event.type -eq "m.room.message") {
                $allMessages += [PSCustomObject]@{
                    Room = $roomName
                    RoomId = $roomId
                    Sender = $event.sender
                    Body = $event.content.body
                    Timestamp = [DateTimeOffset]::FromUnixTimeMilliseconds($event.origin_server_ts).LocalDateTime
                    EventId = $event.event_id
                }
            }
        }
        
    } catch {
        Write-Host "   UYARI: Mesajlar alinamadi" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

# 3. Sonuclari goster
Write-Host "========================================" -ForegroundColor Green
Write-Host "SONUCLAR:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Toplam Oda: $($rooms.Count)" -ForegroundColor White
Write-Host "Toplam Mesaj: $($allMessages.Count)" -ForegroundColor White
Write-Host ""

# 4. Mesajlari dosyaya kaydet
$outputFile = "all-messages_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$allMessages | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding utf8

Write-Host "Tum mesajlar '$outputFile' dosyasina kaydedildi." -ForegroundColor Green
Write-Host ""

# 5. Son 10 mesaji goster
if ($allMessages.Count -gt 0) {
    Write-Host "Son 10 Mesaj:" -ForegroundColor Yellow
    Write-Host "=============" -ForegroundColor Yellow
    Write-Host ""
    
    $allMessages | Sort-Object Timestamp -Descending | Select-Object -First 10 | ForEach-Object {
        Write-Host "[$($_.Timestamp)] " -NoNewline -ForegroundColor Gray
        Write-Host "$($_.Sender)" -NoNewline -ForegroundColor Cyan
        Write-Host " @ " -NoNewline -ForegroundColor DarkGray
        Write-Host "$($_.Room)" -ForegroundColor Yellow
        Write-Host "  > $($_.Body)" -ForegroundColor White
        Write-Host ""
    }
}

