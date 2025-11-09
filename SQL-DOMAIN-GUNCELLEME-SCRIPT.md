# 🔧 SQL DOMAIN GÜNCELLEME SCRIPT

## 📊 MEVCUT DURUM

Veritabanında 3 farklı domain var:
- ❌ `cravexv5-production.up.railway.app` (eski domain)
- ❌ `localhost` (test kullanıcıları)
- ✅ `matrix-synapse.up.railway.app` (yeni domain - doğru)

**Sorun:** Synapse başlamıyor çünkü eski domain'li kullanıcılar var!

---

## ✅ ÇÖZÜM: TÜM KULLANICILARI YENİ DOMAIN'E GÜNCELLE

Navicat'ta **Query** sekmesinde şu SQL'i çalıştırın:

### 1. ÖNCE KONTROL ET

```sql
-- Hangi domain'ler var?
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

Bu sorgu şunu gösterecek:
- `cravexv5-production.up.railway.app`: X kullanıcı
- `localhost`: Y kullanıcı
- `matrix-synapse.up.railway.app`: Z kullanıcı

### 2. TRANSACTION BAŞLAT

```sql
BEGIN;
```

### 3. USERS TABLOSUNU GÜNCELLE

```sql
-- Eski domain'i yeni domain'e çevir
UPDATE users 
SET name = REPLACE(name, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%cravexv5-production.up.railway.app';

-- Localhost domain'ini yeni domain'e çevir
UPDATE users 
SET name = REPLACE(name, 'localhost', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%localhost';
```

### 4. PROFILES TABLOSUNU GÜNCELLE

```sql
-- Profiles tablosunu güncelle
UPDATE profiles 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app'),
    full_user_id = REPLACE(full_user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE profiles 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app'),
    full_user_id = REPLACE(full_user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';
```

### 5. USER_DIRECTORY TABLOSUNU GÜNCELLE

```sql
-- User directory'yi güncelle
UPDATE user_directory 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';
```

### 6. USER_DIRECTORY_SEARCH TABLOSUNU GÜNCELLE

```sql
-- User directory search'ü güncelle
UPDATE user_directory_search 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory_search 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';
```

### 7. ACCESS_TOKENS TABLOSUNU GÜNCELLE

```sql
-- Access tokens'ı güncelle
UPDATE access_tokens 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE access_tokens 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';
```

### 8. DOĞRULAMA

```sql
-- Tüm kullanıcılar yeni domain'de mi?
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY creation_ts DESC;

-- Eski domain kaldı mı?
SELECT COUNT(*) as eski_domain_kalan
FROM users
WHERE name LIKE '%cravexv5-production.up.railway.app' 
   OR name LIKE '%localhost';
```

**Beklenen:** `eski_domain_kalan` = `0`

### 9. COMMIT VEYA ROLLBACK

```sql
-- Eğer her şey doğruysa:
COMMIT;

-- Eğer sorun varsa:
-- ROLLBACK;
```

---

## 📋 TAM SQL SCRIPT (KOPYALA-YAPIŞTIR)

Navicat'ta **Query** sekmesinde çalıştırın:

```sql
-- ============================================
-- SYNAPSE DOMAIN GÜNCELLEME SCRIPT
-- ============================================

-- 1. ÖNCE KONTROL ET
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;

-- 2. TRANSACTION BAŞLAT
BEGIN;

-- 3. USERS TABLOSUNU GÜNCELLE
UPDATE users 
SET name = REPLACE(name, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%cravexv5-production.up.railway.app';

UPDATE users 
SET name = REPLACE(name, 'localhost', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%localhost';

-- 4. PROFILES TABLOSUNU GÜNCELLE
UPDATE profiles 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app'),
    full_user_id = REPLACE(full_user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE profiles 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app'),
    full_user_id = REPLACE(full_user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';

-- 5. USER_DIRECTORY TABLOSUNU GÜNCELLE
UPDATE user_directory 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';

-- 6. USER_DIRECTORY_SEARCH TABLOSUNU GÜNCELLE
UPDATE user_directory_search 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory_search 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';

-- 7. ACCESS_TOKENS TABLOSUNU GÜNCELLE
UPDATE access_tokens 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE access_tokens 
SET user_id = REPLACE(user_id, 'localhost', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%localhost';

-- 8. DOĞRULAMA
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY creation_ts DESC;

SELECT COUNT(*) as eski_domain_kalan
FROM users
WHERE name LIKE '%cravexv5-production.up.railway.app' 
   OR name LIKE '%localhost';

-- 9. COMMIT
COMMIT;
```

---

## ✅ BAŞARILI SONUÇ

SQL güncellemesinden sonra:

1. ✅ Tüm kullanıcılar `@user:matrix-synapse.up.railway.app` formatında olmalı
2. ✅ Eski domain kalmamalı
3. ✅ Localhost domain kalmamalı
4. ✅ Synapse başlamalı
5. ✅ Element Web'de login çalışmalı

---

## 🎯 ADIM ADIM

1. ✅ Navicat'ta bağlanın
2. ✅ `railway` database'ini seçin
3. ✅ **Query** sekmesine gidin
4. ✅ Yukarıdaki SQL script'ini yapıştırın
5. ✅ **Execute** butonuna tıklayın
6. ✅ Sonuçları kontrol edin
7. ✅ Railway Dashboard → Synapse → **Redeploy**

---

**SONUÇ:** Navicat'ta SQL script'ini çalıştırın, sonra Synapse'i redeploy edin!


