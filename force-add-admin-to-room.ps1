# Admin API ile Zorla Odaya Ekle
# =================================

param(
    [string]$RoomId = "!YmULXuAoAFcYvWeQQG:localhost",
    [string]$UserId = "@admin:localhost"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ADMIN ZORLA ODAYA EKLENIYOR..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Admin token al
$body = @{
    type = "m.login.password"
    user = "@admin:localhost"
    password = "Admin@2024!Guclu"
} | ConvertTo-Json

try {
    Start-Sleep -Seconds 2
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                        -Method Post `
                                        -Body $body `
                                        -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "[1/2] Admin token alindi" -ForegroundColor Green
} catch {
    Write-Host "HATA: Token alinamadi!" -ForegroundColor Red
    exit
}

# Admin API ile zorla ekle
$headers = @{
    "Authorization" = "Bearer $token"
}

try {
    Write-Host "[2/2] Zorla ekleniyor (Admin API)..." -ForegroundColor Yellow
    
    # user_id'yi JSON body'de gönder
    $apiUrl = "http://localhost:8008/_synapse/admin/v1/join/${RoomId}"
    $joinBody = @{
        user_id = $UserId
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri $apiUrl `
                                   -Method Post `
                                   -Headers $headers `
                                   -Body $joinBody `
                                   -ContentType "application/json"
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BASARILI!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Admin odaya eklendi!" -ForegroundColor White
    Write-Host ""
    Write-Host "Simdi yapabilirsin:" -ForegroundColor Cyan
    Write-Host "  1. Element Web'de gir:" -ForegroundColor White
    Write-Host "     http://localhost:8080" -ForegroundColor Gray
    Write-Host "  2. 't1t1' odasini sol tarafta goreceksin" -ForegroundColor White
    Write-Host "  3. Odadaki mesajlari okuyabilirsin!" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "HATA: Eklenemedi!" -ForegroundColor Red
    Write-Host "$($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

