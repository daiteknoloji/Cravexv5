# Railway PostgreSQL'den Kullanıcı Silme Rehberi

## 🔍 Railway PostgreSQL'e Nasıl Bağlanılır?

### Yöntem 1: Railway Dashboard Query Sekmesi (EN KOLAY)

1. **Railway Dashboard** → **Cravexv5** projesine gidin
2. **Postgres** servisini seçin
3. **"Query"** sekmesine tıklayın
4. SQL sorgularını buraya yapıştırıp çalıştırın

### Yöntem 2: Railway CLI

```bash
railway connect postgres
```

## 📋 Kullanıcı Silme Yöntemleri

### Yöntem 1: Tüm Kullanıcıları Sil

**⚠️ DİKKAT: Bu işlem TÜM kullanıcıları silecek!**

```sql
-- 1. Önce TÜM kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership;

-- 2. TÜM room memberships'i sil
DELETE FROM room_memberships;

-- 3. TÜM user directory'den sil
DELETE FROM user_directory;

-- 4. TÜM profiles'den sil
DELETE FROM profiles;

-- 5. Son olarak TÜM users tablosundan sil
DELETE FROM users;
```

**Doğrulama:**
```sql
SELECT COUNT(*) as kalan_kullanici_sayisi FROM users;
-- Sonuç 0 olmalı!
```

### Yöntem 2: Belirli Domain'deki Tüm Kullanıcıları Sil

Örnek: `cravexv5-production.up.railway.app` domain'indeki tüm kullanıcıları silmek için:

```sql
-- ÖNCE KONTROL EDİN: Hangi kullanıcılar silinecek?
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app'
ORDER BY name;

-- EĞER SONUÇLAR DOĞRUYSA, AŞAĞIDAKİ SİLME İŞLEMİNİ ÇALIŞTIRIN:

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

**Doğrulama:**
```sql
SELECT COUNT(*) as kalan_kullanici_sayisi
FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app';
-- Sonuç 0 olmalı!
```

### Yöntem 3: Belirli Kullanıcıları Sil (ID ile)

Örnek: `@1canli:cravexv5-production.up.railway.app` kullanıcısını silmek için:

```sql
-- ÖNCE KONTROL EDİN: Hangi kullanıcılar silinecek?
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE name IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
)
ORDER BY name;

-- EĞER SONUÇLAR DOĞRUYSA, AŞAĞIDAKİ SİLME İŞLEMİNİ ÇALIŞTIRIN:

-- 1. Önce kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
);

-- 2. Room memberships'i sil
DELETE FROM room_memberships
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
);

-- 3. User directory'den sil
DELETE FROM user_directory
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
);

-- 4. Profiles'den sil
DELETE FROM profiles
WHERE user_id IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
);

-- 5. Son olarak users tablosundan sil
DELETE FROM users
WHERE name IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
);
```

**Doğrulama:**
```sql
SELECT name as kalan_kullanici
FROM users
WHERE name IN (
    '@1canli:cravexv5-production.up.railway.app',
    '@2canli:cravexv5-production.up.railway.app'
);
-- Sonuç boş olmalı!
```

### Yöntem 4: localhost Domain'indeki Kullanıcıları Sil

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

## 🔍 Kullanıcıları Listeleme

### Tüm Kullanıcıları Listele

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    creation_ts,
    TO_TIMESTAMP(creation_ts) as olusturma_tarihi,
    admin,
    deactivated,
    is_guest
FROM users
ORDER BY domain, name;
```

### Domain Bazında Kullanıcı Sayısı

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

## ⚠️ ÖNEMLİ UYARILAR

1. **Synapse'i Durdurun:** Kullanıcı silme işlemi sırasında Synapse çalışmamalı!
   - Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Settings** → servisi durdurun

2. **Backup Alın:** Önemli verileriniz varsa önce yedekleyin!

3. **Kontrol Sorgusu Çalıştırın:** Silmeden önce mutlaka kontrol sorgusu çalıştırın!

4. **Doğrulama Yapın:** Silme işleminden sonra doğrulama sorgusu çalıştırın!

5. **Sıralı Silme:** SQL sorgularını **SIRASIYLA** çalıştırın (1, 2, 3, 4, 5)

## 📝 Adım Adım Örnek

### Senaryo: `cravexv5-production.up.railway.app` domain'indeki tüm kullanıcıları silmek

1. **Synapse'i durdurun**
2. **Railway Dashboard** → **Cravexv5** → **Postgres** → **Query** sekmesi
3. **Kontrol sorgusu çalıştırın:**
   ```sql
   SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
   FROM users
   GROUP BY split_part(name, ':', 2)
   ORDER BY kullanici_sayisi DESC;
   ```
4. **Silme sorgularını sırasıyla çalıştırın** (Yöntem 2'deki sorgular)
5. **Doğrulama sorgusu çalıştırın:**
   ```sql
   SELECT COUNT(*) as kalan_kullanici_sayisi
   FROM users
   WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app';
   ```
6. **Synapse'i yeniden başlatın**

## 🚀 Sonraki Adımlar

Kullanıcıları sildikten sonra:
1. Synapse'i yeniden başlatın
2. Logları kontrol edin - crash hatası olmamalı
3. Yeni kullanıcılar oluşturun


