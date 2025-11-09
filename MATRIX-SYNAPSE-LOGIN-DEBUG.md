# 🔍 Matrix Synapse Login Debug Rehberi

## ✅ Mevcut Durum

Kullanıcı başarıyla oluşturuldu ve tüm kontroller geçti:

- ✅ `deactivated = 0` (aktif)
- ✅ `is_guest = 0` (normal kullanıcı)
- ✅ `admin = 0` (admin değil)
- ✅ Password hash doğru format (`$2b$12$...`)
- ✅ Password hash length: 60 (doğru)
- ✅ Tüm tablolarda mevcut (users, profiles, user_directory, user_directory_search)

**Ama hala login çalışmıyor!**

---

## 🔧 Olası Nedenler ve Çözümler

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
```

**Örnek log formatı:**
```
2025-11-09T21:18:18.506274268Z [inf] POST /_matrix/client/v3/login
2025-11-09T21:18:18.506274268Z [err] M_FORBIDDEN: Invalid username or password
2025-11-09T21:18:18.506274268Z [err] User @testuser:matrix-synapse.up.railway.app login failed
```

---

### 3. Matrix Synapse'in Password Hash'i Okuma Şekli

Matrix Synapse password hash'i şu şekilde okur:
1. `users` tablosundan `password_hash` alır
2. `bcrypt.checkpw()` ile kontrol eder
3. `deactivated = 0` kontrolü yapar
4. `is_guest = 0` kontrolü yapar

**Kontrol:**
```sql
-- Password hash'in Matrix Synapse'in beklediği formatta olduğunu kontrol et
SELECT 
    name,
    password_hash,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    LENGTH(password_hash) as hash_length,
    deactivated,
    is_guest
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';
```

---

### 4. Matrix Synapse'in Beklediği Başka Tablolar

Matrix Synapse login sırasında şu tabloları kontrol eder:
- `users` ✅
- `profiles` ✅
- `user_directory` ✅
- `user_directory_search` ✅

**Ama şunları da kontrol edebilir:**
- `user_ips` (IP adresleri)
- `user_threepids` (email/telefon)
- `user_filters` (kullanıcı filtreleri)

**Kontrol:**
```sql
-- Matrix Synapse'in beklediği diğer tabloları kontrol et
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%user%' 
ORDER BY table_name;
```

---

### 5. Matrix Synapse Configuration Sorunu

Matrix Synapse'in `homeserver.yaml` dosyasında şu ayarlar olabilir:
- `enable_registration: false` - Yeni kullanıcı kaydı kapalı olabilir
- `password_config` - Password policy ayarları
- `user_directory` - User directory ayarları

**Kontrol:** Railway Matrix Synapse servisinin configuration dosyasını kontrol edin.

---

## 🎯 Debug Adımları

### Adım 1: Matrix Synapse Loglarını Kontrol Et

1. Railway Dashboard → Matrix Synapse → Logs
2. Element Web'de login denemesi yap
3. Login denemesi sırasındaki tüm logları kopyala

**Aranacak loglar:**
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
User @testuser:matrix-synapse.up.railway.app
password_hash
bcrypt
```

### Adım 2: Matrix Synapse'i Yeniden Başlat

1. Railway Dashboard → Matrix Synapse → Restart
2. Yeniden başladıktan sonra login dene

### Adım 3: Password Hash'i Manuel Kontrol Et

```sql
-- Password hash'i kontrol et
SELECT 
    name,
    password_hash,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    LENGTH(password_hash) as hash_length
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Mevcut çalışan bir kullanıcıyla karşılaştır
SELECT 
    name,
    password_hash,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    LENGTH(password_hash) as hash_length
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
      "user": "testuser"
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
User @testuser:matrix-synapse.up.railway.app
password_hash
bcrypt.checkpw
```

### Element Web Console Logları:
```
POST https://matrix-synapse.up.railway.app/_matrix/client/v3/login 403 (Forbidden)
```

---

## ⚠️ Önemli Notlar

1. **Kullanıcı aktif durumda** (`deactivated = 0`) ✅
2. **Password hash doğru format** (`$2b$12$...`) ✅
3. **Tüm tablolarda mevcut** ✅
4. **Ama login çalışmıyor** ❌

**Sorun muhtemelen:**
- Matrix Synapse cache'i güncel değil
- Matrix Synapse'in beklediği başka bir kontrol var
- Matrix Synapse configuration sorunu

---

## 🔧 Sonraki Adımlar

1. ✅ Veritabanı kontrolleri yapıldı - BAŞARILI
2. ⏳ Railway Matrix Synapse loglarını kontrol et
3. ⏳ Matrix Synapse'i yeniden başlat
4. ⏳ Element Web'de login dene
5. ⏳ Matrix Synapse API'yi test et

