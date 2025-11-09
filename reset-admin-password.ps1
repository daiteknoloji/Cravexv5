# Admin User Password Reset Script (PowerShell)
# Token ile Matrix Admin API kullanarak admin user şifresini reset eder

$token = "syt_Y2FuLmNha2ly_tOszttqeSgHPmXRdEuLC_18awM5"
$synapseUrl = "https://matrix-synapse.up.railway.app"
$adminUserId = "@admin:matrix-synapse.up.railway.app"
$newPassword = "GüçlüBirŞifre123!"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Admin User Password Reset" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Token: $($token.Substring(0, 20))..." -ForegroundColor Yellow
Write-Host "Admin User: $adminUserId" -ForegroundColor Yellow
Write-Host "New Password: $newPassword" -ForegroundColor Yellow
Write-Host ""

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    new_password = $newPassword
    logout_devices = $false
} | ConvertTo-Json

$url = "$synapseUrl/_synapse/admin/v1/reset_password/$adminUserId"

Write-Host "Sending request to: $url" -ForegroundColor Yellow
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ContentType "application/json"
    
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Admin user password has been reset successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Restart Matrix Synapse (Railway Dashboard)" -ForegroundColor White
    Write-Host "2. Test login in Element Web: admin / GüçlüBirŞifre123!" -ForegroundColor White
    
} catch {
    Write-Host "❌ ERROR!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Possible causes:" -ForegroundColor Yellow
    Write-Host "- Token expired or invalid" -ForegroundColor White
    Write-Host "- can.cakir user is not an admin" -ForegroundColor White
    Write-Host "- Matrix Synapse API endpoint not accessible" -ForegroundColor White
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan

