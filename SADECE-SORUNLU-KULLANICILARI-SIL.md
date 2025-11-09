# 🔍 Sorunlu Kullanıcıları Bul ve Sil

## Sorun
Synapse crash oluyor çünkü veritabanında farklı domain'de kullanıcılar var.

## ✅ Çözüm: Sadece Sorunlu Kullanıcıları Sil

### Adım 1: Veritabanındaki Kullanıcıları Kontrol Et

Railway CLI ile PostgreSQL'e bağlan:

```bash
railway run --service postgres psql -c "SELECT name, creation_ts FROM users ORDER BY creation_ts DESC LIMIT 20;"
```

Bu komut son 20 kullanıcıyı gösterir. Kullanıcı adları şu formatta olacak:
- `@kullanici:matrix-synapse-production.up.railway.app`
- `@kullanici:cravex1-production.up.railway.app`

### Adım 2: Hangi Domain'de Kullanıcılar Var?

```bash
railway run --service postgres psql -c "SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi FROM users GROUP BY split_part(name, ':', 2);"
```

Bu komut hangi domain'de kaç kullanıcı olduğunu gösterir.

### Adım 3A: Eğer `matrix-synapse-production.up.railway.app` Domain'inde Kullanıcılar Varsa

**Çözüm:** Railway'de `SYNAPSE_SERVER_NAME`'i `matrix-synapse-production.up.railway.app` olarak ayarla (zaten öyle görünüyor).

VEYA sadece o domain'deki kullanıcıları sil:

```bash
railway run --service postgres psql -c "DELETE FROM users WHERE name LIKE '%:matrix-synapse-production.up.railway.app';"
```

### Adım 3B: Eğer `cravex1-production.up.railway.app` Domain'inde Kullanıcılar Varsa

**Çözüm:** Railway'de `SYNAPSE_SERVER_NAME`'i `cravex1-production.up.railway.app` olarak ayarla.

VEYA sadece o domain'deki kullanıcıları sil:

```bash
railway run --service postgres psql -c "DELETE FROM users WHERE name LIKE '%:cravex1-production.up.railway.app';"
```

### Adım 4: İlişkili Tabloları Temizle

Kullanıcıları sildikten sonra ilişkili verileri de temizle:

```bash
railway run --service postgres psql -c "
DELETE FROM user_ips WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM user_filters WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM user_directory WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM profiles WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM access_tokens WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM devices WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
"
```

**VEYA** eğer `cravex1-production.up.railway.app` domain'indeki kullanıcıları sildiysen:

```bash
railway run --service postgres psql -c "
DELETE FROM user_ips WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM user_filters WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM user_directory WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM profiles WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM access_tokens WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM devices WHERE user_id LIKE '%:cravex1-production.up.railway.app';
"
```

### Adım 5: Synapse'i Yeniden Başlat

Railway dashboard → Synapse servisi → Redeploy

---

## 🎯 EN KOLAY ÇÖZÜM (Önerilen)

Loglardan görüldüğü üzere:
- Veritabanında `matrix-synapse-production.up.railway.app` domain'inde kullanıcılar var
- Synapse `matrix-synapse-production.up.railway.app` ile başlamaya çalışıyor ama hata veriyor

**Çözüm:** Railway'de `SYNAPSE_SERVER_NAME` environment variable'ını kontrol et. Eğer `cravex1-production.up.railway.app` olarak ayarlıysa, `matrix-synapse-production.up.railway.app` olarak değiştir.

VEYA veritabanındaki kullanıcıların domain'ini kontrol et ve Synapse'i o domain ile başlat.

---

## 🔍 Hangi Domain Kullanılmalı?

Loglardan:
```
Server hostname: matrix-synapse-production.up.railway.app
Exception: Found users in database not native to matrix-synapse-production.up.railway.app!
```

Bu, veritabanında `matrix-synapse-production.up.railway.app` **DIŞINDA** başka bir domain'de kullanıcılar olduğunu gösteriyor.

**Kontrol et:**
```bash
railway run --service postgres psql -c "SELECT DISTINCT split_part(name, ':', 2) as domain FROM users;"
```

Bu komut veritabanındaki tüm domain'leri gösterir. Synapse'i **en çok kullanıcının olduğu domain** ile başlat.


