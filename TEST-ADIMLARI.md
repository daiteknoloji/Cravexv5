# Test Adımları - Admin User Aktif ✅

## Durum
- ✅ Admin user aktif (`deactivated = 0`)
- ✅ Password hash mevcut (`$2b$12$...`)
- ✅ Admin yetkisi var (`admin = 1`)

## Test Adımları

### 1. Matrix Synapse Restart (ÖNEMLİ!)
Railway Dashboard → Matrix Synapse servisi → **Restart**

Bu, admin user'ın aktif durumunu Matrix Synapse'e bildirir.

### 2. Admin Panel Restart (ÖNEMLİ!)
Railway Dashboard → Admin Panel servisi → **Restart**

Bu, yeni kod değişikliklerini yükler.

### 3. Yeni Kullanıcı Oluşturma Testi

1. **Admin Panel'e git:** `https://considerate-adaptation-production.up.railway.app/`
2. **Login:** `admin` / `GüçlüBirŞifre123!`
3. **Kullanıcılar → Yeni Kullanıcı**
4. **Bilgileri gir:**
   - Username: `test6`
   - Password: `12344321`
   - Display Name: `Test 6` (opsiyonel)
5. **Oluştur**

### 4. Railway Admin Panel Loglarını Kontrol Et

Şu logları ara:
```
[INFO] No admin token found, attempting auto-login for @admin:matrix-synapse.up.railway.app...
[INFO] Auto-login successful! Token obtained: ...
[DEBUG] Admin token found: ...
[DEBUG] Calling Synapse API: https://matrix-synapse.up.railway.app/_synapse/admin/v2/users/@test6:matrix-synapse.up.railway.app
[INFO] User created via Matrix API. Verifying password...
[INFO] Password verification successful!
```

**Eğer bu loglar görünüyorsa:** ✅ Başarılı!

**Eğer `Auto-login failed` görünüyorsa:**
- `ADMIN_PASSWORD` environment variable'ı yanlış olabilir
- Admin user'ın şifresi Matrix Synapse'de farklı olabilir

### 5. Element Web Login Testi

1. **Element Web'e git**
2. **Login:**
   - Username: `test6`
   - Password: `12344321`
3. **Başarılı olmalı** ✅

### 6. Password Reset Testi

1. **Admin Panel → Kullanıcılar → `test6` → Şifre Değiştir**
2. **Yeni şifre:** `12345678`
3. **Kaydet**
4. **Element Web'de yeni şifre ile login dene:**
   - Username: `test6`
   - Password: `12345678`
5. **Başarılı olmalı** ✅

## Beklenen Sonuçlar

### ✅ Başarılı Senaryo:
- Admin Panel'de kullanıcı oluşturma başarılı
- Railway loglarında `Auto-login successful!` görünüyor
- Railway loglarında `Password verification successful!` görünüyor
- Element Web'de login başarılı
- Password reset başarılı

### ❌ Başarısız Senaryo:
- `Auto-login failed: 403 - Invalid username or password`
  - **Çözüm:** `ADMIN_PASSWORD` environment variable'ını kontrol et
- `Matrix API failed: 403`
  - **Çözüm:** Admin user'ın Matrix Synapse'de aktif olduğundan emin ol
- `Matrix API error: Connection timeout`
  - **Çözüm:** `SYNAPSE_URL` environment variable'ını kontrol et

## Sorun Giderme

### Sorun 1: Auto-login Başarısız
**Log:** `Auto-login failed: 403 - Invalid username or password`

**Kontrol:**
1. Railway Admin Panel → Variables → `ADMIN_PASSWORD`
2. Matrix Synapse'deki admin user şifresi ile eşleştiğinden emin ol

**Çözüm:**
- `ADMIN_PASSWORD` değerini Matrix Synapse'deki admin user şifresi ile eşleştir
- Admin Panel'i restart et

### Sorun 2: Matrix API 403 Hatası
**Log:** `Matrix API failed: 403`

**Kontrol:**
```sql
SELECT name, admin, deactivated
FROM users
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

**Beklenen:**
- `admin`: `1`
- `deactivated`: `0`

**Çözüm:**
- Admin user'ı aktif et (zaten yaptık ✅)
- Matrix Synapse'i restart et

### Sorun 3: Connection Timeout
**Log:** `Matrix API error: Connection timeout`

**Kontrol:**
- Railway Admin Panel → Variables → `SYNAPSE_URL`
- Değer: `https://matrix-synapse.up.railway.app`

**Çözüm:**
- `SYNAPSE_URL` değerini kontrol et
- Matrix Synapse servisinin çalıştığından emin ol

## Sonuç

Admin user aktif! Şimdi:
1. ✅ Matrix Synapse'i restart et
2. ✅ Admin Panel'i restart et
3. ✅ Yeni kullanıcı oluştur
4. ✅ Login test et
5. ✅ Password reset test et

Sonuçları paylaş!

