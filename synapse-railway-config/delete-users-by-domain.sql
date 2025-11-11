-- Belirli bir domain'deki tüm kullanıcıları sil
-- DİKKAT: Bu işlem GERİ ALINAMAZ!
-- ⚠️ NOT: Aşağıdaki örnekte eski domain (cravexv5-production.up.railway.app) kullanılmıştır
-- Güncel domain: matrix-synapse.up.railway.app
-- Domain'i kendi domain'inizle değiştirin!

-- ÖNCE KONTROL EDİN: Hangi kullanıcılar silinecek?
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE split_part(name, ':', 2) = 'matrix-synapse.up.railway.app'  -- ⚠️ Domain'i güncelleyin!
ORDER BY name;

-- EĞER SONUÇLAR DOĞRUYSA, AŞAĞIDAKİ SİLME İŞLEMİNİ ÇALIŞTIRIN:

-- 1. Önce kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

-- 2. Room memberships'i sil
DELETE FROM room_memberships
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

-- 3. User directory'den sil
DELETE FROM user_directory
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

-- 4. Profiles'den sil
DELETE FROM profiles
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

-- 5. Son olarak users tablosundan sil
DELETE FROM users
WHERE split_part(name, ':', 2) = 'matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

-- DOĞRULAMA: Kullanıcılar silindi mi?
SELECT COUNT(*) as kalan_kullanici_sayisi
FROM users
WHERE split_part(name, ':', 2) = 'matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!
-- Sonuç 0 olmalı!


