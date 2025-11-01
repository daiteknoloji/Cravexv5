# 🔐 ADMIN TÜM MESAJLARI OKUMA KILAVUZU

Admin kullanıcısının tüm sohbetleri okuyabilmesi için 3 yöntem:

---

## 🎯 YÖNTEM 1: SYNAPSE ADMIN PANEL (EN KOLAY)

### Adım 1: Giriş Yap
```
URL: http://localhost:5173
Username: @admin:localhost
Password: Admin@2024!Guclu
```

### Adım 2: Odaları Görüntüle
1. Sol menüden **"Rooms"** tıkla
2. Tüm odaları göreceksin
3. Herhangi bir odaya tıkla

### Adım 3: Mesajları Oku
- **"Show Events"** butonuna tıkla
- Tüm mesajlar ve event'ler görünür
- Filtreleme ve arama yapabilirsin

**Avantajlar:**
- ✅ Görsel arayüz
- ✅ Kolay kullanım
- ✅ Filtreleme ve arama
- ✅ Tüm oda bilgileri

**Dezavantajlar:**
- ❌ Tek tek oda açman gerekir
- ❌ Toplu export yok

---

## 🔧 YÖNTEM 2: API İLE OTOMATIK (PROGRAMATIK)

### Adım 1: Admin Token Al

```powershell
# Token'ı al ve kaydet
.\get-admin-token.ps1
```

Çıktı:
```
ADMIN ACCESS TOKEN:
syt_YWRtaW4_ABCxyz123...
```

Token `admin-token.txt` dosyasına kaydedilir.

### Adım 2: Tüm Mesajları Al

```powershell
# Tüm odaların mesajlarını çek
.\get-all-messages.ps1
```

Veya token ile:
```powershell
.\get-all-messages.ps1 -Token "syt_YWRtaW4_..."
```

**Çıktı:**
- Tüm mesajlar JSON formatında kaydedilir
- `all-messages_20251031_143025.json` gibi dosya oluşur
- Son 10 mesaj ekranda gösterilir

**Avantajlar:**
- ✅ Otomatik
- ✅ Toplu işlem
- ✅ JSON export
- ✅ Script'lerle entegrasyon

**Dezavantajlar:**
- ❌ Komut satırı bilgisi gerekir
- ❌ Token yönetimi

---

## 📡 YÖNTEM 3: MANUEL API ÇAĞRILARI

### Token Al:

```powershell
$body = @{
    type = "m.login.password"
    user = "@admin:localhost"
    password = "Admin@2024!Guclu"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://localhost:8008/_matrix/client/r0/login" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$token = $response.access_token
Write-Host "Token: $token"
```

### Tüm Odaları Listele:

```powershell
$headers = @{"Authorization" = "Bearer $token"}

$rooms = Invoke-RestMethod `
    -Uri "http://localhost:8008/_synapse/admin/v1/rooms" `
    -Method Get `
    -Headers $headers

$rooms.rooms | Format-Table name, room_id, joined_members
```

### Belirli Bir Odanın Mesajlarını Al:

```powershell
$roomId = "!AbCdEfGhIjKlMnOp:localhost"

$messages = Invoke-RestMethod `
    -Uri "http://localhost:8008/_synapse/admin/v2/rooms/$roomId/messages" `
    -Method Get `
    -Headers $headers

$messages.chunk | Where-Object {$_.type -eq "m.room.message"} | 
    Select-Object sender, @{N='message';E={$_.content.body}}, origin_server_ts
```

### Tüm Event'leri Al (Her Şey):

```powershell
$events = Invoke-RestMethod `
    -Uri "http://localhost:8008/_synapse/admin/v1/rooms/$roomId/state" `
    -Method Get `
    -Headers $headers

$events.state | Format-List
```

---

## 🗃️ YÖNTEM 4: DOĞRUDAN VERİTABANINDAN (İLERİ SEVİYE)

**UYARI: Bu yöntem sadece acil durumlarda kullanılmalı!**

### Event'leri Listele:

```powershell
docker exec matrix-postgres psql -U synapse_user -d synapse -c "
SELECT 
    e.room_id,
    e.sender,
    e.type,
    ej.json::json->'content'->>'body' as message,
    to_timestamp(e.origin_server_ts/1000) as timestamp
FROM events e
LEFT JOIN event_json ej ON e.event_id = ej.event_id
WHERE e.type = 'm.room.message'
ORDER BY e.stream_ordering DESC
LIMIT 100;
"
```

### Belirli Bir Odanın Mesajları:

```powershell
docker exec matrix-postgres psql -U synapse_user -d synapse -c "
SELECT 
    e.sender,
    ej.json::json->'content'->>'body' as message,
    to_timestamp(e.origin_server_ts/1000) as timestamp
FROM events e
LEFT JOIN event_json ej ON e.event_id = ej.event_id
WHERE e.room_id = '!YOUR_ROOM_ID:localhost'
  AND e.type = 'm.room.message'
