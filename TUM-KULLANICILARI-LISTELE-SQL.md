# Tüm Kullanıcıları Listeleyen SQL Sorguları

## 1. Basit Kullanıcı Listesi (Tüm Kullanıcılar)

```sql
SELECT 
    name as user_id,
    admin,
    deactivated,
    creation_ts,
    locked,
    shadow_banned
FROM users
ORDER BY admin DESC, deactivated ASC, creation_ts DESC;
```

## 2. Detaylı Kullanıcı Listesi (Profil, Oda, Oturum Bilgileri ile)

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.deactivated,
    u.creation_ts,
    u.locked,
    u.shadow_banned,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count,
    (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as active_sessions,
    (SELECT COUNT(*) FROM devices WHERE user_id = u.name) as device_count
FROM users u
ORDER BY u.admin DESC, u.deactivated ASC, u.name;
```

## 3. Sadece Aktif Kullanıcılar (Deactivated = false)

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.creation_ts,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count,
    (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as active_sessions
FROM users u
WHERE u.deactivated = false OR u.deactivated IS NULL
ORDER BY u.admin DESC, u.name;
```

## 4. Sadece Pasif/Deaktif Kullanıcılar

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.creation_ts,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count
FROM users u
WHERE u.deactivated = true
ORDER BY u.creation_ts DESC;
```

## 5. Admin Kullanıcılar

```sql
SELECT 
    u.name as user_id,
    u.deactivated,
    u.creation_ts,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as active_sessions
FROM users u
WHERE u.admin = true
ORDER BY u.name;
```

## 6. Aktif Oturumu Olan Kullanıcılar (Login Olmuş)

```sql
SELECT DISTINCT
    u.name as user_id,
    u.admin,
    u.deactivated,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as session_count,
    (SELECT MAX(id) FROM access_tokens WHERE user_id = u.name) as last_token_id
FROM users u
WHERE EXISTS (
    SELECT 1 FROM access_tokens WHERE user_id = u.name
)
ORDER BY u.name;
```

## 7. En Çok Odaya Sahip Kullanıcılar

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.deactivated,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count
FROM users u
ORDER BY room_count DESC, u.name
LIMIT 50;
```

## 8. Yeni Eklenen Kullanıcılar (Son 30 Gün)

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.deactivated,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    TO_TIMESTAMP(u.creation_ts) as created_at,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count
FROM users u
WHERE u.creation_ts > EXTRACT(EPOCH FROM NOW() - INTERVAL '30 days') * 1000
ORDER BY u.creation_ts DESC;
```

## 9. Kullanıcı İstatistikleri (Özet)

```sql
SELECT 
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE admin = true) as admin_count,
    COUNT(*) FILTER (WHERE deactivated = true) as deactivated_count,
    COUNT(*) FILTER (WHERE deactivated = false OR deactivated IS NULL) as active_count,
    COUNT(*) FILTER (WHERE EXISTS (
        SELECT 1 FROM access_tokens WHERE user_id = users.name
    )) as users_with_sessions
FROM users;
```

## 10. Kullanıcı Detayları (Tüm Bilgiler)

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.deactivated,
    u.creation_ts,
    u.locked,
    u.shadow_banned,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT avatar_url FROM profiles WHERE user_id = u.name LIMIT 1) as avatar_url,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count,
    (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as active_sessions,
    (SELECT COUNT(*) FROM devices WHERE user_id = u.name) as device_count,
    (SELECT COUNT(*) FROM room_memberships WHERE user_id = u.name) as total_memberships,
    TO_TIMESTAMP(u.creation_ts / 1000) as created_at_formatted
FROM users u
ORDER BY u.admin DESC, u.deactivated ASC, u.creation_ts DESC;
```

## 11. Kullanıcı ve Mesaj İstatistikleri

```sql
SELECT 
    u.name as user_id,
    u.admin,
    u.deactivated,
    (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
    (SELECT COUNT(*) FROM events 
     WHERE sender = u.name AND type = 'm.room.message') as message_count,
    (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
     WHERE user_id = u.name AND membership = 'join') as room_count
FROM users u
ORDER BY message_count DESC NULLS LAST
LIMIT 100;
```

## 12. Kullanıcı Silme Kontrolü (Hangi Kullanıcılar Silinebilir)

```sql
-- Bu sorgu, silme işlemi yapılmadan önce hangi kullanıcıların silinebileceğini gösterir
SELECT 
    u.name as user_id,
    u.admin,
    u.deactivated,
    (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as tokens_to_delete,
    (SELECT COUNT(*) FROM devices WHERE user_id = u.name) as devices_to_delete,
    (SELECT COUNT(*) FROM room_memberships WHERE user_id = u.name) as memberships_to_delete
FROM users u
WHERE u.name != '@admin:matrix-synapse.up.railway.app'  -- Admin kullanıcıyı hariç tut
ORDER BY u.name;
```

## Kullanım Notları

- `creation_ts` değeri milisaniye cinsinden olabilir, formatlamak için `TO_TIMESTAMP(creation_ts / 1000)` kullanın
- `deactivated` NULL olabilir (eski Synapse versiyonlarında), bu durumda `deactivated = false` olarak kabul edilir
- `profiles` tablosunda kullanıcı profili olmayabilir, bu durumda `displayname` NULL döner
- `room_memberships` tablosunda `membership = 'join'` olanlar aktif üyelikleri gösterir

