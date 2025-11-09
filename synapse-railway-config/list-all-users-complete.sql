-- Tüm kullanıcıları detaylı listele
-- Railway PostgreSQL Query sekmesinde çalıştırın

-- 1. Tüm kullanıcılar ve domain'leri
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

-- 2. Domain bazında kullanıcı sayısı
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi,
    COUNT(*) FILTER (WHERE admin = 1) as admin_sayisi,
    COUNT(*) FILTER (WHERE deactivated = 1) as deaktif_sayisi,
    COUNT(*) FILTER (WHERE is_guest = 1) as guest_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;

-- 3. Sadece aktif kullanıcılar
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    TO_TIMESTAMP(creation_ts) as olusturma_tarihi
FROM users
WHERE deactivated = 0
ORDER BY domain, name;

-- 4. Sadece admin kullanıcılar
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    TO_TIMESTAMP(creation_ts) as olusturma_tarihi
FROM users
WHERE admin = 1
ORDER BY domain, name;


