# Tüm Odaları Listeleyen SQL Sorguları

## 1. Basit Oda Listesi (Tüm Odalar)

```sql
SELECT 
    room_id,
    creator,
    is_public,
    room_version
FROM rooms
ORDER BY room_id;
```

## 2. Detaylı Oda Listesi (İsim, Üye Sayısı, Mesaj Sayısı ile)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    r.creator,
    r.is_public,
    r.room_version,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count
FROM rooms r
ORDER BY member_count DESC, r.room_id;
```

## 3. En Çok Üyeye Sahip Odalar

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count
FROM rooms r
ORDER BY member_count DESC
LIMIT 50;
```

## 4. En Çok Mesaj İçeren Odalar

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
ORDER BY message_count DESC
LIMIT 50;
```

## 5. Public Odalar (Herkese Açık)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    r.creator,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
WHERE r.is_public = true
ORDER BY member_count DESC;
```

## 6. Private Odalar (Özel)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    r.creator,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
WHERE r.is_public = false OR r.is_public IS NULL
ORDER BY member_count DESC;
```

## 7. Direct Message (DM) Odaları (2 Kişilik)

```sql
SELECT 
    r.room_id,
    r.creator,
    (SELECT STRING_AGG(user_id, ' ↔ ')
     FROM room_memberships
     WHERE room_id = r.room_id AND membership = 'join'
     LIMIT 2) as participants,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count
FROM rooms r
WHERE (SELECT COUNT(*) FROM room_memberships 
       WHERE room_id = r.room_id AND membership = 'join') = 2
  AND NOT EXISTS (
      SELECT 1 FROM event_json ej
      WHERE ej.room_id = r.room_id 
        AND ej.json::json->>'type' = 'm.room.name'
  )
ORDER BY r.room_id;
```

## 8. Grup Odaları (3+ Kişilik)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    r.creator,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count
FROM rooms r
WHERE (SELECT COUNT(*) FROM room_memberships 
       WHERE room_id = r.room_id AND membership = 'join') > 2
ORDER BY member_count DESC;
```

## 9. İsimsiz Odalar (İsim Olmayan)

```sql
SELECT 
    r.room_id,
    r.creator,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count
FROM rooms r
WHERE NOT EXISTS (
    SELECT 1 FROM event_json ej
    WHERE ej.room_id = r.room_id 
      AND ej.json::json->>'type' = 'm.room.name'
)
ORDER BY member_count DESC;
```

## 10. Belirli Bir Kullanıcının Odaları

```sql
-- @user:matrix-synapse.up.railway.app kullanıcısının odaları
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    rm.membership,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
JOIN room_memberships rm ON r.room_id = rm.room_id
WHERE rm.user_id = '@user:matrix-synapse.up.railway.app'
  AND rm.membership = 'join'
ORDER BY member_count DESC;
```

## 11. Oda İstatistikleri (Özet)

```sql
SELECT 
    COUNT(*) as total_rooms,
    COUNT(*) FILTER (WHERE is_public = true) as public_rooms,
    COUNT(*) FILTER (WHERE is_public = false OR is_public IS NULL) as private_rooms,
    COUNT(*) FILTER (WHERE EXISTS (
        SELECT 1 FROM room_memberships rm
        WHERE rm.room_id = rooms.room_id 
          AND rm.membership = 'join'
        HAVING COUNT(*) = 2
    )) as dm_rooms,
    COUNT(*) FILTER (WHERE EXISTS (
        SELECT 1 FROM room_memberships rm
        WHERE rm.room_id = rooms.room_id 
          AND rm.membership = 'join'
        HAVING COUNT(*) > 2
    )) as group_rooms,
    COUNT(*) FILTER (WHERE NOT EXISTS (
        SELECT 1 FROM event_json ej
        WHERE ej.room_id = rooms.room_id 
          AND ej.json::json->>'type' = 'm.room.name'
    )) as unnamed_rooms
FROM rooms;
```

## 12. Oda ve Üye Detayları (Tüm Bilgiler)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    (SELECT ej.json::json->'content'->>'topic' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.topic'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_topic,
    r.creator,
    r.is_public,
    r.room_version,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'invite') as invited_count,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'leave') as left_count,
    (SELECT COUNT(*) FROM events 
     WHERE room_id = r.room_id AND type = 'm.room.message') as message_count,
    (SELECT MAX(origin_server_ts) FROM events 
     WHERE room_id = r.room_id) as last_message_ts
FROM rooms r
ORDER BY last_message_ts DESC NULLS LAST;
```

## 13. Boş Odalar (Üyesi Olmayan)

```sql
SELECT 
    r.room_id,
    r.creator,
    r.is_public
FROM rooms r
WHERE NOT EXISTS (
    SELECT 1 FROM room_memberships rm
    WHERE rm.room_id = r.room_id 
      AND rm.membership = 'join'
)
ORDER BY r.room_id;
```

## 14. Son Aktif Odalar (Son Mesaj Tarihine Göre)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    (SELECT MAX(origin_server_ts) FROM events 
     WHERE room_id = r.room_id) as last_activity_ts,
    TO_TIMESTAMP((SELECT MAX(origin_server_ts) FROM events 
                  WHERE room_id = r.room_id) / 1000) as last_activity_date,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
WHERE EXISTS (
    SELECT 1 FROM events 
    WHERE room_id = r.room_id
)
ORDER BY last_activity_ts DESC NULLS LAST
LIMIT 100;
```

## 15. Oda Üyeleri ile Birlikte (Detaylı)

```sql
SELECT 
    r.room_id,
    (SELECT ej.json::json->'content'->>'name' 
     FROM event_json ej
     WHERE ej.room_id = r.room_id 
       AND ej.json::json->>'type' = 'm.room.name'
     ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
     LIMIT 1) as room_name,
    (SELECT STRING_AGG(rm.user_id, ', ' ORDER BY rm.user_id)
     FROM room_memberships rm
     WHERE rm.room_id = r.room_id 
       AND rm.membership = 'join'
    ) as members,
    (SELECT COUNT(*) FROM room_memberships 
     WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
ORDER BY member_count DESC;
```

## Kullanım Notları

- `room_id`: Oda benzersiz kimliği (örn: `!abc123:matrix-synapse.up.railway.app`)
- `creator`: Odayı oluşturan kullanıcı ID'si
- `is_public`: Oda herkese açık mı? (`true` = public, `false` = private)
- `room_version`: Oda versiyonu (Matrix protokol versiyonu)
- `room_name`: Oda adı `event_json` tablosundan `m.room.name` event tipinden alınır
- `room_topic`: Oda konusu `event_json` tablosundan `m.room.topic` event tipinden alınır
- `member_count`: Aktif üye sayısı (`membership = 'join'`)
- `message_count`: Oda içindeki mesaj sayısı (`type = 'm.room.message'`)
- Direct Message (DM): 2 kişilik ve ismi olmayan odalar genellikle DM'dir
- `event_json` tablosunda oda bilgileri JSON formatında saklanır
- `room_memberships` tablosunda üyelik bilgileri tutulur (`join`, `invite`, `leave`, `ban`)

## ÖNEMLİ: PostgreSQL Tip Uyumluluğu

- `is_public` kolonu `boolean` tipindedir: `true` = public, `false` = private
- `room_version` kolonu `text` veya `integer` tipinde olabilir
- `origin_server_ts` değerleri milisaniye cinsinden olabilir, formatlamak için `TO_TIMESTAMP(ts / 1000)` kullanın

