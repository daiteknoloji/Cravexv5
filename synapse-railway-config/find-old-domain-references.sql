-- Eski domain (matrix-synapse-production.up.railway.app) referanslarını bul
-- Synapse'in server_name kontrolü bu tablolara bakıyor olabilir

-- 1. Users tablosunda eski domain
SELECT 'users' as tablo, name as kullanici_id
FROM users
WHERE split_part(name, ':', 2) != 'cravex1-production.up.railway.app';

-- 2. Local_current_membership tablosunda eski domain
SELECT 'local_current_membership' as tablo, user_id
FROM local_current_membership
WHERE split_part(user_id, ':', 2) != 'cravex1-production.up.railway.app'
LIMIT 20;

-- 3. Room_memberships tablosunda eski domain
SELECT 'room_memberships' as tablo, user_id
FROM room_memberships
WHERE split_part(user_id, ':', 2) != 'cravex1-production.up.railway.app'
LIMIT 20;

-- 4. Profiles tablosunda eski domain
SELECT 'profiles' as tablo, full_user_id
FROM profiles
WHERE split_part(full_user_id, ':', 2) != 'cravex1-production.up.railway.app'
LIMIT 20;

-- 5. User_directory tablosunda eski domain
SELECT 'user_directory' as tablo, user_id
FROM user_directory
WHERE split_part(user_id, ':', 2) != 'cravex1-production.up.railway.app'
LIMIT 20;

-- 6. "matrix-synapse-production" içeren tüm kayıtlar (herhangi bir tabloda)
-- Bu sorgu çalışmayabilir, ama deneyin:
SELECT 'GENEL_ARAMA' as tablo, 'matrix-synapse-production.up.railway.app bulundu' as sonuc
WHERE EXISTS (
    SELECT 1 FROM users WHERE name LIKE '%matrix-synapse-production.up.railway.app%'
    UNION ALL
    SELECT 1 FROM local_current_membership WHERE user_id LIKE '%matrix-synapse-production.up.railway.app%'
    UNION ALL
    SELECT 1 FROM room_memberships WHERE user_id LIKE '%matrix-synapse-production.up.railway.app%'
);


