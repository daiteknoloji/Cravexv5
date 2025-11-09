-- Synapse'in server_name'i sakladığı metadata tablolarını kontrol et
-- Synapse genellikle server_name'i schema_version veya başka bir metadata tablosunda saklar

-- 1. Schema version tablosunu kontrol et
SELECT * FROM schema_version;

-- 2. Tüm tabloları listele (metadata tablolarını bulmak için)
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- 3. "server_name" içeren kolonları bul
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND (column_name LIKE '%server%' OR column_name LIKE '%name%' OR column_name LIKE '%domain%')
ORDER BY table_name, column_name;

-- 4. Config veya metadata içeren tabloları kontrol et
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND (table_name LIKE '%config%' OR table_name LIKE '%metadata%' OR table_name LIKE '%server%')
ORDER BY table_name;

-- 5. Eğer "applied_schema_deltas" tablosu varsa kontrol et
SELECT * FROM applied_schema_deltas WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'applied_schema_deltas') LIMIT 10;


