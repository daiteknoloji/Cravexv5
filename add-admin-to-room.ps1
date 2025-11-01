# Admin'i Odaya Ekle
# ====================

param(
    [string]$RoomId = "!YmULXuAoAFcYvWeQQG:localhost",
    [string]$UserId = "@admin:localhost"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ADMIN ODAYA EKLENIYOR..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Oda ID: $RoomId" -ForegroundColor Yellow
Write-Host "Kullanici: $UserId" -ForegroundColor Yellow
Write-Host ""

# Token al
Write-Host "[1/2] Token aliniyor..." -ForegroundColor Yellow

$body = @{
    type = "m.login.password"
    user = $UserId
    password = "Admin@2024!Guclu"
} | ConvertTo-Json

try {
    Start-Sleep -Seconds 2
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                        -Method Post `
                                        -Body $body `
                                        -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "   Token alindi!" -ForegroundColor Green
} catch {
    Write-Host "   HATA: Token alinamadi!" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# Odaya katil
Write-Host ""
Write-Host "[2/2] Odaya katiliniyor..." -ForegroundColor Yellow

$headers = @{
    "Authorization" = "Bearer $token"
}

$joinBody = @{} | ConvertTo-Json

try {
    $joinResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/rooms/$RoomId/join" `
                                       -Method Post `
                                       -Headers $headers `
                                       -Body $joinBody `
                                       -ContentType "application/json"
    
    Write-Host "   OK Admin odaya eklendi!" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BASARILI!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Artik Element Web'de bu odayi gorebilirsin:" -ForegroundColor Cyan
    Write-Host "  http://localhost:8080/#/room/$RoomId" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "   HATA: Odaya eklenemedi!" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    
    if ($_.Exception.Message -like "*already*" -or $_.Exception.Message -like "*M_FORBIDDEN*") {
        Write-Host "   Not: Kullanici zaten bu odanin uyesi olabilir." -ForegroundColor Yellow
        Write-Host "   Veya odaya katilma izni olmayabilir (private oda)." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "   Cozum: Oda sahibi admin'i davet etmeli!" -ForegroundColor Cyan
    }
}

Write-Host ""
