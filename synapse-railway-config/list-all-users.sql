-- Tüm kullanıcıları domain'leriyle birlikte listele
-- Railway PostgreSQL'de çalıştırın

-- 1. Domain bazında kullanıcı sayıları
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;

-- 2. Tüm kullanıcıları domain'leriyle birlikte listele (ilk 50)
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    created_ts as olusturulma_tarihi
FROM users
ORDER BY domain, name
LIMIT 50;

-- 3. Her domain'den örnek kullanıcılar (tüm domain'ler için)
SELECT 
    split_part(name, ':', 2) as domain,
    name as kullanici_id,
    created_ts as olusturulma_tarihi
FROM (
    SELECT 
        name,
        created_ts,
        split_part(name, ':', 2) as domain,
        ROW_NUMBER() OVER (PARTITION BY split_part(name, ':', 2) ORDER BY created_ts DESC) as rn
    FROM users
) ranked
WHERE rn <= 3
ORDER BY domain, created_ts DESC;


