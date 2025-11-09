# 🔧 SYNAPSE DOMAIN DEĞİŞTİRME - SQL ÇÖZÜMÜ

## ⚠️ SORUN

Synapse başlamıyor çünkü:
- Veritabanında eski domain (`cravexv5-production.up.railway.app`) ile kullanıcılar var
- Yeni domain (`matrix-synapse.up.railway.app`) ile başlatmaya çalışıyoruz
- Synapse domain değişikliğine izin vermiyor!

**Hata:**
```
Exception: Found users in database not native to matrix-synapse.up.railway.app!
You cannot change a synapse server_name after it's been configured
```

---

## ✅ ÇÖZÜM: SQL İLE DOMAIN GÜNCELLEME

### Adım 1: Veritabanında Hangi Kullanıcılar Var?

Railway Dashboard → PostgreSQL → **Query** sekmesinde:

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY creation_ts DESC;
```

Bu sorgu hangi domain'lerin kullanıldığını gösterecek.

### Adım 2: Eski Domain'i Yeni Domain ile Değiştir

**⚠️ ÖNEMLİ:** Önce backup alın!

Railway Dashboard → PostgreSQL → **Query** sekmesinde:

```sql
-- ÖNCE KONTROL ET: Kaç kullanıcı etkilenecek?
SELECT COUNT(*) as etkilenen_kullanici_sayisi
FROM users
WHERE name LIKE '%cravexv5-production.up.railway.app';

-- Eğer sayı makul görünüyorsa, güncelle:
UPDATE users 
SET name = REPLACE(name, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%cravexv5-production.up.railway.app';

-- Diğer tablolarda da güncelle (gerekirse):
UPDATE profiles 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app'),
    full_user_id = REPLACE(full_user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory_search 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE access_tokens 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';
```

### Adım 3: Doğrulama

```sql
-- Yeni domain ile kullanıcıları kontrol et:
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
WHERE name LIKE '%matrix-synapse.up.railway.app'
ORDER BY creation_ts DESC;

-- Eski domain kaldı mı kontrol et:
SELECT COUNT(*) as eski_domain_kalan
FROM users
WHERE name LIKE '%cravexv5-production.up.railway.app';
```

**Beklenen:** `eski_domain_kalan` = `0`

### Adım 4: Synapse'i Yeniden Başlat

Railway Dashboard → Synapse servisi → **Deployments** → **Redeploy**

---

## 📋 TAM SQL SCRIPT (Kopyala-Yapıştır)

Railway Dashboard → PostgreSQL → **Query** sekmesinde çalıştırın:

```sql
-- 1. ÖNCE KONTROL ET
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain,
    COUNT(*) OVER() as toplam_kullanici
FROM users
WHERE name LIKE '%cravexv5-production.up.railway.app';

-- 2. EĞER SONUÇLAR DOĞRUYSA, GÜNCELLE:
BEGIN;

UPDATE users 
SET name = REPLACE(name, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%cravexv5-production.up.railway.app';

UPDATE profiles 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app'),
    full_user_id = REPLACE(full_user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE user_directory_search 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

UPDATE access_tokens 
SET user_id = REPLACE(user_id, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE user_id LIKE '%cravexv5-production.up.railway.app';

-- 3. DOĞRULAMA
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY creation_ts DESC
LIMIT 10;

-- 4. EĞER HER ŞEY DOĞRUYSA:
COMMIT;
-- EĞER BİR SORUN VARSA:
-- ROLLBACK;
```

---

## ⚠️ ÖNEMLİ NOTLAR

### Transaction Kullanın!
- `BEGIN;` ile başlayın
- `COMMIT;` ile bitirin
- Sorun olursa `ROLLBACK;` ile geri alın

### Backup Alın!
- Railway Dashboard → PostgreSQL → **Backups** → **Create Backup**
- Veya SQL export yapın

### Hangi Tablolar Güncellenmeli?

1. ✅ `users` - Kullanıcı bilgileri (ZORUNLU)
2. ✅ `profiles` - Kullanıcı profilleri (ZORUNLU)
3. ✅ `user_directory` - Kullanıcı dizini (ZORUNLU)
4. ✅ `user_directory_search` - Arama dizini (ZORUNLU)
5. ✅ `access_tokens` - Access token'lar (Önerilir)

---

## 🎯 ADIM ADIM

1. **Railway Dashboard → PostgreSQL → Query**
2. **İlk sorguyu çalıştırın** (kontrol)
3. **Sonuçları kontrol edin**
4. **Transaction başlatın** (`BEGIN;`)
5. **UPDATE sorgularını çalıştırın**
6. **Doğrulama sorgusunu çalıştırın**
7. **Her şey doğruysa:** `COMMIT;`
8. **Sorun varsa:** `ROLLBACK;`
9. **Synapse'i redeploy edin**

---

## ✅ BAŞARILI SONUÇ

SQL güncellemesinden sonra:
- ✅ Tüm kullanıcılar `@user:matrix-synapse.up.railway.app` formatında olmalı
- ✅ Synapse başlamalı
- ✅ Element Web'de login çalışmalı

---

**SONUÇ:** SQL ile domain güncellemesi yapın, sonra Synapse'i redeploy edin!