ORDER BY e.stream_ordering ASC;
"
```

**Avantajlar:**
- ✅ En hızlı
- ✅ Direkt veri erişimi
- ✅ SQL sorguları

**Dezavantajlar:**
- ❌ Riskli (yanlış sorgu veriyi bozabilir)
- ❌ Şifreleme göz ardı edilir
- ❌ Matrix protokolü atlanır

---

## 🔑 SYNAPSE ADMIN API ENDPOINT'LERİ

### Temel Endpoint'ler:

| Endpoint | Açıklama |
|----------|----------|
| `GET /_synapse/admin/v1/rooms` | Tüm odaları listele |
| `GET /_synapse/admin/v1/rooms/{room_id}` | Oda detayları |
| `GET /_synapse/admin/v2/rooms/{room_id}/messages` | Oda mesajları |
| `GET /_synapse/admin/v1/rooms/{room_id}/state` | Oda state/event'leri |
| `GET /_synapse/admin/v1/users/{user_id}/media` | Kullanıcı medyaları |
| `GET /_synapse/admin/v1/rooms/{room_id}/members` | Oda üyeleri |

### Filtreleme ve Sayfalama:

```powershell
# İlk 100 oda
Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms?limit=100" -Headers $headers

# Sonraki sayfa
Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v1/rooms?from=next_token" -Headers $headers

# Belirli tarihten sonraki mesajlar
$from = [DateTimeOffset]::Now.AddDays(-7).ToUnixTimeMilliseconds()
Invoke-RestMethod -Uri "http://localhost:8008/_synapse/admin/v2/rooms/$roomId/messages?from=$from" -Headers $headers
```

---

## 📊 TOPLU RAPOR OLUŞTURMA

### Script ile Günlük Rapor:

```powershell
# Token al
.\get-admin-token.ps1

# Tüm mesajları çek
.\get-all-messages.ps1

# JSON'ı oku ve analiz et
$messages = Get-Content "all-messages_*.json" | ConvertFrom-Json

# İstatistikler
Write-Host "Toplam Mesaj: $($messages.Count)"
Write-Host "Aktif Kullanıcılar: $($messages.Sender | Select-Object -Unique).Count"
Write-Host "Aktif Odalar: $($messages.Room | Select-Object -Unique).Count"

# En çok mesaj yazan kullanıcı
$messages | Group-Object Sender | Sort-Object Count -Descending | Select-Object -First 5
```

---

## 🔐 GÜVENLİK NOTLARI

### Token Güvenliği:
- ✅ Token'ları asla git'e commit etme
- ✅ `admin-token.txt` dosyasını `.gitignore`'a ekle
- ✅ Token'lar expire olabilir, yenile
- ✅ Üretim ortamında token rotation kullan

### Yasal Uyarı:
- ⚠️ Kullanıcı gizliliği önemli!
- ⚠️ Mesaj okuma yetkilerini belge altına al
- ⚠️ GDPR/KVKK uyumlu ol
- ⚠️ Audit log tut

---

## 🛠️ OTOMASYON ÖRNEKLERİ

### Günlük Backup:

```powershell
# Her gün saat 02:00'de çalışacak task
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-File C:\path\to\get-all-messages.ps1"

$trigger = New-ScheduledTaskTrigger -Daily -At 2am

Register-ScheduledTask -Action $action -Trigger $trigger `
    -TaskName "Matrix-Daily-Backup" -Description "Daily message backup"
```

### Belirli Kelime Arama:

```powershell
# Tüm mesajları al
.\get-all-messages.ps1

# JSON'dan ara
$messages = Get-Content "all-messages_*.json" | ConvertFrom-Json
$searchTerm = "önemli"
$results = $messages | Where-Object {$_.Body -like "*$searchTerm*"}

Write-Host "Bulunan mesaj sayısı: $($results.Count)"
$results | Format-Table Timestamp, Sender, Room, Body
```

---

## 📝 ÖNERİLEN KULLANIM

### Production Ortamı İçin:

1. **Synapse Admin Panel** kullan (manuel işlemler için)
2. **API scriptleri** kullan (otomatik raporlar için)
3. **Veritabanı yedeklerini** düzenli al
4. **Audit log** sistemi kur
5. **Token rotation** uygula
6. **Rate limiting** ekle

### Development Ortamı İçin:

1. **Synapse Admin Panel** yeterli
2. Test için **API scriptleri** kullan
3. Veritabanına doğrudan erişim (dikkatli)

---

## 🆘 SORUN GİDERME

### "401 Unauthorized" Hatası:
```powershell
# Token expired olabilir, yeni token al
.\get-admin-token.ps1
```

### "403 Forbidden" Hatası:
```powershell
# Kullanıcı admin mi kontrol et
docker exec matrix-postgres psql -U synapse_user -d synapse -c "SELECT name, admin FROM users;"
```

### Token Çalışmıyor:
```powershell
# Token'ı test et
$headers = @{"Authorization" = "Bearer YOUR_TOKEN"}
Invoke-RestMethod -Uri "http://localhost:8008/_matrix/client/r0/account/whoami" -Headers $headers
```

---

## 📚 EK KAYNAKLAR

- [Synapse Admin API Docs](https://element-hq.github.io/synapse/latest/usage/administration/admin_api/)
- [Matrix Client-Server API](https://spec.matrix.org/v1.1/client-server-api/)
- [Synapse Admin Panel GitHub](https://github.com/Awesome-Technologies/synapse-admin)

---

**En Temiz Yöntem:** Synapse Admin Panel (http://localhost:5173)
**En Güçlü Yöntem:** API Script'leri
**En Hızlı Yöntem:** Direkt veritabanı (dikkatli kullan)

---

Son Güncelleme: 31 Ekim 2025

