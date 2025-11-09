-- Tüm kullanıcıları domain'leriyle birlikte listele
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY domain, name;


