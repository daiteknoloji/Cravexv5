-- Synapse veritabanını TAMAMEN temizle
-- DİKKAT: Bu işlem TÜM VERİLERİ SİLECEKTİR!

-- 1. Tüm bağlantıları kes
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = current_database()
  AND pid <> pg_backend_pid();

-- 2. Tüm tabloları sil
DROP SCHEMA public CASCADE;

-- 3. Schema'yı yeniden oluştur
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- 4. Tüm sequence'ları temizle (eğer varsa)
DROP SEQUENCE IF EXISTS public.schema_version_version_seq CASCADE;

-- 5. Doğrulama: Şema boş mu?
SELECT COUNT(*) as tablo_sayisi 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Sonuç 0 olmalı!


