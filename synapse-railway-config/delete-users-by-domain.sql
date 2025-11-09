-- Belirli bir domain'deki tüm kullanıcıları sil
-- DİKKAT: Bu işlem GERİ ALINAMAZ!

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

-- DOĞRULAMA: Kullanıcılar silindi mi?
SELECT COUNT(*) as kalan_kullanici_sayisi
FROM users
WHERE split_part(name, ':', 2) = 'cravexv5-production.up.railway.app';
-- Sonuç 0 olmalı!


