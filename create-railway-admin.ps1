# Create Admin User on Railway Synapse

$username = "admin"
$password = "Admin@2024!Guclu"
$synapseUrl = "https://matrix-synapse.up.railway.app"
$sharedSecret = "CHANGE_THIS_TO_RANDOM_STRING"

Write-Host ""
Write-Host "Creating ADMIN user on Railway Synapse..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Get nonce
Write-Host "Step 1: Getting nonce..." -ForegroundColor Yellow
$nonceUrl = "$synapseUrl/_synapse/admin/v1/register"

try {
    $nonceResponse = Invoke-RestMethod -Uri $nonceUrl -Method GET
    $nonce = $nonceResponse.nonce
    Write-Host "Nonce received: $nonce" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Could not get nonce" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

# Step 2: Calculate HMAC
Write-Host "Step 2: Calculating HMAC..." -ForegroundColor Yellow

$hmacsha1 = New-Object System.Security.Cryptography.HMACSHA1
$hmacsha1.key = [Text.Encoding]::UTF8.GetBytes($sharedSecret)
$message = "$nonce`0$username`0$password`0admin"
$signature = $hmacsha1.ComputeHash([Text.Encoding]::UTF8.GetBytes($message))
$mac = [System.BitConverter]::ToString($signature).Replace("-","").ToLower()

Write-Host "HMAC calculated" -ForegroundColor Green

# Step 3: Create user
Write-Host "Step 3: Creating admin user..." -ForegroundColor Yellow

$body = @{
    nonce = $nonce
    username = $username
    password = $password
    admin = $true
    mac = $mac
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $nonceUrl -Method POST -Body $body -ContentType "application/json"
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! ADMIN USER CREATED!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "LOGIN CREDENTIALS:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Element Web (Chat):" -ForegroundColor Yellow
    Write-Host "  URL: https://cozy-dragon-54547b.netlify.app/#/login"
    Write-Host "  Username: admin"
    Write-Host "  Password: $password"
    Write-Host ""
    Write-Host "  Synapse Admin (User Management):" -ForegroundColor Yellow
    Write-Host "  URL: https://cravex-admin.netlify.app"
    Write-Host "  Homeserver: https://matrix-synapse.up.railway.app"
    Write-Host "  Username: admin"
    Write-Host "  Password: $password"
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "ERROR: Could not create user" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Yellow
    }
    
    exit 1
}




