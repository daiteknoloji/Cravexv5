# Railway Settings Export Script v2
# Railway servislerinin tüm ayarlarını export eder ve local backup alır

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RAILWAY SETTINGS EXPORT v2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Backup klasörü oluştur
$backupDir = "railway-backups"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupPath = Join-Path $backupDir "railway-settings-$timestamp"

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

New-Item -ItemType Directory -Path $backupPath | Out-Null

Write-Host "Backup klasörü oluşturuldu: $backupPath" -ForegroundColor Green
Write-Host ""

# Railway CLI kontrolü
Write-Host "Railway CLI kontrol ediliyor..." -ForegroundColor Yellow
try {
    $railwayVersion = railway --version 2>&1
    Write-Host "Railway CLI bulundu: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "Railway CLI bulunamadı! Lütfen kurun:" -ForegroundColor Red
    Write-Host "npm install -g @railway/cli" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Railway login kontrolü
Write-Host "Railway login kontrol ediliyor..." -ForegroundColor Yellow
try {
    railway whoami 2>&1 | Out-Null
    Write-Host "Railway'a giriş yapılmış ✅" -ForegroundColor Green
} catch {
    Write-Host "Railway'a giriş yapılmamış! Lütfen giriş yapın:" -ForegroundColor Red
    Write-Host "railway login" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Proje bilgilerini al
Write-Host "Proje bilgileri alınıyor..." -ForegroundColor Yellow
$projectInfo = railway project 2>&1
Write-Host "Proje: $projectInfo" -ForegroundColor Green
Write-Host ""

# Servis listesini al
Write-Host "Servisler listeleniyor..." -ForegroundColor Yellow
$services = railway service list 2>&1

# Servisleri parse et ve export et
$serviceNames = @()

# Railway servisleri (tahmin edilen)
$knownServices = @(
    "cravexv5",           # Synapse
    "considerate-adaptation",  # Admin Panel
    "surprising-emotion"   # Element Web
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SERVİSLER EXPORT EDİLİYOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($serviceName in $knownServices) {
    Write-Host "Servis: $serviceName" -ForegroundColor Yellow
    
    $serviceBackupDir = Join-Path $backupPath $serviceName
    New-Item -ItemType Directory -Path $serviceBackupDir -Force | Out-Null
    
    # Service config export
    Write-Host "  → Config export ediliyor..." -ForegroundColor Gray
    try {
        railway service --service $serviceName 2>&1 | Out-File -FilePath (Join-Path $serviceBackupDir "service-info.txt") -Encoding UTF8
    } catch {
        Write-Host "    ⚠️ Config export edilemedi" -ForegroundColor Yellow
    }
    
    # Variables export
    Write-Host "  → Variables export ediliyor..." -ForegroundColor Gray
    try {
        railway variables --service $serviceName --json 2>&1 | Out-File -FilePath (Join-Path $serviceBackupDir "variables.json") -Encoding UTF8
        
        # Human-readable format
        railway variables --service $serviceName 2>&1 | Out-File -FilePath (Join-Path $serviceBackupDir "variables.txt") -Encoding UTF8
    } catch {
        Write-Host "    ⚠️ Variables export edilemedi" -ForegroundColor Yellow
    }
    
    # Networking info
    Write-Host "  → Networking bilgileri export ediliyor..." -ForegroundColor Gray
    try {
        railway service --service $serviceName 2>&1 | Select-String -Pattern "domain|port|networking" | Out-File -FilePath (Join-Path $serviceBackupDir "networking.txt") -Encoding UTF8
    } catch {
        Write-Host "    ⚠️ Networking bilgileri export edilemedi" -ForegroundColor Yellow
    }
    
    Write-Host "  ✅ $serviceName export edildi" -ForegroundColor Green
    Write-Host ""
}

# Railway config dosyalarını kopyala
Write-Host "Railway config dosyaları kopyalanıyor..." -ForegroundColor Yellow

$configFiles = @(
    "railway-synapse.json",
    "railway-admin-panel.json",
    "railway-turnserver.json"
)

foreach ($configFile in $configFiles) {
    if (Test-Path $configFile) {
        Copy-Item $configFile -Destination (Join-Path $backupPath $configFile) -Force
        Write-Host "  ✅ $configFile kopyalandı" -ForegroundColor Green
    }
}

Write-Host ""

# Environment variables template oluştur
Write-Host "Environment variables template oluşturuluyor..." -ForegroundColor Yellow

$envTemplate = @"
# Railway Environment Variables Template
# Export Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Synapse Service (cravexv5)
SYNAPSE_SERVER_NAME="matrix-synapse.up.railway.app"
SYNAPSE_PUBLIC_BASEURL="https://matrix-synapse.up.railway.app/"
WEB_CLIENT_LOCATION="https://surprising-emotion-production.up.railway.app"
POSTGRES_HOST=`${{Postgres.PGHOST}}
POSTGRES_PORT=`${{Postgres.PGPORT}}
POSTGRES_USER=`${{Postgres.PGUSER}}
POSTGRES_PASSWORD=`${{Postgres.PGPASSWORD}}
POSTGRES_DB=`${{Postgres.PGDATABASE}}

# Admin Panel Service (considerate-adaptation)
HOMESERVER_DOMAIN="matrix-synapse.up.railway.app"
SYNAPSE_URL="https://matrix-synapse.up.railway.app"
ADMIN_PASSWORD="GüçlüBirŞifre123!"
PGDATABASE=`${{Postgres.PGDATABASE}}
PGHOST=`${{Postgres.PGHOST}}
PGPASSWORD=`${{Postgres.PGPASSWORD}}
PGPORT=`${{Postgres.PGPORT}}
PGUSER=`${{Postgres.PGUSER}}
RAILWAY_DOCKERFILE_PATH="admin-panel.Dockerfile"

# Element Web Service (surprising-emotion)
# (Railway otomatik deploy ediyor, config dosyası kullanıyor)
"@

$envTemplate | Out-File -FilePath (Join-Path $backupPath "railway-env-template.txt") -Encoding UTF8
Write-Host "  ✅ Environment variables template oluşturuldu" -ForegroundColor Green
Write-Host ""

# Özet dosyası oluştur
Write-Host "Özet dosyası oluşturuluyor..." -ForegroundColor Yellow

$summary = @"
# Railway Settings Backup Summary
Export Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Backup Path: $backupPath

## Servisler:
1. Synapse (cravexv5)
   - Domain: matrix-synapse.up.railway.app
   - Config: railway-synapse.json

2. Admin Panel (considerate-adaptation)
   - Domain: considerate-adaptation-production.up.railway.app
   - Config: railway-admin-panel.json

3. Element Web (surprising-emotion)
   - Domain: surprising-emotion-production.up.railway.app
   - Config: www/element-web/config.json

## Dosyalar:
- railway-synapse.json: Synapse servis config
- railway-admin-panel.json: Admin Panel servis config
- railway-turnserver.json: TURN Server servis config
- railway-env-template.txt: Environment variables template

## Restore:
Railway Dashboard'dan manuel olarak restore edebilirsiniz:
1. Railway Dashboard → Service → Variables
2. Variables'ları tek tek ekleyin
3. Config dosyalarını Railway'a yükleyin
"@

$summary | Out-File -FilePath (Join-Path $backupPath "README.md") -Encoding UTF8
Write-Host "  ✅ Özet dosyası oluşturuldu" -ForegroundColor Green
Write-Host ""

# JSON formatında tam backup
Write-Host "JSON formatında tam backup oluşturuluyor..." -ForegroundColor Yellow

$fullBackup = @{
    exportDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    backupPath = $backupPath
    services = @()
}

foreach ($serviceName in $knownServices) {
    $serviceInfo = @{
        name = $serviceName
        config = $null
        variables = $null
    }
    
    # Config dosyasını oku
    $configFile = "railway-$($serviceName -replace 'considerate-adaptation', 'admin-panel' -replace 'surprising-emotion', 'element-web').json"
    if (Test-Path $configFile) {
        $serviceInfo.config = Get-Content $configFile -Raw | ConvertFrom-Json
    }
    
    # Variables dosyasını oku
    $varsFile = Join-Path $backupPath $serviceName "variables.json"
    if (Test-Path $varsFile) {
        try {
            $serviceInfo.variables = Get-Content $varsFile -Raw | ConvertFrom-Json
        } catch {
            $serviceInfo.variables = Get-Content $varsFile -Raw
        }
    }
    
    $fullBackup.services += $serviceInfo
}

$fullBackup | ConvertTo-Json -Depth 10 | Out-File -FilePath (Join-Path $backupPath "railway-backup-full.json") -Encoding UTF8
Write-Host "  ✅ JSON backup oluşturuldu" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ BACKUP TAMAMLANDI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backup konumu: $backupPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backup içeriği:" -ForegroundColor Yellow
Get-ChildItem -Path $backupPath -Recurse | Select-Object FullName | Format-Table -AutoSize
Write-Host ""


