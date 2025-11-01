# ========================================
# MATRIX FULL STACK - DURUM KONTROLU
# ========================================
# Bu script servislerin durumunu gosterir
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MATRIX FULL STACK DURUM RAPORU      " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Backend Container'lari Kontrol Et
Write-Host "BACKEND SERVISLERI (Docker):" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow
Write-Host ""

$containers = @(
    @{Name="matrix-synapse"; Display="Matrix Synapse Server"; Port=8008},
    @{Name="matrix-postgres"; Display="PostgreSQL Database"; Port=5432},
    @{Name="matrix-redis"; Display="Redis Cache"; Port=6379},
    @{Name="synapse-admin-ui"; Display="Docker Admin Panel"; Port=8082}
)

foreach ($container in $containers) {
    $status = docker ps --filter "name=$($container.Name)" --filter "status=running" -q 2>$null
    
    if ($status) {
        $health = docker inspect --format='{{.State.Health.Status}}' $container.Name 2>$null
        
        Write-Host "  [" -NoNewline
        if ($health -eq "healthy") {
            Write-Host "OK" -ForegroundColor Green -NoNewline
        } else {
            Write-Host "??" -ForegroundColor Yellow -NoNewline
        }
        Write-Host "] " -NoNewline
        Write-Host "$($container.Display)" -ForegroundColor White -NoNewline
        Write-Host " (Port: $($container.Port))" -ForegroundColor Gray
        
        if ($health -and $health -ne "healthy") {
            Write-Host "      Status: $health" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [" -NoNewline
        Write-Host "X" -ForegroundColor Red -NoNewline
        Write-Host "]  " -NoNewline
        Write-Host "$($container.Display)" -ForegroundColor DarkGray -NoNewline
        Write-Host " (DURMUS)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "FRONTEND SERVISLERI (Node.js):" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow
Write-Host ""

# Element Web Kontrol
$elementPort = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if ($elementPort) {
    $elementPid = $elementPort.OwningProcess
    Write-Host "  [" -NoNewline
    Write-Host "OK" -ForegroundColor Green -NoNewline
    Write-Host "] " -NoNewline
    Write-Host "Element Web" -ForegroundColor White -NoNewline
    Write-Host " (Port: 8080, PID: $elementPid)" -ForegroundColor Gray
} else {
    Write-Host "  [" -NoNewline
    Write-Host "X" -ForegroundColor Red -NoNewline
    Write-Host "]  " -NoNewline
    Write-Host "Element Web" -ForegroundColor DarkGray -NoNewline
    Write-Host " (DURMUS)" -ForegroundColor Red
}

# Synapse Admin Kontrol
$adminPort = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
if ($adminPort) {
    $adminPid = $adminPort.OwningProcess
    Write-Host "  [" -NoNewline
    Write-Host "OK" -ForegroundColor Green -NoNewline
    Write-Host "] " -NoNewline
    Write-Host "Synapse Admin" -ForegroundColor White -NoNewline
    Write-Host " (Port: 5173, PID: $adminPid)" -ForegroundColor Gray
} else {
    Write-Host "  [" -NoNewline
    Write-Host "X" -ForegroundColor Red -NoNewline
    Write-Host "]  " -NoNewline
    Write-Host "Synapse Admin" -ForegroundColor DarkGray -NoNewline
    Write-Host " (DURMUS)" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ERISIM ADRESLERI:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# URL'leri ve durumlarini goster
$urls = @(
    @{Name="Backend API"; URL="http://localhost:8008"; Port=8008},
    @{Name="Element Web"; URL="http://localhost:8080"; Port=8080},
    @{Name="Synapse Admin"; URL="http://localhost:5173"; Port=5173},
    @{Name="Docker Admin"; URL="http://localhost:8082"; Port=8082}
)

foreach ($url in $urls) {
    $isActive = $false
    
    # Docker container mu yoksa Node.js mi kontrol et
    if ($url.Port -eq 8008 -or $url.Port -eq 8082) {
        # Docker container
        $containerName = if ($url.Port -eq 8008) { "matrix-synapse" } else { "synapse-admin-ui" }
        $status = docker ps --filter "name=$containerName" --filter "status=running" -q 2>$null
        $isActive = [bool]$status
    } else {
        # Node.js process
        $portStatus = Get-NetTCPConnection -LocalPort $url.Port -State Listen -ErrorAction SilentlyContinue
        $isActive = [bool]$portStatus
    }
    
    Write-Host "  " -NoNewline
    if ($isActive) {
        Write-Host "[AKTIF]" -ForegroundColor Green -NoNewline
    } else {
        Write-Host "[KAPALI]" -ForegroundColor Red -NoNewline
    }
    Write-Host " $($url.Name): " -NoNewline -ForegroundColor White
    Write-Host "$($url.URL)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "KOMUTLAR:" -ForegroundColor Yellow
Write-Host "=========" -ForegroundColor Yellow
Write-Host "  Baslat:  " -NoNewline -ForegroundColor White
Write-Host ".\BASLAT.ps1" -ForegroundColor Green
Write-Host "  Durdur:  " -NoNewline -ForegroundColor White
Write-Host ".\DURDUR.ps1" -ForegroundColor Red
Write-Host "  Durum:   " -NoNewline -ForegroundColor White
Write-Host ".\DURUM.ps1" -ForegroundColor Cyan
Write-Host ""

# Veritabani bilgisi
Write-Host "VERITABANI:" -ForegroundColor Yellow
Write-Host "===========" -ForegroundColor Yellow

$pgRunning = docker ps --filter "name=matrix-postgres" --filter "status=running" -q 2>$null
if ($pgRunning) {
    try {
        $dbStats = docker exec matrix-postgres psql -U synapse_user -d synapse -t -c "SELECT (SELECT COUNT(*) FROM users) as users, (SELECT COUNT(*) FROM rooms) as rooms, (SELECT COUNT(*) FROM events) as messages, pg_size_pretty(pg_database_size('synapse')) as size;" 2>$null
        
        if ($dbStats) {
            $stats = $dbStats -split '\|'
            Write-Host "  Kullanicilar: " -NoNewline -ForegroundColor White
            Write-Host "$($stats[0].Trim())" -ForegroundColor Green
            Write-Host "  Odalar:       " -NoNewline -ForegroundColor White
            Write-Host "$($stats[1].Trim())" -ForegroundColor Green
            Write-Host "  Mesajlar:     " -NoNewline -ForegroundColor White
            Write-Host "$($stats[2].Trim())" -ForegroundColor Green
            Write-Host "  Boyut:        " -NoNewline -ForegroundColor White
            Write-Host "$($stats[3].Trim())" -ForegroundColor Green
        }
    } catch {
        Write-Host "  [INFO] Veritabani istatistikleri alinamadi" -ForegroundColor Gray
    }
} else {
    Write-Host "  [INFO] PostgreSQL calismyor" -ForegroundColor Gray
}

Write-Host ""

