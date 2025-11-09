# 🔍 Matrix Synapse Login Kontrol Rehberi

## 📋 Sorun Analizi

Kullanıcı başarıyla oluşturuluyor ve password hash doğru görünüyor ama Matrix Synapse login'i reddediyor (403 Forbidden).

### ✅ Başarılı İşlemler:
- Kullanıcı `users` tablosuna yazıldı
- Password hash doğru format (`$2b$12$...`)
- Password verification PASSED (`bcrypt.checkpw`)
- `profiles` tablosuna yazıldı
- `user_directory` tablosuna yazıldı
- `user_directory_search` tablosuna yazıldı
- Tüm değişiklikler commit edildi

### ❌ Sorun:
- Matrix Synapse login'i reddediyor (403 Forbidden)
- Element Web'de login çalışmıyor

---

## 🔧 Olası Nedenler ve Çözümler

### 1. Matrix Synapse Cache Sorunu

**Sorun:** Matrix Synapse cache'i güncel değil olabilir.

**Çözüm:**
```bash
# Railway'de Matrix Synapse servisini yeniden başlat
# Railway Dashboard → Matrix Synapse → Restart
```

---

### 2. Matrix Synapse'in Beklediği Tablolar Eksik Olabilir

**Kontrol:**
```sql
-- Kullanıcının tüm tablolarda olup olmadığını kontrol et
SELECT 'users' as table_name, COUNT(*) as count FROM users WHERE name = '@testuser:matrix-synapse.up.railway.app'
UNION ALL
SELECT 'profiles', COUNT(*) FROM profiles WHERE user_id = '@testuser:matrix-synapse.up.railway.app'
UNION ALL
SELECT 'user_directory', COUNT(*) FROM user_directory WHERE user_id = '@testuser:matrix-synapse.up.railway.app'
UNION ALL
SELECT 'user_directory_search', COUNT(*) FROM user_directory_search WHERE user_id = '@testuser:matrix-synapse.up.railway.app';

-- Mevcut çalışan bir kullanıcıyla karşılaştır
SELECT 'users' as table_name, COUNT(*) as count FROM users WHERE name LIKE '@admin:%'
UNION ALL
SELECT 'profiles', COUNT(*) FROM profiles WHERE user_id LIKE '@admin:%'
UNION ALL
SELECT 'user_directory', COUNT(*) FROM user_directory WHERE user_id LIKE '@admin:%'
UNION ALL
SELECT 'user_directory_search', COUNT(*) FROM user_directory_search WHERE user_id LIKE '@admin:%';
```

---

### 3. Password Hash Formatı Sorunu

**Kontrol:**
```sql
-- Yeni kullanıcının password hash formatını kontrol et
SELECT 
    name,
    LEFT(password_hash, 30) as hash_start,
    LENGTH(password_hash) as hash_length,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    deactivated,
    is_guest,
    admin
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Mevcut çalışan bir kullanıcıyla karşılaştır
SELECT 
    name,
    LEFT(password_hash, 30) as hash_start,
    LENGTH(password_hash) as hash_length,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format,
    deactivated,
    is_guest,
    admin
FROM users 
WHERE name LIKE '@admin:%' 
LIMIT 1;
```

---

### 4. Matrix Synapse Loglarını Kontrol Et

**Railway Matrix Synapse Loglarında şunları ara:**
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
```

**Örnek log:**
```
2025-11-09T21:18:18.506274268Z [inf] POST /_matrix/client/v3/login
2025-11-09T21:18:18.506274268Z [err] M_FORBIDDEN: Invalid username or password
```

---

### 5. Kullanıcı Deactivated Durumda Olabilir

**Kontrol:**
```sql
-- Kullanıcının deactivated durumunu kontrol et
SELECT 
    name,
    deactivated,
    is_guest,
    admin,
    creation_ts
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Eğer deactivated = true ise, false yap
UPDATE users 
SET deactivated = false 
WHERE name = '@testuser:matrix-synapse.up.railway.app';
```

---

### 6. Matrix Synapse'in Beklediği Başka Tablolar Olabilir

**Kontrol:**
```sql
-- Matrix Synapse'in beklediği diğer tabloları kontrol et
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%user%' 
ORDER BY table_name;

-- Örnek tablolar:
-- - user_ips
-- - user_threepids
-- - user_filters
-- - user_stats_historical
-- vb.
```

---

## 🎯 Hızlı Test Senaryosu

1. **Yeni kullanıcı oluştur:**
   - Username: `testuser`
   - Password: `12345678`

2. **Veritabanını kontrol et:**
   ```sql
   SELECT 
       name,
       LEFT(password_hash, 30) as hash_start,
       deactivated,
       is_guest
   FROM users 
   WHERE name = '@testuser:matrix-synapse.up.railway.app';
   ```

3. **Matrix Synapse'i yeniden başlat:**
   - Railway Dashboard → Matrix Synapse → Restart

4. **Login dene:**
   - Element Web'de login yap
   - Railway Matrix Synapse loglarını kontrol et

---

## 📝 Gerekli Loglar

### Railway Admin Panel Logları:
```
[INFO] Creating user @testuser:matrix-synapse.up.railway.app in database...
[INFO] User @testuser:matrix-synapse.up.railway.app inserted into users table
[INFO] Profile created/updated for @testuser:matrix-synapse.up.railway.app
[INFO] User @testuser:matrix-synapse.up.railway.app added to user_directory
[INFO] User @testuser:matrix-synapse.up.railway.app added to user_directory_search
[INFO] All database changes committed successfully!
[DEBUG] Password verification test (bcrypt.checkpw) with DB hash: True
[INFO] Password hash verification PASSED! Login should work!
```

### Railway Matrix Synapse Logları:
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
```

### Element Web Console Logları:
```
POST https://matrix-synapse.up.railway.app/_matrix/client/v3/login 403 (Forbidden)
```

---

## ⚠️ Önemli Notlar

1. **Password hash doğru görünüyor** ama Matrix Synapse login'i kabul etmiyor
2. **Tüm tablolara yazıldı** ama Matrix Synapse kullanıcıyı tanımıyor olabilir
3. **Matrix Synapse cache'i güncel olmayabilir** - yeniden başlatmayı deneyin
4. **Matrix Synapse'in beklediği başka tablolar olabilir** - kontrol edin

---

## 🔧 Sonraki Adımlar

1. ✅ Railway Admin Panel loglarını kontrol ettik - BAŞARILI
2. ⏳ Veritabanı sorgularını çalıştırın
3. ⏳ Railway Matrix Synapse loglarını kontrol edin
4. ⏳ Matrix Synapse'i yeniden başlatın
5. ⏳ Element Web'de login deneyin

