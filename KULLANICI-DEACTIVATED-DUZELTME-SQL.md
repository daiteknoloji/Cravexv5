# 🔧 Kullanıcı Deactivated Durumu Düzeltme SQL

## ❌ Hata

```
ERROR: column "deactivated" is of type smallint but expression is of type boolean
LINE 3: SET deactivated = false
```

## ✅ Çözüm

PostgreSQL'de `deactivated` sütunu `smallint` tipinde. `false` yerine `0`, `true` yerine `1` kullanılmalı.

### Doğru SQL Sorguları:

```sql
-- Kullanıcının deactivated durumunu kontrol et
SELECT 
    name,
    deactivated,
    is_guest,
    admin,
    LEFT(password_hash, 30) as hash_start,
    LENGTH(password_hash) as hash_length,
    creation_ts
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Eğer deactivated = 1 ise, 0 yap (false yap)
UPDATE users 
SET deactivated = 0 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Tüm deactivated kullanıcıları kontrol et
SELECT 
    name,
    deactivated,
    CASE 
        WHEN deactivated = 0 THEN 'Aktif'
        WHEN deactivated = 1 THEN 'Pasif'
        ELSE 'Bilinmiyor'
    END as durum
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';
```

## 📋 Deactivated Değerleri

- `0` = Aktif (false)
- `1` = Pasif (true)
- `NULL` = Belirtilmemiş

## 🔍 Tüm Kullanıcıları Kontrol Et

```sql
-- Tüm kullanıcıların deactivated durumunu kontrol et
SELECT 
    name,
    deactivated,
    CASE 
        WHEN deactivated = 0 THEN 'Aktif'
        WHEN deactivated = 1 THEN 'Pasif'
        ELSE 'Bilinmiyor'
    END as durum,
    LEFT(password_hash, 30) as hash_start
FROM users 
ORDER BY name;
```

## ⚠️ Önemli Notlar

1. PostgreSQL'de `smallint` tipi için:
   - `false` → `0`
   - `true` → `1`

2. Kodda zaten `deactivated = 0` olarak ayarlanıyor, bu doğru.

3. Eğer kullanıcı deactivated durumda ise (`deactivated = 1`), login çalışmaz.

4. Kullanıcıyı aktif yapmak için:
   ```sql
   UPDATE users 
   SET deactivated = 0 
   WHERE name = '@testuser:matrix-synapse.up.railway.app';
   ```

