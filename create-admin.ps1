# Matrix Synapse Admin Kullanıcı Oluşturma
# Bu script interaktif, kullanıcı adı ve şifre girmeniz gerekecek

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Matrix Synapse Admin Kullanıcı Oluşturma" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Kullanıcı adı (örn: admin): " -NoNewline -ForegroundColor Yellow
$username = Read-Host

Write-Host "Şifre: " -NoNewline -ForegroundColor Yellow
$password = Read-Host -AsSecureString

Write-Host ""
Write-Host "Admin kullanıcı oluşturuluyor..." -ForegroundColor Green

# Docker exec komutu
docker exec -it matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u $username -p ([System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))) -a

Write-Host ""
Write-Host "İşlem tamamlandı!" -ForegroundColor Green
Write-Host ""
Write-Host "Giriş bilgileri:" -ForegroundColor Cyan
Write-Host "  Homeserver: http://localhost:8008" -ForegroundColor White
Write-Host "  Username: @$username:localhost" -ForegroundColor White
Write-Host "==================================" -ForegroundColor Cyan


