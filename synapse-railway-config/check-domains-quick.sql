-- Hangi domain'ler var? Hızlı kontrol
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;


