# Railway GUI'den Kullanıcıları Silme

## 🔍 Railway PostgreSQL Query Sekmesinden Kullanıcı Silme

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesine gidin.

## ⚠️ DİKKAT

- Bu işlem **GERİ ALINAMAZ!**
- Kullanıcıları silmeden önce **mutlaka kontrol sorgusu çalıştırın**
- Synapse'i durdurun (kullanıcı silme işlemi sırasında)

## 📋 Seçenek 1: Belirli Domain'deki Tüm Kullanıcıları Sil

### Adım 1: Önce Kontrol Edin

```sql
-- Hangi kullanıcılar silinecek?
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app'
ORDER BY name;
```

Bu sorgu size `cravexv5-production.up.railway.app` domain'indeki tüm kullanıcıları gösterecek.

### Adım 2: Kullanıcıları Sil

**ÖNEMLİ:** Synapse'i durdurun!

```sql
-- 1. Önce kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

-- 2. Room memberships'i sil
DELETE FROM room_memberships
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

-- 3. User directory'den sil
DELETE FROM user_directory
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

-- 4. Profiles'den sil
DELETE FROM profiles
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

-- 5. Son olarak users tablosundan sil
DELETE FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app';
```

### Adım 3: Doğrulama

```sql
-- Kullanıcılar silindi mi?
SELECT COUNT(*) as kalan_kullanici_sayisi
FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app';
```

**Sonuç `0` olmalı!**

## 📋 Seçenek 2: Belirli Kullanıcıları Sil (ID ile)

### Adım 1: Önce Kontrol Edin

```sql
-- Hangi kullanıcılar silinecek?
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE name IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
)
ORDER BY name;
```

### Adım 2: Kullanıcıları Sil

**ÖNEMLİ:** Synapse'i durdurun!

```sql
-- 1. Önce kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
);

-- 2. Room memberships'i sil
DELETE FROM room_memberships
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
);

-- 3. User directory'den sil
DELETE FROM user_directory
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
);

-- 4. Profiles'den sil
DELETE FROM profiles
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
);

-- 5. Son olarak users tablosundan sil
DELETE FROM users
WHERE name IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
);
```

### Adım 3: Doğrulama

```sql
-- Kullanıcılar silindi mi?
SELECT name as kalan_kullanici
FROM users
WHERE name IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app',
    '@zohan:cravexv5-production.up.railway.app',
    '@stark:cravexv5-production.up.railway.app'
);
```

**Sonuç boş olmalı!**

## 📋 Seçenek 3: Sadece localhost Domain'indeki Kullanıcıları Sil

```sql
-- localhost domain'indeki kullanıcıları sil
DELETE FROM local_current_membership
WHERE user_id LIKE '%:localhost';

DELETE FROM room_memberships
WHERE user_id LIKE '%:localhost';

DELETE FROM user_directory
WHERE user_id LIKE '%:localhost';

DELETE FROM profiles
WHERE user_id LIKE '%:localhost';

DELETE FROM users
WHERE split_part(name, ':', 2) = 'localhost';
```

## 🚀 Sonraki Adımlar

1. Kullanıcıları sildikten sonra Synapse'i yeniden başlatın
2. Logları kontrol edin - crash hatası olmamalı
3. `SYNAPSE_SERVER_NAME` environment variable'ını doğru domain'e ayarlayın

## ⚠️ ÖNEMLİ UYARILAR

1. **Synapse'i durdurun** - Kullanıcı silme işlemi sırasında Synapse çalışmamalı
2. **Backup alın** - Önemli verileriniz varsa önce yedekleyin
3. **Kontrol sorgusu çalıştırın** - Silmeden önce mutlaka kontrol edin
4. **Doğrulama yapın** - Silme işleminden sonra doğrulama sorgusu çalıştırın

## 📝 Notlar

- Kullanıcıları silmek için birden fazla tablodan veri silmeniz gerekir
- Sadece `users` tablosundan silmek yeterli değil, ilişkili tablolardan da silmelisiniz
- Synapse başladığında veritabanı tutarlılığını kontrol eder


