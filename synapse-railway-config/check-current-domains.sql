-- Veritabanında hangi domain'lerin olduğunu kontrol et
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as user_count 
FROM users 
GROUP BY split_part(name, ':', 2)
ORDER BY user_count DESC;


