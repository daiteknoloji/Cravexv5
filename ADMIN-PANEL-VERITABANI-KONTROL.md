# 🔍 ADMIN PANEL VERİTABANI KONTROLÜ

## ✅ Admin Panel Kullanıcı Oluşturma İşlevi

**URL:** `https://considerate-adaptation-production.up.railway.app/`

Admin panel **DOĞRU ŞEKİLDE** veritabanına yazıyor! ✅

---

## 📊 Nasıl Çalışıyor?

### 1. Önce Matrix API Deniyor
- Synapse Admin API'yi kullanarak kullanıcı oluşturmayı dener
- Eğer admin token varsa, Matrix API üzerinden oluşturur

### 2. Fallback: Direkt Veritabanına Yazıyor
Eğer Matrix API çalışmıyorsa, **direkt PostgreSQL veritabanına** yazar:

**Yazılan Tablolar:**
1. ✅ `users` - Kullanıcı bilgileri (password hash ile)
2. ✅ `profiles` - Kullanıcı profili (displayname)
3. ✅ `user_directory` - Kullanıcı dizini (login için kritik!)
4. ✅ `user_directory_search` - Arama için

**Password Hash:**
- ✅ bcrypt kullanıyor (12 rounds - Synapse ile aynı)
- ✅ Güvenli şifreleme

---

## 🔍 VERİTABANI BAĞLANTISI

Admin panel şu environment variable'ları kullanıyor:

```python
DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'database': os.getenv('PGDATABASE', 'synapse'),
    'user': os.getenv('PGUSER', 'synapse_user'),
    'password': os.getenv('PGPASSWORD', 'SuperGucluSifre2024!'),
    'port': int(os.getenv('PGPORT', '5432'))
}
```

**HOMESERVER_DOMAIN:**
```python
HOMESERVER_DOMAIN = os.getenv('HOMESERVER_DOMAIN', 'localhost')
user_id = f'@{username}:{HOMESERVER_DOMAIN}'
```

---

## ⚠️ ÖNEMLİ: Railway Environment Variables

Railway'de admin panel servisinde şu variable'ların doğru ayarlanmış olması gerekiyor:

### Gerekli Environment Variables:

1. **PGHOST** - PostgreSQL host (Railway internal domain)
2. **PGDATABASE** - Database adı (`railway` veya `synapse`)
3. **PGUSER** - PostgreSQL kullanıcı adı
4. **PGPASSWORD** - PostgreSQL şifresi
5. **PGPORT** - PostgreSQL port (genellikle `5432`)
6. **HOMESERVER_DOMAIN** - `matrix-synapse.up.railway.app` (ÖNEMLİ!)

---

## ✅ KONTROL ADIMLARI

### 1. Railway'de Environment Variables Kontrol Et

Railway Dashboard → Admin Panel servisi → **Variables**:

Şu variable'ların olduğundan emin olun:
- ✅ `PGHOST` - Railway PostgreSQL internal host
- ✅ `PGDATABASE` - `railway` veya `synapse`
- ✅ `PGUSER` - PostgreSQL user
- ✅ `PGPASSWORD` - PostgreSQL password
- ✅ `PGPORT` - `5432`
- ✅ `HOMESERVER_DOMAIN` - `matrix-synapse.up.railway.app` ⚠️ ÖNEMLİ!

### 2. Admin Panel'den Kullanıcı Oluştur

1. `https://considerate-adaptation-production.up.railway.app/` açın
2. Login yapın (admin / admin123)
3. Kullanıcı oluşturun
4. Başarı mesajını kontrol edin

### 3. Veritabanında Kontrol Et

Railway Dashboard → PostgreSQL → **Query** sekmesinde:

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    admin,
    deactivated,
    TO_TIMESTAMP(creation_ts/1000) as olusturma_tarihi
FROM users
ORDER BY creation_ts DESC
LIMIT 10;
```

Bu sorgu son oluşturulan kullanıcıları gösterecek.

---

## 🎯 DOĞRULAMA

### Kullanıcı Oluşturuldu mu?

1. **Admin Panel'den oluşturun:**
   - Username: `testuser`
   - Password: `Test123!`
   - Admin: `false`

2. **Veritabanında kontrol edin:**
   ```sql
   SELECT name FROM users WHERE name LIKE '%testuser%';
   ```
   
   Beklenen: `@testuser:matrix-synapse.up.railway.app`

3. **Element Web'de login deneyin:**
   - URL: `https://cozy-dragon-54547b.netlify.app/#/login`
   - Username: `testuser`
   - Password: `Test123!`

---

## ⚠️ ÖNEMLİ NOTLAR

### Domain Sorunu:
Eğer `HOMESERVER_DOMAIN` yanlış ayarlanmışsa:
- ❌ Kullanıcı `@testuser:localhost` olarak oluşur
- ❌ Element Web'de login çalışmaz
- ✅ Doğru: `@testuser:matrix-synapse.up.railway.app`

### Veritabanı Bağlantısı:
- ✅ Admin panel Railway PostgreSQL'e bağlanıyor
- ✅ Aynı veritabanını kullanıyor (Synapse ile aynı)
- ✅ Doğru tablolara yazıyor

---

## 📋 CHECKLIST

- [ ] Railway Dashboard → Admin Panel → Variables kontrol ettim
- [ ] `HOMESERVER_DOMAIN` = `matrix-synapse.up.railway.app` olduğunu doğruladım
- [ ] PostgreSQL environment variable'ları doğru mu kontrol ettim
- [ ] Admin Panel'den kullanıcı oluşturdum
- [ ] Veritabanında kullanıcıyı kontrol ettim
- [ ] Element Web'de login denedim

---

**SONUÇ:** Admin panel **DOĞRU ŞEKİLDE** veritabanına yazıyor! Sadece `HOMESERVER_DOMAIN` environment variable'ının doğru ayarlanmış olması gerekiyor.


