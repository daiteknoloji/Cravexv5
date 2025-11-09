# Kullanıcı Silme Hızlı Rehber

## ✅ Hazırlık

- ✅ Synapse durduruldu
- ✅ PostgreSQL çalışıyor (doğru!)
- ✅ Railway Dashboard → Cravexv5 → Postgres → Query sekmesi açık

## 📋 Adım Adım

### 1. Önce Kontrol Edin

Railway PostgreSQL Query sekmesinde şu sorguyu çalıştırın:

```sql
-- Tüm kullanıcıları listele
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY domain, name;
```

Bu sorgu size hangi kullanıcıların olduğunu gösterecek.

### 2. Domain Bazında Kontrol

```sql
-- Domain bazında kullanıcı sayısı
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

### 3. Kullanıcıları Silin

Aşağıdaki seçeneklerden birini seçin:

#### SEÇENEK A: Tüm Kullanıcıları Sil

```sql
DELETE FROM local_current_membership;
DELETE FROM room_memberships;
DELETE FROM user_directory;
DELETE FROM profiles;
DELETE FROM users;
```

#### SEÇENEK B: Belirli Domain'deki Kullanıcıları Sil

Örnek: `cravexv5-production.up.railway.app` domain'indeki kullanıcıları silmek için:

```sql
DELETE FROM local_current_membership
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

DELETE FROM room_memberships
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

DELETE FROM user_directory
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

DELETE FROM profiles
WHERE user_id LIKE '%:cravexv5-production.up.railway.app';

DELETE FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app';
```

#### SEÇENEK C: Belirli Kullanıcıları Sil

Örnek: `@1canli:cravexv5-production.up.railway.app` kullanıcısını silmek için:

```sql
DELETE FROM local_current_membership
WHERE user_id = '@1canli:cravexv5-production.up.railway.app';

DELETE FROM room_memberships
WHERE user_id = '@1canli:cravexv5-production.up.railway.app';

DELETE FROM user_directory
WHERE user_id = '@1canli:cravexv5-production.up.railway.app';

DELETE FROM profiles
WHERE user_id = '@1canli:cravexv5-production.up.railway.app';

DELETE FROM users
WHERE name = '@1canli:cravexv5-production.up.railway.app';
```

### 4. Doğrulama

```sql
SELECT COUNT(*) as kalan_kullanici_sayisi FROM users;
```

Sonuç `0` olmalı (eğer tüm kullanıcıları sildiyseniz) veya beklediğiniz sayı olmalı.

### 5. Synapse'i Yeniden Başlatın

1. Railway Dashboard → Cravexv5 → Synapse servisi
2. **"Deploy"** butonuna tıklayın
3. Logları kontrol edin - crash hatası olmamalı

## ⚠️ ÖNEMLİ

- SQL sorgularını **SIRASIYLA** çalıştırın (1, 2, 3, 4, 5)
- Her sorgudan sonra **"Run Query"** butonuna tıklayın
- Doğrulama sorgusunu mutlaka çalıştırın

## 📝 Notlar

- PostgreSQL çalışırken kullanıcıları silebilirsiniz (doğru yaptınız!)
- Synapse durmuş olmalı (doğru yaptınız!)
- Kullanıcıları sildikten sonra Synapse'i yeniden başlatın

er a
