# Tüm Odaları ve Mesajları Silme SQL Sorguları

## ⚠️ ÖNEMLİ UYARI

**Bu sorgular veritabanındaki TÜM odaları ve mesajları kalıcı olarak siler!**
- **Yedekleme:** İşlem öncesi mutlaka veritabanı yedeği alın
- **Geri dönüş yok:** Silinen veriler geri getirilemez
- **Test ortamında deneyin:** Önce test ortamında deneyin

---

## 1. ÖNCE YEDEK ALMA (ÖNERİLEN)

```sql
-- Tüm odaları yedekleme
CREATE TABLE rooms_backup AS SELECT * FROM rooms;

-- Tüm mesajları yedekleme
CREATE TABLE events_backup AS SELECT * FROM events;

-- Tüm oda üyeliklerini yedekleme
CREATE TABLE room_memberships_backup AS SELECT * FROM room_memberships;

-- Tüm event JSON'larını yedekleme
CREATE TABLE event_json_backup AS SELECT * FROM event_json;
```

---

## 2. SİLME SIRASI (Önemli: Bağımlılık sırasına göre)

### Adım 1: Mesajları Sil (Önce mesajlar, sonra odalar)

```sql
-- Tüm mesajları sil
DELETE FROM events WHERE type = 'm.room.message';

-- Tüm event JSON'larını sil (mesaj içerikleri)
DELETE FROM event_json WHERE json::json->>'type' = 'm.room.message';

-- Silinen mesaj kayıtlarını temizle
DELETE FROM redactions;
```

### Adım 2: Oda Event'lerini Sil

```sql
-- Tüm oda event'lerini sil (oda ismi, topic, avatar vb.)
DELETE FROM events WHERE room_id IS NOT NULL;

-- Tüm oda event JSON'larını sil
DELETE FROM event_json WHERE room_id IS NOT NULL;
```

### Adım 3: Oda Üyeliklerini Sil

```sql
-- Tüm oda üyeliklerini sil
DELETE FROM room_memberships;
```

### Adım 4: Odaları Sil

```sql
-- Tüm odaları sil
DELETE FROM rooms;
```

---

## 3. TEK SORGU İLE TÜMÜNÜ SİLME (Hızlı)

```sql
-- Tüm mesajları ve event'leri sil
DELETE FROM events;
DELETE FROM event_json;
DELETE FROM redactions;

-- Tüm oda üyeliklerini sil
DELETE FROM room_memberships;

-- Tüm odaları sil
DELETE FROM rooms;
```

---

## 4. TRUNCATE İLE SİLME (Daha Hızlı, AUTO_INCREMENT Resetler)

```sql
-- Dikkat: TRUNCATE FOREIGN KEY kontrolü yapmaz, önce bağımlılıkları silin!

-- Önce bağımlı tabloları temizle
TRUNCATE TABLE redactions CASCADE;
TRUNCATE TABLE event_json CASCADE;
TRUNCATE TABLE events CASCADE;
TRUNCATE TABLE room_memberships CASCADE;

-- Sonra odaları temizle
TRUNCATE TABLE rooms CASCADE;
```

---

## 5. BELİRLİ BİR ODAYI VE MESAJLARINI SİLME

```sql
-- Belirli bir oda ID'si için
-- Örnek: !lkYurmTqwFVvZIRUzs:matrix-synapse.up.railway.app

-- 1. Oda mesajlarını sil
DELETE FROM events 
WHERE room_id = '!lkYurmTqwFVvZIRUzs:matrix-synapse.up.railway.app';

-- 2. Oda event JSON'larını sil
DELETE FROM event_json 
WHERE room_id = '!lkYurmTqwFVvZIRUzs:matrix-synapse.up.railway.app';

-- 3. Oda üyeliklerini sil
DELETE FROM room_memberships 
WHERE room_id = '!lkYurmTqwFVvZIRUzs:matrix-synapse.up.railway.app';

-- 4. Odayı sil
DELETE FROM rooms 
WHERE room_id = '!lkYurmTqwFVvZIRUzs:matrix-synapse.up.railway.app';
```

---

## 6. BELİRLİ KULLANICININ ODALARINI SİLME

```sql
-- Örnek: @6e:matrix-synapse.up.railway.app kullanıcısının odaları

-- 1. Kullanıcının oda mesajlarını sil
DELETE FROM events 
WHERE room_id IN (
    SELECT room_id FROM room_memberships 
    WHERE user_id = '@6e:matrix-synapse.up.railway.app'
);

-- 2. Kullanıcının oda event JSON'larını sil
DELETE FROM event_json 
WHERE room_id IN (
    SELECT room_id FROM room_memberships 
    WHERE user_id = '@6e:matrix-synapse.up.railway.app'
);

-- 3. Kullanıcının oda üyeliklerini sil
DELETE FROM room_memberships 
WHERE user_id = '@6e:matrix-synapse.up.railway.app';

-- 4. Kullanıcının oluşturduğu odaları sil
DELETE FROM rooms 
WHERE creator = '@6e:matrix-synapse.up.railway.app';
```

---

## 7. BOŞ ODALARI SİLME (Üyesi Olmayan)

```sql
-- Üyesi olmayan odaları bul ve sil
DELETE FROM rooms 
WHERE room_id NOT IN (
    SELECT DISTINCT room_id 
    FROM room_memberships 
    WHERE membership = 'join'
);
```

---

## 8. MESAJ SAYISINA GÖRE SİLME

