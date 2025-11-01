# Belirli Bir Odanin Mesajlarini Al
# ===================================

param(
    [string]$RoomId = "!YmULXuAoAFcYvWeQQG:localhost",
    [string]$Token = ""
)

if ($Token -eq "" -and (Test-Path "admin-token.txt")) {
    $Token = Get-Content "admin-token.txt" -Raw
    $Token = $Token.Trim()
    Write-Host "Token dosyadan okundu." -ForegroundColor Gray
} elseif ($Token -eq "") {
    Write-Host "Token aliniyor..." -ForegroundColor Yellow
    
    # Token al
    $body = @{
        type = "m.login.password"
        user = "@admin:localhost"
        password = "Admin@2024!Guclu"
    } | ConvertTo-Json
    
    try {
        Start-Sleep -Seconds 2  # Rate limit icin bekle
        $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                            -Method Post `
                                            -Body $body `
                                            -ContentType "application/json"
        $Token = $loginResponse.access_token
        Write-Host "Token alindi!" -ForegroundColor Green
    } catch {
        Write-Host "HATA: Token alinamadi!" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ODA MESAJLARI ALINIYOR..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Oda ID: $RoomId" -ForegroundColor Yellow
Write-Host ""

$headers = @{
    "Authorization" = "Bearer $Token"
}

# Oda bilgilerini al
Write-Host "[1/3] Oda bilgileri aliniyor..." -ForegroundColor Yellow
try {
    $roomInfo = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms/$RoomId" `
                                   -Method Get `
                                   -Headers $headers
    
    Write-Host "   Oda Adi: $($roomInfo.name)" -ForegroundColor Green
    Write-Host "   Uye Sayisi: $($roomInfo.joined_members)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "   UYARI: Oda bilgileri alinamadi" -ForegroundColor Yellow
    Write-Host ""
}

# Oda uyelerini al
Write-Host "[2/3] Oda uyeleri aliniyor..." -ForegroundColor Yellow
try {
    $members = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms/$RoomId/members" `
                                  -Method Get `
                                  -Headers $headers
    
    Write-Host "   Uyeler:" -ForegroundColor Green
    foreach ($member in $members.members) {
        Write-Host "     - $member" -ForegroundColor White
    }
    Write-Host ""
} catch {
    Write-Host "   UYARI: Uyeler alinamadi" -ForegroundColor Yellow
    Write-Host ""
}

# Mesajlari al
Write-Host "[3/3] Mesajlar aliniyor..." -ForegroundColor Yellow
try {
    # Admin API v2 endpoint
    $messagesUrl = "http://localhost:8008/_synapse/admin/v2/rooms/$RoomId/messages?limit=100"
    $messagesResponse = Invoke-RestMethod -Uri $messagesUrl `
                                          -Method Get `
                                          -Headers $headers
    
    $messages = $messagesResponse.chunk | Where-Object {$_.type -eq "m.room.message"}
    
    Write-Host "   Toplam $($messages.Count) mesaj bulundu" -ForegroundColor Green
    Write-Host ""
    
    if ($messages.Count -eq 0) {
        Write-Host "Henuz mesaj yok." -ForegroundColor Yellow
    } else {
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "MESAJLAR:" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        
        $messages | Sort-Object origin_server_ts | ForEach-Object {
            $timestamp = [DateTimeOffset]::FromUnixTimeMilliseconds($_.origin_server_ts).LocalDateTime
            $sender = $_.sender
            $body = $_.content.body
            
            Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
            Write-Host "$sender" -ForegroundColor Cyan
            Write-Host "  > $body" -ForegroundColor White
            Write-Host ""
        }
        
        # JSON'a kaydet
        $outputFile = "room_messages_$($RoomId.Replace('!','').Replace(':','_'))_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
        $messages | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding utf8
        
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Mesajlar '$outputFile' dosyasina kaydedildi." -ForegroundColor Green
    }
    
} catch {
    Write-Host "   HATA: Mesajlar alinamadi!" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

