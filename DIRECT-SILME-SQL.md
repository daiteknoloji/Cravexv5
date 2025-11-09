# Direkt Silme SQL Sorguları (Yedek Olmadan)

## ⚠️ UYARI: Bu sorgular geri alınamaz!

---

## 1. TÜM MESAJLARI VE ODALARI SİL (Önerilen - Transaction ile)

```sql
BEGIN;

-- Mesajları sil
DELETE FROM redactions;
DELETE FROM event_json WHERE json::json->>'type' = 'm.room.message';
DELETE FROM events WHERE type = 'm.room.message';

-- Oda event'lerini sil
DELETE FROM event_json WHERE room_id IS NOT NULL;
DELETE FROM events WHERE room_id IS NOT NULL;

-- Oda üyeliklerini sil
DELETE FROM room_memberships;

-- Odaları sil
DELETE FROM rooms;

-- Kontrol
SELECT COUNT(*) as kalan_odalar FROM rooms;
SELECT COUNT(*) as kalan_mesajlar FROM events;

-- Eğer her şey tamam ise:
COMMIT;

-- Eğer sorun varsa geri almak için:
-- ROLLBACK;
```

---

## 2. HIZLI SİLME (TRUNCATE - En Hızlı)

```sql
-- Dikkat: TRUNCATE geri alınamaz ve AUTO_INCREMENT'i sıfırlar!
-- ÖNEMLİ: Eğer transaction hatası alırsanız, önce ROLLBACK; yapın

-- Önce transaction'ı temizle (eğer hata varsa)
ROLLBACK;

-- Sonra tek tek çalıştırın (her biri ayrı transaction)
TRUNCATE TABLE redactions CASCADE;
TRUNCATE TABLE event_json CASCADE;
TRUNCATE TABLE events CASCADE;
TRUNCATE TABLE room_memberships CASCADE;
TRUNCATE TABLE rooms CASCADE;
```

## 2A. TRUNCATE HATASI ALIRSANIZ (Tablo Yoksa veya Constraint Sorunu)

```sql
-- Önce transaction'ı temizle
ROLLBACK;

-- Tabloları kontrol et
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('redactions', 'event_json', 'events', 'room_memberships', 'rooms');

-- Eğer redactions tablosu yoksa, sadece diğerlerini silin:
TRUNCATE TABLE event_json CASCADE;
TRUNCATE TABLE events CASCADE;
TRUNCATE TABLE room_memberships CASCADE;
TRUNCATE TABLE rooms CASCADE;
```

---

## 3. TEK SORGU İLE SİLME (DELETE)

```sql
DELETE FROM redactions;
DELETE FROM event_json;
DELETE FROM events;
DELETE FROM room_memberships;
DELETE FROM rooms;
```

---

## 4. SADECE MESAJLARI SİL (Odaları Koru)

```sql
DELETE FROM redactions;
DELETE FROM event_json WHERE json::json->>'type' = 'm.room.message';
DELETE FROM events WHERE type = 'm.room.message';
```

---

## 5. SADECE ODALARI SİL (Mesajları Koru - Önerilmez)

```sql
DELETE FROM room_memberships;
DELETE FROM rooms;
```

---

## 6. SİLME SONRASI TEMİZLEME (Disk Alanını Geri Kazan)

```sql
-- Silme işleminden sonra çalıştırın
VACUUM FULL ANALYZE redactions;
VACUUM FULL ANALYZE event_json;
VACUUM FULL ANALYZE events;
VACUUM FULL ANALYZE room_memberships;
VACUUM FULL ANALYZE rooms;
```

---

## EN HIZLI YOL (Kopyala-Yapıştır - DELETE ile Güvenli)

```sql
BEGIN;

-- Önce redactions varsa sil (yoksa hata vermez)
DELETE FROM redactions WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'redactions');

-- Diğer tabloları sil
DELETE FROM event_json;
DELETE FROM events;
DELETE FROM room_memberships;
DELETE FROM rooms;

-- Kontrol
SELECT COUNT(*) as kalan_odalar FROM rooms;
SELECT COUNT(*) as kalan_mesajlar FROM events;

-- Eğer her şey tamam ise:
COMMIT;

-- Eğer sorun varsa:
-- ROLLBACK;

-- Temizleme
VACUUM FULL ANALYZE;
```

## EN GÜVENLİ YOL (Her Komut Ayrı - Hata Durumunda Devam Eder)

```sql
-- Her komutu tek tek çalıştırın (transaction olmadan)

-- 1. Redactions (varsa)
DELETE FROM redactions;

-- 2. Event JSON'ları
DELETE FROM event_json;

-- 3. Events (mesajlar ve diğer event'ler)
DELETE FROM events;

-- 4. Oda üyelikleri
DELETE FROM room_memberships;

-- 5. Odalar
DELETE FROM rooms;

-- Kontrol
SELECT COUNT(*) as kalan_odalar FROM rooms;
SELECT COUNT(*) as kalan_mesajlar FROM events;

-- Temizleme
VACUUM FULL ANALYZE;
```

---

## KONTROL SORGULARI (Silme Öncesi/Sonrası)

```sql
-- Kaç oda var?
SELECT COUNT(*) as toplam_oda FROM rooms;

-- Kaç mesaj var?
SELECT COUNT(*) as toplam_mesaj FROM events WHERE type = 'm.room.message';

-- Kaç üyelik var?
SELECT COUNT(*) as toplam_uyelik FROM room_memberships;
```

