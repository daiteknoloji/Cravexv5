-- Veritabanı şemasını kontrol et
-- Eğer users tablosu yoksa, Synapse henüz şemayı oluşturmamış demektir

-- 1. Tüm tabloları listele
SELECT 
    table_schema,
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 2. Tablo sayısını kontrol et
SELECT COUNT(*) as tablo_sayisi
FROM information_schema.tables
WHERE table_schema = 'public';

-- 3. Schema versiyonunu kontrol et (eğer varsa)
SELECT * FROM schema_version LIMIT 5;


