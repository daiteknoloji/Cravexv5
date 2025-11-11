-- Belirli kullanıcıları sil (ID ile)
-- DİKKAT: Bu işlem GERİ ALINAMAZ!
-- ⚠️ NOT: Aşağıdaki örneklerde eski domain (cravexv5-production.up.railway.app) kullanılmıştır
-- Güncel domain: matrix-synapse.up.railway.app
-- Kullanıcı ID'lerini kendi domain'inizle güncelleyin!

-- ÖNCE KONTROL EDİN: Hangi kullanıcılar silinecek?
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

-- EĞER SONUÇLAR DOĞRUYSA, AŞAĞIDAKİ SİLME İŞLEMİNİ ÇALIŞTIRIN:

-- 1. Önce kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

-- 2. Room memberships'i sil
DELETE FROM room_memberships
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

-- 3. User directory'den sil
DELETE FROM user_directory
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

-- 4. Profiles'den sil
DELETE FROM profiles
WHERE user_id IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

-- 5. Son olarak users tablosundan sil
DELETE FROM users
WHERE name IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);

-- DOĞRULAMA: Kullanıcılar silindi mi?
SELECT name as kalan_kullanici
FROM users
WHERE name IN (
    '@1canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@2canli:matrix-synapse.up.railway.app',  -- ⚠️ Domain'i güncelleyin!
    '@zohan:matrix-synapse.up.railway.app',   -- ⚠️ Domain'i güncelleyin!
    '@stark:matrix-synapse.up.railway.app'    -- ⚠️ Domain'i güncelleyin!
);
-- Sonuç boş olmalı!


