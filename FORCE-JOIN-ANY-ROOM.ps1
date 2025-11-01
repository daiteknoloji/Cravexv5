# =============================================
# ZORLA HERHANGI BIR ODAYA ADMIN EKLEME
# =============================================
# Oda ayarlarını değiştirip admin'i ekler
# =============================================

param(
    [Parameter(Mandatory=$true)]
    [string]$RoomId,
    [string]$AdminUser = "@admin:localhost"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ZORLA ODA ERISIMI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Oda: $RoomId" -ForegroundColor Yellow
Write-Host "Admin: $AdminUser" -ForegroundColor Yellow
Write-Host ""

# Admin token al
$body = @{
    type = "m.login.password"
    user = $AdminUser
    password = "Admin@2024!Guclu"
} | ConvertTo-Json

try {
    Write-Host "[1/5] Token aliniyor..." -ForegroundColor Gray
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/login" `
                                        -Method Post `
                                        -Body $body `
                                        -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "      OK" -ForegroundColor Green
} catch {
    Write-Host "      HATA: Token alinamadi!" -ForegroundColor Red
    exit
}

$headers = @{
    "Authorization" = "Bearer $token"
}

# Oda bilgilerini al
try {
    Write-Host "[2/5] Oda bilgileri aliniyor..." -ForegroundColor Gray
    $roomInfo = Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms/$RoomId" `
                                   -Method Get `
                                   -Headers $headers
    Write-Host "      Oda: $($roomInfo.name)" -ForegroundColor White
    Write-Host "      Uye sayisi: $($roomInfo.joined_members)" -ForegroundColor White
    Write-Host "      OK" -ForegroundColor Green
} catch {
    Write-Host "      UYARI: Oda bilgisi alinamadi" -ForegroundColor Yellow
}

# Join rules'u public yap (geçici olarak)
try {
    Write-Host "[3/5] Oda ayarlari degistiriliyor (public)..." -ForegroundColor Gray
    
    $stateBody = @{
        join_rule = "public"
    } | ConvertTo-Json
    
    # Admin API kullanarak state event gönder
    $stateUrl = "http://localhost:8008/_matrix/client/r0/rooms/$RoomId/state/m.room.join_rules"
    Invoke-RestMethod -Uri $stateUrl `
                      -Method Put `
                      -Headers $headers `
                      -Body $stateBody `
                      -ContentType "application/json" -ErrorAction SilentlyContinue
    
    Write-Host "      OK" -ForegroundColor Green
    Start-Sleep -Seconds 1
} catch {
    Write-Host "      UYARI: Oda ayari degistirilemedi (devam ediliyor)" -ForegroundColor Yellow
}

# Admin'i ekle
try {
    Write-Host "[4/5] Admin odaya ekleniyor..." -ForegroundColor Gray
    
    # Önce normal join dene
    $joinBody = @{} | ConvertTo-Json
    $joinUrl = "http://localhost:8008/_matrix/client/r0/rooms/$RoomId/join"
    
    try {
        Invoke-RestMethod -Uri $joinUrl `
                         -Method Post `
                         -Headers $headers `
                         -Body $joinBody `
                         -ContentType "application/json"
        Write-Host "      OK - Normal join ile eklendi" -ForegroundColor Green
    } catch {
        # Normal join olmadıysa Admin API kullan
        Write-Host "      Normal join calismadi, Admin API deneniyor..." -ForegroundColor Yellow
        
        # user_id'yi JSON body'de gönder
        $adminJoinUrl = "http://localhost:8008/_synapse/admin/v1/join/${RoomId}"
        $adminJoinBody = @{
            user_id = $AdminUser
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri $adminJoinUrl `
                         -Method Post `
                         -Headers $headers `
                         -Body $adminJoinBody `
                         -ContentType "application/json"
        
        Write-Host "      OK - Admin API ile eklendi" -ForegroundColor Green
    }
    
} catch {
    Write-Host "      HATA: Eklenemedi!" -ForegroundColor Red
    Write-Host "      $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "ALTERNATIF COZUM:" -ForegroundColor Yellow
    Write-Host "1. Element Web'de odaya gir (1k veya 2k kullanicisi ile)" -ForegroundColor White
    Write-Host "2. Oda ayarlari -> Guvenlik -> Admin'i davet et" -ForegroundColor White
    exit
}

# Join rules'u geri al (isteğe bağlı)
try {
    Write-Host "[5/5] Oda ayarlari geri alinsin mi? (E/H): " -NoNewline -ForegroundColor Gray
    $revert = Read-Host
    
    if ($revert -eq "E" -or $revert -eq "e") {
        $stateBody = @{
            join_rule = "invite"
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/rooms/$RoomId/state/m.room.join_rules" `
                         -Method Put `
                         -Headers $headers `
                         -Body $stateBody `
                         -ContentType "application/json"
        
        Write-Host "      Oda tekrar invite-only yapildi" -ForegroundColor Green
    } else {
        Write-Host "      Oda public olarak kaldi" -ForegroundColor Yellow
    }
} catch {
    Write-Host "      UYARI: Ayar geri alinamadi" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BASARILI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Admin odada! Simdi mesajlari okuyabilirsin:" -ForegroundColor White
Write-Host "  Element Web: http://localhost:8080" -ForegroundColor Cyan
Write-Host "  Synapse Admin: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""

