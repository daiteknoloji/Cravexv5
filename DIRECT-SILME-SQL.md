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

TRUNCATE TABLE redactions CASCADE;
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

## EN HIZLI YOL (Kopyala-Yapıştır)

```sql
BEGIN;
DELETE FROM redactions;
DELETE FROM event_json;
DELETE FROM events;
DELETE FROM room_memberships;
DELETE FROM rooms;
SELECT COUNT(*) as kalan_odalar FROM rooms;
SELECT COUNT(*) as kalan_mesajlar FROM events;
COMMIT;
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

