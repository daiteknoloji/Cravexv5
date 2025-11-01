# =============================================
# VERİTABANINDAN MESAJLARI SORGULA
# =============================================

param(
    [string]$Query = "last",
    [string]$RoomId = "",
    [string]$Sender = "",
    [string]$Search = "",
    [int]$Limit = 20
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERİTABANI MESAJ SORGULAMA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# SQL sorgusu oluştur
$sql = ""

switch ($Query) {
    "last" {
        Write-Host "Son $Limit mesaj getiriliyor..." -ForegroundColor Yellow
        $sql = "SELECT to_timestamp(origin_server_ts/1000) as zaman, sender as gonderen, room_id as oda, content::json->>'body' as mesaj FROM events WHERE type = 'm.room.message' ORDER BY origin_server_ts DESC LIMIT $Limit;"
    }
    "room" {
        if ($RoomId -eq "") {
            Write-Host "HATA: -RoomId parametresi gerekli!" -ForegroundColor Red
            Write-Host "Ornek: .\db-query-messages.ps1 -Query room -RoomId '!abc:localhost'" -ForegroundColor Yellow
            exit
        }
        Write-Host "Oda mesajlari getiriliyor: $RoomId" -ForegroundColor Yellow
        $sql = "SELECT to_timestamp(origin_server_ts/1000) as zaman, sender as gonderen, content::json->>'body' as mesaj FROM events WHERE room_id = '$RoomId' AND type = 'm.room.message' ORDER BY origin_server_ts ASC;"
    }
    "user" {
        if ($Sender -eq "") {
            Write-Host "HATA: -Sender parametresi gerekli!" -ForegroundColor Red
            Write-Host "Ornek: .\db-query-messages.ps1 -Query user -Sender '@1k:localhost'" -ForegroundColor Yellow
            exit
        }
        Write-Host "Kullanici mesajlari getiriliyor: $Sender" -ForegroundColor Yellow
        $sql = "SELECT to_timestamp(origin_server_ts/1000) as zaman, room_id as oda, content::json->>'body' as mesaj FROM events WHERE sender = '$Sender' AND type = 'm.room.message' ORDER BY origin_server_ts DESC LIMIT $Limit;"
    }
    "search" {
        if ($Search -eq "") {
            Write-Host "HATA: -Search parametresi gerekli!" -ForegroundColor Red
            Write-Host "Ornek: .\db-query-messages.ps1 -Query search -Search 'test'" -ForegroundColor Yellow
            exit
        }
        Write-Host "Mesaj arama: '$Search'" -ForegroundColor Yellow
        $sql = "SELECT to_timestamp(origin_server_ts/1000) as zaman, sender as gonderen, room_id as oda, content::json->>'body' as mesaj FROM events WHERE type = 'm.room.message' AND content::json->>'body' LIKE '%$Search%' ORDER BY origin_server_ts DESC LIMIT $Limit;"
    }
    "rooms" {
        Write-Host "Tum odalar getiriliyor..." -ForegroundColor Yellow
        $sql = "SELECT room_id, name, creator, to_timestamp(creation_ts/1000) as olusturma FROM rooms ORDER BY creation_ts DESC;"
    }
    "stats" {
        Write-Host "Mesaj istatistikleri getiriliyor..." -ForegroundColor Yellow
        $sql = "SELECT room_id as oda, COUNT(*) as mesaj_sayisi, COUNT(DISTINCT sender) as kullanici_sayisi FROM events WHERE type = 'm.room.message' GROUP BY room_id ORDER BY mesaj_sayisi DESC;"
    }
    default {
        Write-Host "HATA: Gecersiz sorgu tipi!" -ForegroundColor Red
        Write-Host ""
        Write-Host "KULLANIM:" -ForegroundColor Yellow
        Write-Host "  .\db-query-messages.ps1 -Query last [-Limit 20]" -ForegroundColor White
        Write-Host "  .\db-query-messages.ps1 -Query room -RoomId '!abc:localhost'" -ForegroundColor White
        Write-Host "  .\db-query-messages.ps1 -Query user -Sender '@1k:localhost' [-Limit 50]" -ForegroundColor White
        Write-Host "  .\db-query-messages.ps1 -Query search -Search 'test' [-Limit 20]" -ForegroundColor White
        Write-Host "  .\db-query-messages.ps1 -Query rooms" -ForegroundColor White
        Write-Host "  .\db-query-messages.ps1 -Query stats" -ForegroundColor White
        Write-Host ""
        exit
    }
}

Write-Host ""
Write-Host "SQL: $sql" -ForegroundColor DarkGray
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Sorguyu çalıştır
docker exec matrix-postgres psql -U synapse_user -d synapse -c $sql

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

