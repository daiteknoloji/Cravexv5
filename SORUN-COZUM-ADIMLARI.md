# Synapse Server Name Sorunu - Detaylı Çözüm

## 🔍 Durum Analizi

SQL sorgusu sonucu gösteriyor ki:
- ✅ Tüm kullanıcılar `cravex1-production.up.railway.app` domain'inde
- ❌ Ama Synapse hala "Found users in database not native to cravex1-production.up.railway.app!" hatası veriyor

Bu durum, Synapse'in **sadece `users` tablosuna bakmadığını**, başka tablolarda da domain kontrolü yaptığını gösteriyor.

## 🔎 Adım 1: Tüm Tablolarda Domain Kontrolü

Railway PostgreSQL'de şu sorguyu çalıştırın:

```sql
-- 1. Local_current_membership tablosu (oda üyelikleri)
SELECT 'local_current_membership' as tablo, split_part(user_id, ':', 2) as domain, COUNT(*) as sayi
FROM local_current_membership
GROUP BY split_part(user_id, ':', 2);

-- 2. Room_memberships tablosu
SELECT 'room_memberships' as tablo, split_part(user_id, ':', 2) as domain, COUNT(*) as sayi
FROM room_memberships
GROUP BY split_part(user_id, ':', 2);

-- 3. Profiles tablosu
SELECT 'profiles' as tablo, split_part(full_user_id, ':', 2) as domain, COUNT(*) as sayi
FROM profiles
GROUP BY split_part(full_user_id, ':', 2);

-- 4. User_directory tablosu
SELECT 'user_directory' as tablo, split_part(user_id, ':', 2) as domain, COUNT(*) as sayi
FROM user_directory
GROUP BY split_part(user_id, ':', 2);
```

## 🛠️ Adım 2: Eski Domain Referanslarını Bul

Eğer yukarıdaki sorgularda `matrix-synapse-production.up.railway.app` veya başka bir domain görürseniz:

```sql
-- Local_current_membership'ten eski domain'i temizle
DELETE FROM local_current_membership 
WHERE split_part(user_id, ':', 2) = 'matrix-synapse-production.up.railway.app';

-- Room_memberships'ten eski domain'i temizle
DELETE FROM room_memberships 
WHERE split_part(user_id, ':', 2) = 'matrix-synapse-production.up.railway.app';

-- Profiles'ten eski domain'i temizle
DELETE FROM profiles 
WHERE split_part(full_user_id, ':', 2) = 'matrix-synapse-production.up.railway.app';

-- User_directory'den eski domain'i temizle
DELETE FROM user_directory 
WHERE split_part(user_id, ':', 2) = 'matrix-synapse-production.up.railway.app';
```

## 💡 Alternatif Çözüm: Veritabanını Tamamen Temizle

Eğer yukarıdaki adımlar işe yaramazsa, Synapse veritabanını tamamen temizleyip yeniden başlatabilirsiniz:

```sql
-- DİKKAT: Bu işlem TÜM VERİLERİ SİLECEKTİR!
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

Sonra Synapse servisini yeniden başlatın. Synapse otomatik olarak şemayı yeniden oluşturacak.

## 🚀 Önerilen Sıra

1. **Önce** yukarıdaki domain kontrol sorgularını çalıştırın
2. **Sonuçları** paylaşın - hangi tablolarda eski domain var görelim
3. **Ona göre** temizleme işlemini yapalım

## ⚠️ ÖNEMLİ UYARI

- Veritabanı işlemlerinden önce **mutlaka yedek alın**
- DELETE komutlarını çalıştırmadan önce SELECT ile kontrol edin
- Railway'de veritabanı yedeği almak için Railway Dashboard → PostgreSQL → Settings → Backups


