-- Synapse'in server_name kontrolü sadece users tablosuna bakmıyor
-- Diğer tablolarda da domain referansları olabilir
-- Bu sorgular tüm olası domain referanslarını bulur

-- 1. Users tablosu (zaten kontrol ettik, ama tekrar)
SELECT 'users' as tablo, split_part(name, ':', 2) as domain, COUNT(*) as sayi
FROM users
GROUP BY split_part(name, ':', 2);

-- 2. Local_current_membership tablosu (oda üyelikleri)
SELECT 'local_current_membership' as tablo, split_part(user_id, ':', 2) as domain, COUNT(*) as sayi
FROM local_current_membership
GROUP BY split_part(user_id, ':', 2);

-- 3. Room_memberships tablosu
SELECT 'room_memberships' as tablo, split_part(user_id, ':', 2) as domain, COUNT(*) as sayi
FROM room_memberships
GROUP BY split_part(user_id, ':', 2);

-- 4. Profiles tablosu
SELECT 'profiles' as tablo, split_part(full_user_id, ':', 2) as domain, COUNT(*) as sayi
FROM profiles
GROUP BY split_part(full_user_id, ':', 2);

-- 5. User_directory tablosu
SELECT 'user_directory' as tablo, split_part(user_id, ':', 2) as domain, COUNT(*) as sayi
FROM user_directory
GROUP BY split_part(user_id, ':', 2);

-- 6. Event_auth tablosu (event'lerde domain referansları)
SELECT 'event_auth' as tablo, split_part(event_id, ':', 1) as domain, COUNT(*) as sayi
FROM event_auth
WHERE event_id LIKE '%:%'
GROUP BY split_part(event_id, ':', 1)
LIMIT 10;

-- 7. Tüm tablolarda "matrix-synapse-production" araması
SELECT 'TUM_TABLOLAR' as tablo, 'matrix-synapse-production.up.railway.app' as domain, 
       (SELECT COUNT(*) FROM users WHERE name LIKE '%matrix-synapse-production.up.railway.app%') +
       (SELECT COUNT(*) FROM local_current_membership WHERE user_id LIKE '%matrix-synapse-production.up.railway.app%') +
       (SELECT COUNT(*) FROM room_memberships WHERE user_id LIKE '%matrix-synapse-production.up.railway.app%') as toplam_sayi;


