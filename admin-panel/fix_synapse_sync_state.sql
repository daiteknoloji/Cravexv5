-- ============================================
-- SYNAPSE SYNC STATE DÜZELTME
-- ============================================
-- Bu script, büyük veri silme işlemlerinden sonra
-- Synapse'in eksik internal state'ini düzeltir
-- ============================================
-- ⚠️ UYARI: Synapse servisini durdurmadan önce çalıştırın!
-- ============================================

-- 1. event_push_actions tablosunda eksik olan rotation tracking'i düzelt
-- Synapse, notification rotation için bir stream_ordering değeri bekliyor
-- Eğer hiç event yoksa, 0 olarak başlatıyoruz

-- Önce mevcut durumu kontrol edin:
-- SELECT * FROM event_push_actions WHERE 1=0; -- Tablo yapısını görmek için

-- Eğer event_push_actions tablosu tamamen boşsa ve Synapse hata veriyorsa,
-- bu tabloyu temizleyip Synapse'in yeniden başlatılmasını sağlayın
-- Ancak bu genellikle gerekli değildir çünkü Synapse otomatik olarak başlatır

-- 2. stream_ordering sequence'larını kontrol et ve gerekirse resetle
-- Synapse, events için stream_ordering kullanır ve bu bir sequence'dan gelir
-- Eğer tüm events silindiyse, sequence'ı resetlemek gerekebilir

-- PostgreSQL sequence'larını kontrol et:
-- SELECT sequence_name, last_value FROM information_schema.sequences 
-- WHERE sequence_schema = 'public' AND sequence_name LIKE '%stream%';

-- 3. event_stream_ordering sequence'ını resetle (eğer tüm events silindiyse)
-- NOT: Bu sadece TÜM events silindiyse yapılmalı!
-- DİKKAT: Bu sequence'ı resetlemek, Synapse'in event numaralandırmasını sıfırlar
-- Sadece kesinlikle gerekliyse kullanın!

-- ALTER SEQUENCE event_stream_ordering RESTART WITH 1;

-- 4. Synapse'in internal cache'lerini temizlemek için
-- Synapse'i yeniden başlatmak gerekebilir
-- Bu SQL script'i çalıştırdıktan sonra Synapse servisini yeniden başlatın

-- ============================================
-- ALTERNATİF ÇÖZÜM: Synapse'i yeniden başlat
-- ============================================
-- En güvenli çözüm, Synapse servisini yeniden başlatmaktır.
-- Synapse başlatıldığında, eksik internal state'i otomatik olarak
-- initialize edecektir.

-- ============================================
-- ÖNERİLEN ADIMLAR:
-- ============================================
-- 1. Bu script'i çalıştırın (şimdilik sadece kontrol sorguları)
-- 2. Synapse servisini yeniden başlatın (Railway'de restart)
-- 3. Element Web'de cache'i temizleyin ve yeniden login olun
-- 4. Eğer hala sorun varsa, stream_ordering sequence'ını resetleyin

-- Kontrol sorguları:
SELECT 
    'event_push_actions row count' as check_name,
    COUNT(*) as count
FROM event_push_actions;

SELECT 
    'events row count' as check_name,
    COUNT(*) as count
FROM events;

SELECT 
    'stream_ordering sequences' as check_name,
    sequence_name,
    last_value
FROM information_schema.sequences 
WHERE sequence_schema = 'public' 
AND (sequence_name LIKE '%stream%' OR sequence_name LIKE '%event%');