```sql
-- Mesajı olmayan odaları sil
DELETE FROM rooms 
WHERE room_id NOT IN (
    SELECT DISTINCT room_id 
    FROM events 
    WHERE type = 'm.room.message'
);
```

---

## 9. SİLME ÖNCESİ KONTROL SORGULARI

### Kaç oda var?
```sql
SELECT COUNT(*) as total_rooms FROM rooms;
```

### Kaç mesaj var?
```sql
SELECT COUNT(*) as total_messages FROM events WHERE type = 'm.room.message';
```

### Kaç oda üyeliği var?
```sql
SELECT COUNT(*) as total_memberships FROM room_memberships;
```

### En çok mesajı olan odalar
```sql
SELECT 
    room_id,
    COUNT(*) as message_count
FROM events 
WHERE type = 'm.room.message'
GROUP BY room_id
ORDER BY message_count DESC
LIMIT 10;
```

---

## 10. GÜVENLİ SİLME (Transaction ile - Hata durumunda geri alınır)

```sql
BEGIN;

-- İşlemleri yapın
DELETE FROM events;
DELETE FROM event_json;
DELETE FROM redactions;
DELETE FROM room_memberships;
DELETE FROM rooms;

-- Kontrol edin
SELECT COUNT(*) FROM rooms;
SELECT COUNT(*) FROM events;

-- Eğer her şey tamam ise:
COMMIT;

-- Eğer bir sorun varsa geri almak için:
-- ROLLBACK;
```

---

## 11. SADECE MESAJLARI SİLME (Odaları Koruma)

```sql
-- Sadece mesajları sil, odaları koru
DELETE FROM events WHERE type = 'm.room.message';
DELETE FROM event_json WHERE json::json->>'type' = 'm.room.message';
DELETE FROM redactions;
```

---

## 12. SADECE ODALARI SİLME (Mesajları Koruma - Önerilmez)

```sql
-- ⚠️ DİKKAT: Bu sorgu mesajları korur ama odaları siler
-- Bu durumda mesajlar "orphan" (sahipsiz) kalır

DELETE FROM room_memberships;
DELETE FROM rooms;
```

---

## 13. BELİRLİ TARİHTEN ÖNCEKİ MESAJLARI SİLME

```sql
-- Örnek: 2024-01-01'den önceki mesajları sil

-- Timestamp'i milisaniye cinsinden hesaplayın
-- 2024-01-01 00:00:00 = 1704067200000 (milisaniye)

DELETE FROM events 
WHERE type = 'm.room.message' 
  AND origin_server_ts < 1704067200000;

DELETE FROM event_json 
WHERE json::json->>'type' = 'm.room.message'
  AND (json::json->>'origin_server_ts')::bigint < 1704067200000;
```

---

## 14. TABLO BOYUTLARINI KONTROL ETME

```sql
-- Tablo boyutlarını göster
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('rooms', 'events', 'event_json', 'room_memberships', 'redactions')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 15. SİLME SONRASI TEMİZLEME (VACUUM)

```sql
-- Silme işleminden sonra disk alanını geri kazanmak için
VACUUM FULL ANALYZE rooms;
VACUUM FULL ANALYZE events;
VACUUM FULL ANALYZE event_json;
VACUUM FULL ANALYZE room_memberships;
VACUUM FULL ANALYZE redactions;
```

---

## ÖNERİLEN SİLME ADIMLARI

1. **Yedekleme yapın** (Bölüm 1)
2. **Kontrol sorgularını çalıştırın** (Bölüm 9)
3. **Transaction başlatın** (Bölüm 10)
4. **Silme işlemlerini yapın** (Bölüm 3 veya 4)
5. **Kontrol edin** (Bölüm 9)
6. **Commit edin** (Bölüm 10)
7. **VACUUM çalıştırın** (Bölüm 15)

---

## HIZLI BAŞLANGIÇ (Tümünü Silmek İçin)

```sql
-- 1. Yedek alın
CREATE TABLE rooms_backup AS SELECT * FROM rooms;
CREATE TABLE events_backup AS SELECT * FROM events;
CREATE TABLE room_memberships_backup AS SELECT * FROM room_memberships;
CREATE TABLE event_json_backup AS SELECT * FROM event_json;

-- 2. Transaction başlatın
BEGIN;

-- 3. Silme işlemleri
DELETE FROM redactions;
DELETE FROM event_json;
DELETE FROM events;
DELETE FROM room_memberships;
DELETE FROM rooms;

-- 4. Kontrol edin
SELECT COUNT(*) FROM rooms;  -- 0 olmalı
SELECT COUNT(*) FROM events;  -- 0 olmalı

-- 5. Commit edin
COMMIT;

-- 6. Temizleme
VACUUM FULL ANALYZE;
```

---

## NOTLAR

- **Foreign Key:** Bazı tablolar arasında foreign key ilişkileri olabilir, bu yüzden silme sırası önemlidir
- **CASCADE:** `TRUNCATE ... CASCADE` kullanırsanız bağımlı tablolar da otomatik silinir
- **Performance:** Büyük tablolarda `DELETE` yerine `TRUNCATE` daha hızlıdır ama geri alınamaz
- **Disk Alanı:** Silme sonrası `VACUUM FULL` çalıştırmak disk alanını geri kazandırır
- **Index'ler:** Silme işleminden sonra index'ler otomatik güncellenir ama `VACUUM ANALYZE` önerilir

