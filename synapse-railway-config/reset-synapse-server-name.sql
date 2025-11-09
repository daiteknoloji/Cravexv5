-- Synapse'in server_name kontrolünü atlamak için veritabanını tamamen temizle
-- DİKKAT: Bu işlem TÜM VERİLERİ SİLECEKTİR!

-- Önce yedek alın!
-- Railway Dashboard → PostgreSQL → Settings → Backups

-- 1. Tüm tabloları sil
DROP SCHEMA public CASCADE;

-- 2. Schema'yı yeniden oluştur
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- 3. Synapse servisini yeniden başlatın
-- Synapse otomatik olarak şemayı yeniden oluşturacak ve server_name'i doğru kaydedecek


