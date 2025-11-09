# Admin User Aktif Etme SQL

## Sorun
Admin user `deactivated = 1` (deaktif) durumda. Bu yüzden Matrix Admin API auto-login çalışmıyor.

## Çözüm

Railway PostgreSQL'e bağlan ve şu SQL'i çalıştır:

```sql
-- Admin user'ı aktif et
UPDATE users 
SET deactivated = 0 
WHERE name = '@admin:matrix-synapse.up.railway.app';

-- Kontrol et
SELECT name, password_hash, admin, deactivated
FROM users
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

**Beklenen Sonuç:**
- `deactivated`: `0` (aktif) ✅

## Alternatif: Matrix Synapse Restart

Eğer SQL ile düzeltme çalışmazsa:

1. **Matrix Synapse'i restart et** (Railway Dashboard)
2. **Admin Panel'i restart et** (Railway Dashboard)
3. **Yeni kullanıcı oluşturmayı tekrar dene**

## Notlar

- Admin user aktif olmalı ki Matrix Admin API auto-login çalışsın
- `deactivated = 1` olan admin user ile login yapılamaz
- SQL ile düzeltme sonrası Matrix Synapse restart gerekebilir

