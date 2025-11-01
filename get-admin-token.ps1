# Admin Access Token Al
# ======================

Write-Host "Admin Token Aliniyor..." -ForegroundColor Yellow
Write-Host ""

$username = "@admin:localhost"
$password = "Admin@2024!Guclu"

$body = @{
    type = "m.login.password"
    user = $username
    password = $password
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                   -Method Post `
                                   -Body $body `
                                   -ContentType "application/json"
    
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "ADMIN ACCESS TOKEN:" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host $response.access_token -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Bu token'i kaydet! API cagrilerinde kullanacaksin." -ForegroundColor Yellow
    Write-Host ""
    
    # Dosyaya kaydet
    $response.access_token | Out-File -FilePath "admin-token.txt" -Encoding utf8
    Write-Host "Token 'admin-token.txt' dosyasina kaydedildi." -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "HATA: Token alinamadi!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

