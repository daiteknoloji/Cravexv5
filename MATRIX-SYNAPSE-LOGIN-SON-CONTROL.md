# 🔍 Matrix Synapse Login Son Kontrol

## ✅ Mevcut Durum

Her iki kullanıcı da doğru formatta:

### Admin Kullanıcı:
- Password hash: `$2b$12$/w.NVlLy7gr0kSzhRoawB.x...`
- Hash length: 60 ✅
- Bcrypt format: `$2b$12$...` ✅
- `deactivated`: 0 (aktif) ✅
- `is_guest`: 0 ✅

### test1 Kullanıcı:
- Password hash: `$2b$12$HW0JeQG0/Df0VcCbO0vsSO9L0OLn8iBhpesMCfqgZ/XuHrbCBT/nm`
- Hash length: 60 ✅
- Bcrypt format: `$2b$12$...` ✅
- `deactivated`: 0 (aktif) ✅
- `is_guest`: 0 ✅

**Ama hala login çalışmıyor!**

---

## 🔧 Sorun Analizi

Element Web console'da görülen hata:
```
POST https://matrix-synapse.up.railway.app/_matrix/client/v3/login 403 (Forbidden)
```

Bu, Matrix Synapse'in login'i reddettiği anlamına geliyor.

---

## 🎯 Olası Nedenler

### 1. Matrix Synapse Cache Sorunu

**Sorun:** Matrix Synapse cache'i güncel değil olabilir.

**Çözüm:**
```
Railway Dashboard → Matrix Synapse → Restart
```

---

### 2. Matrix Synapse Loglarını Kontrol Et

**Railway Matrix Synapse Loglarında şunları ara:**

```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
User @test1:matrix-synapse.up.railway.app
password_hash
bcrypt.checkpw
```

**Örnek log formatı:**
```
2025-11-09T21:18:18.506274268Z [inf] POST /_matrix/client/v3/login
2025-11-09T21:18:18.506274268Z [err] M_FORBIDDEN: Invalid username or password
2025-11-09T21:18:18.506274268Z [err] User @test1:matrix-synapse.up.railway.app login failed
2025-11-09T21:18:18.506274268Z [err] password_hash check failed
```

---

### 3. Matrix Synapse'in Password Hash'i Okuma Şekli

Matrix Synapse password hash'i şu şekilde okur:
1. `users` tablosundan `password_hash` alır
2. `bcrypt.checkpw()` ile kontrol eder
3. `deactivated = 0` kontrolü yapar
4. `is_guest = 0` kontrolü yapar

**Ama şu kontrolleri de yapabilir:**
- `password_hash IS NOT NULL` kontrolü
- `password_hash` format kontrolü
- `password_hash` length kontrolü

---

### 4. Matrix Synapse Configuration Sorunu

Matrix Synapse'in `homeserver.yaml` dosyasında şu ayarlar olabilir:
- `enable_registration: false` - Yeni kullanıcı kaydı kapalı olabilir
- `password_config` - Password policy ayarları
- `user_directory` - User directory ayarları

**Kontrol:** Railway Matrix Synapse servisinin configuration dosyasını kontrol edin.

---

## 🔧 Debug Adımları

### Adım 1: Railway Matrix Synapse Loglarını Kontrol Et

1. Railway Dashboard → Matrix Synapse → Logs
2. Element Web'de login denemesi yap:
   - Username: `test1`
   - Password: (oluşturduğun şifre)
3. Login denemesi sırasındaki tüm logları kopyala

**Aranacak loglar:**
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
User @test1:matrix-synapse.up.railway.app
password_hash
bcrypt.checkpw
```

### Adım 2: Matrix Synapse'i Yeniden Başlat

1. Railway Dashboard → Matrix Synapse → Restart
2. Yeniden başladıktan sonra login dene

### Adım 3: Password Hash'i Manuel Test Et

Railway PostgreSQL'e bağlan ve şu sorguyu çalıştır:

```sql
-- Password hash'i kontrol et
SELECT 
    name,
    password_hash,
    password_hash IS NOT NULL as hash_not_null,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    LENGTH(password_hash) as hash_length,
    deactivated,
    is_guest
FROM users 
WHERE name = '@test1:matrix-synapse.up.railway.app';

-- Admin kullanıcıyla karşılaştır
SELECT 
    name,
    password_hash,
    password_hash IS NOT NULL as hash_not_null,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    LENGTH(password_hash) as hash_length,
    deactivated,
    is_guest
FROM users 
WHERE name LIKE '@admin:%' 
LIMIT 1;
```

### Adım 4: Matrix Synapse API'yi Test Et

Railway Terminal'den Matrix Synapse'e bağlan ve login'i test et:

```bash
# Matrix Synapse container'ına bağlan
railway run --service matrix-synapse bash

# Login test et (eğer curl varsa)
curl -X POST https://matrix-synapse.up.railway.app/_matrix/client/v3/login \
  -H "Content-Type: application/json" \
  -d '{
    "type": "m.login.password",
    "identifier": {
      "type": "m.id.user",
      "user": "test1"
    },
    "password": "12345678"
  }'
```

---

## 📝 Gerekli Loglar

### Railway Matrix Synapse Logları:
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
User @test1:matrix-synapse.up.railway.app
password_hash
bcrypt.checkpw
```

### Element Web Console Logları:
```
POST https://matrix-synapse.up.railway.app/_matrix/client/v3/login 403 (Forbidden)
```

---

## ⚠️ Önemli Notlar

1. **Her iki kullanıcı da doğru formatta** ✅
2. **Password hash doğru format** (`$2b$12$...`) ✅
3. **Tüm tablolarda mevcut** ✅
4. **Ama login çalışmıyor** ❌

**Sorun muhtemelen:**
- Matrix Synapse cache'i güncel değil
- Matrix Synapse'in beklediği başka bir kontrol var
- Matrix Synapse configuration sorunu
- Matrix Synapse loglarında daha detaylı hata var

---

## 🔧 Sonraki Adımlar

1. ✅ Veritabanı kontrolleri yapıldı - BAŞARILI
2. ⏳ **Railway Matrix Synapse loglarını kontrol et** (EN ÖNEMLİ!)
3. ⏳ Matrix Synapse'i yeniden başlat
4. ⏳ Element Web'de login dene
5. ⏳ Matrix Synapse API'yi test et

**ÖNEMLİ:** Railway Matrix Synapse loglarını mutlaka kontrol edin! Bu loglar sorunun kaynağını gösterecek.

