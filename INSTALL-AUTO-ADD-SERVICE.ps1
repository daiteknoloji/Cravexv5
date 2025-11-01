# =============================================
# WINDOWS SERVIS OLARAK OTOMATIK ADMIN EKLEME
# =============================================
# Bu script Windows Task Scheduler'a otomatik
# admin ekleme görevini ekler
# =============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  WINDOWS SERVIS KURULUMU" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Join-Path $PSScriptRoot "AUTO-ADD-ADMIN.ps1"
$taskName = "Matrix-Auto-Add-Admin"

# Task var mı kontrol et
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "UYARI: '$taskName' gorevi zaten mevcut!" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Mevcut gorevi silip yeniden olusturmak ister misin? (E/H)"
    
    if ($response -eq "E" -or $response -eq "e") {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "Eski gorev silindi." -ForegroundColor Gray
    } else {
        Write-Host "Islem iptal edildi." -ForegroundColor Yellow
        exit
    }
}

Write-Host ""
Write-Host "Gorev olusturuluyor..." -ForegroundColor Yellow
Write-Host ""

# Gorev ayarları
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`" -IntervalSeconds 60"

# Trigger: Windows başladıktan 2 dakika sonra başla
$trigger = New-ScheduledTaskTrigger -AtStartup
$trigger.Delay = "PT2M"  # 2 dakika gecikme

# Settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Principal (SYSTEM olarak çalıştır)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# Görevi kaydet
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description "Matrix Synapse - Her yeni odaya otomatik admin ekler"
    
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BASARILI!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Windows Task Scheduler'a eklendi!" -ForegroundColor White
    Write-Host ""
    Write-Host "Gorev Adi: $taskName" -ForegroundColor Yellow
    Write-Host "Script: $scriptPath" -ForegroundColor Gray
    Write-Host "Calisma: Windows basladiginda otomatik" -ForegroundColor Gray
    Write-Host "Kontrol: Her 60 saniyede bir" -ForegroundColor Gray
    Write-Host ""
    
    # Şimdi başlat
    Write-Host "Gorevi simdi baslatmak ister misin? (E/H): " -NoNewline -ForegroundColor Cyan
    $startNow = Read-Host
    
    if ($startNow -eq "E" -or $startNow -eq "e") {
        Start-ScheduledTask -TaskName $taskName
        Write-Host ""
        Write-Host "Gorev baslatildi!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Durum kontrolu:" -ForegroundColor Yellow
        Write-Host "  Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
        Write-Host ""
    }
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "YONETIM:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Durumu gor:" -ForegroundColor White
    Write-Host "  Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Manuel baslat:" -ForegroundColor White
    Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Durdur:" -ForegroundColor White
    Write-Host "  Stop-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Kaldir:" -ForegroundColor White
    Write-Host "  Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Loglari gor:" -ForegroundColor White
    Write-Host "  Task Scheduler GUI -> Microsoft -> Windows" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host "HATA: Gorev olusturulamadi!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Not: Bu scripti YONETICI olarak calistirman gerekebilir!" -ForegroundColor Yellow
    Write-Host "Sag tik -> 'Run as Administrator'" -ForegroundColor Yellow
}

Write-Host ""

