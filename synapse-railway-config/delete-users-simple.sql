-- KULLANICI SİLME SQL SORGULARI
-- Railway PostgreSQL Query sekmesinde çalıştırın

-- ============================================
-- ÖNCE KONTROL EDİN: Hangi kullanıcılar var?
-- ============================================

-- Tüm kullanıcıları listele
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY domain, name;

-- Domain bazında kullanıcı sayısı
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;

-- ============================================
-- SEÇENEK 1: TÜM KULLANICILARI SİL
-- ============================================
-- ⚠️ DİKKAT: Bu işlem TÜM kullanıcıları silecek!

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

-- DOĞRULAMA
SELECT COUNT(*) as kalan_kullanici_sayisi FROM users;
-- Sonuç 0 olmalı!

-- ============================================
-- SEÇENEK 2: BELİRLİ DOMAIN'DEKİ KULLANICILARI SİL
-- ============================================
-- ⚠️ NOT: Aşağıdaki örneklerde eski domain (cravexv5-production.up.railway.app) kullanılmıştır
-- Güncel domain: matrix-synapse.up.railway.app
-- Örnek: matrix-synapse.up.railway.app domain'indeki kullanıcıları silmek için

-- ÖNCE KONTROL EDİN:
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE split_part(name, ':', 2) = 'matrix-synapse.up.railway.app'  -- ⚠️ Domain'i güncelleyin!
ORDER BY name;

-- SİLME İŞLEMİ (Domain adını değiştirin):
DELETE FROM local_current_membership
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

DELETE FROM room_memberships
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

DELETE FROM user_directory
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

DELETE FROM profiles
WHERE user_id LIKE '%:matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

DELETE FROM users
WHERE split_part(name, ':', 2) = 'matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!

-- DOĞRULAMA
SELECT COUNT(*) as kalan_kullanici_sayisi
FROM users
WHERE split_part(name, ':', 2) = 'matrix-synapse.up.railway.app';  -- ⚠️ Domain'i güncelleyin!
-- Sonuç 0 olmalı!

-- ============================================
-- SEÇENEK 3: BELİRLİ KULLANICILARI SİL (ID ile)
-- ============================================
-- Örnek: @1canli:matrix-synapse.up.railway.app kullanıcısını silmek için

-- ÖNCE KONTROL EDİN:
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
WHERE name IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'   -- ⚠️ Domain'i güncelleyin!
)
ORDER BY name;

-- SİLME İŞLEMİ (Kullanıcı ID'lerini değiştirin):
DELETE FROM local_current_membership
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

DELETE FROM room_memberships
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

DELETE FROM user_directory
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

DELETE FROM profiles
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

DELETE FROM users
WHERE name IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

-- DOĞRULAMA
SELECT name as kalan_kullanici
FROM users
WHERE name IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);
-- Sonuç boş olmalı!

-- ============================================
-- SEÇENEK 4: localhost DOMAIN'İNDEKİ KULLANICILARI SİL
-- ============================================

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

-- DOĞRULAMA
SELECT COUNT(*) as kalan_kullanici_sayisi
FROM users
WHERE split_part(name, ':', 2) = 'localhost';
-- Sonuç 0 olmalı!


