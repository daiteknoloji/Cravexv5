-- TÜM KULLANICILARI SİL
-- DİKKAT: Bu işlem GERİ ALINAMAZ! TÜM KULLANICILAR SİLİNECEK!

-- ÖNCE KONTROL EDİN: Kaç kullanıcı var?
SELECT COUNT(*) as toplam_kullanici_sayisi FROM users;

-- Hangi domain'ler var?
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;

-- EĞER DEVAM ETMEK İSTİYORSANIZ, AŞAĞIDAKİ SİLME İŞLEMİNİ ÇALIŞTIRIN:

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

-- DOĞRULAMA: Kullanıcılar silindi mi?
SELECT COUNT(*) as kalan_kullanici_sayisi FROM users;
-- Sonuç 0 olmalı!

-- Domain kontrolü
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2);
-- Sonuç boş olmalı!


