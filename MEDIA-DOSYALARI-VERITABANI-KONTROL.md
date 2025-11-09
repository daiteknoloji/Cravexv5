# Media Dosyaları Veritabanı Kontrol Rehberi

## 📋 Matrix Synapse'ta Media Dosyaları Nasıl Saklanır?

Matrix Synapse'ta media dosyaları **veritabanında saklanmaz**, fiziksel olarak dosya sisteminde veya S3 gibi bir storage'da saklanır. Veritabanında sadece **media referansları** (MXC URL'leri) saklanır.

---

## 🗄️ Media Referanslarının Saklandığı Tablolar

### 1. **Events Tablosu** (Ana Referans)
Media referansları `events` ve `event_json` tablolarında saklanır:

```sql
-- Belirli bir media_id'yi içeren event'leri bul
SELECT 
    e.event_id,
    e.sender,
    e.room_id,
    e.type,
    e.origin_server_ts,
    ej.json->'content'->>'url' as mxc_url,
    ej.json->'content'->>'msgtype' as msgtype,
    ej.json->'content'->'info'->>'mimetype' as mimetype,
    ej.json->'content'->'info'->>'size' as file_size
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json->'content'->>'url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
   OR ej.json->'content'->'info'->>'thumbnail_url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
ORDER BY e.origin_server_ts DESC
LIMIT 10;
```

### 2. **Local Media Repository** (Opsiyonel - Eğer varsa)
Bazı Synapse kurulumlarında media metadata'sı bu tabloda saklanabilir:

```sql
-- Local media repository tablosunu kontrol et
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%media%';
```

Eğer `local_media_repository` tablosu varsa:

```sql
-- Local media repository'den media bilgilerini al
SELECT 
    media_id,
    created_ts,
    upload_name,
    media_type,
    media_length,
    user_id,
    quarantined_by
FROM local_media_repository
WHERE media_id = 'jyinIDPycSnHOEyuztFhQCgg';
```

### 3. **Remote Media Cache** (Federasyon için)
Federasyon ile gelen media dosyaları için:

```sql
-- Remote media cache tablosunu kontrol et
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%remote%media%';
```

Eğer `remote_media_cache` tablosu varsa:

```sql
-- Remote media cache'den media bilgilerini al
SELECT 
    media_id,
    origin,
    created_ts,
    upload_name,
    media_type,
    media_length,
    quarantined_by
FROM remote_media_cache
WHERE media_id = 'jyinIDPycSnHOEyuztFhQCgg';
```

---

## 🔍 Belirli Bir Media ID İçin Kapsamlı Kontrol

```sql
-- 1. Event'lerde media referansını bul
SELECT 
    'EVENT' as source,
    e.event_id,
    e.sender,
    e.room_id,
    e.type,
    to_timestamp(e.origin_server_ts/1000) as timestamp,
    ej.json->'content'->>'url' as mxc_url
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json->'content'->>'url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
   OR ej.json->'content'->'info'->>'thumbnail_url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
ORDER BY e.origin_server_ts DESC
LIMIT 5;

-- 2. Tüm media ile ilgili tabloları listele
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND (
    table_name LIKE '%media%' 
    OR table_name LIKE '%file%'
    OR table_name LIKE '%content%'
)
ORDER BY table_name;

-- 3. Media ID'nin hangi event'lerde kullanıldığını bul
SELECT 
    e.event_id,
    e.sender,
    e.room_id,
    e.type,
    to_timestamp(e.origin_server_ts/1000) as timestamp,
    ej.json->'content'->>'url' as full_mxc_url,
    CASE 
        WHEN ej.json->'content'->>'url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%' THEN 'main_url'
        WHEN ej.json->'content'->'info'->>'thumbnail_url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%' THEN 'thumbnail_url'
        ELSE 'other'
    END as usage_type
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json->'content'->>'url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
   OR ej.json->'content'->'info'->>'thumbnail_url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
ORDER BY e.origin_server_ts DESC;
```

---

## 📁 Fiziksel Dosya Konumu

Media dosyaları fiziksel olarak şu konumlarda saklanır:

### Railway Deployment:
- **Local Storage**: `/data/media_store/` (Railway volume'da)
- **S3 Storage**: Eğer S3 yapılandırılmışsa, S3 bucket'ta

### Kontrol için:
```bash
# Railway container'ında media store'u kontrol et
docker exec <synapse-container> ls -la /data/media_store/

# Belirli bir media ID'nin dosyasını bul
docker exec <synapse-container> find /data/media_store -name "*jyinIDPycSnHOEyuztFhQCgg*"
```

---

## ⚠️ Önemli Notlar

1. **Media dosyaları veritabanında saklanmaz**: Sadece referanslar (MXC URL'leri) saklanır
2. **Fiziksel dosyalar**: `media_store` dizininde veya S3'te saklanır
3. **Media ID formatı**: `mxc://server_name/media_id` şeklinde saklanır
4. **Event JSON'da**: `content.url` veya `content.info.thumbnail_url` olarak saklanır

---

## 🔧 Sorun Giderme

### Media dosyası bulunamıyorsa:

1. **Event'te referans var mı kontrol et:**
```sql
SELECT COUNT(*) 
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json->'content'->>'url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%';
```

2. **Fiziksel dosya var mı kontrol et:**
   - Railway volume'da `/data/media_store/` dizinini kontrol et
   - S3 bucket'ı kontrol et (eğer S3 kullanılıyorsa)

3. **Media server erişilebilir mi kontrol et:**
   - `https://matrix-synapse.up.railway.app/_matrix/media/r0/download/matrix-synapse.up.railway.app/jyinIDPycSnHOEyuztFhQCgg`
   - Bu URL'e direkt erişim deneyin

---

## 📊 Örnek: Belirli Media ID İçin Tüm Bilgileri Getir

```sql
-- Kapsamlı media bilgisi sorgusu
WITH media_events AS (
    SELECT 
        e.event_id,
        e.sender,
        e.room_id,
        e.type,
        e.origin_server_ts,
        ej.json->'content'->>'url' as mxc_url,
        ej.json->'content'->>'msgtype' as msgtype,
        ej.json->'content'->'info'->>'mimetype' as mimetype,
        ej.json->'content'->'info'->>'size' as file_size,
        ej.json->'content'->'info'->>'w' as image_width,
        ej.json->'content'->'info'->>'h' as image_height
    FROM events e
    JOIN event_json ej ON e.event_id = ej.event_id
    WHERE ej.json->'content'->>'url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
       OR ej.json->'content'->'info'->>'thumbnail_url' LIKE '%jyinIDPycSnHOEyuztFhQCgg%'
)
SELECT 
    event_id,
    sender,
    room_id,
    type,
    to_timestamp(origin_server_ts/1000) as timestamp,
    mxc_url,
    msgtype,
    mimetype,
    file_size,
    image_width,
    image_height
FROM media_events
ORDER BY origin_server_ts DESC;
```

---

## 🎯 Sonuç

Media dosyaları:
- ✅ **Referanslar**: `events` + `event_json` tablolarında
- ✅ **Fiziksel dosyalar**: `/data/media_store/` dizininde veya S3'te
- ❌ **Veritabanında saklanmaz**: Sadece referanslar saklanır

