# Railway Environment Variables Kontrol Listesi

## ✅ Considerate-adaptation (Admin Panel) Variables

### Mevcut Variables:
- ✅ `ADMIN_PASSWORD="GüçlüBirŞifre123!"` - **DOĞRU**
- ✅ `HOMESERVER_DOMAIN="matrix-synapse.up.railway.app"` - **DOĞRU**
- ✅ `SYNAPSE_URL="https://matrix-synapse.up.railway.app"` - **DOĞRU**
- ✅ `PGDATABASE="${{Postgres.PGDATABASE}}"` - **DOĞRU** (Railway shared Postgres)
- ✅ `PGHOST="${{Postgres.PGHOST}}"` - **DOĞRU**
- ✅ `PGPASSWORD="${{Postgres.PGPASSWORD}}"` - **DOĞRU**
- ✅ `PGPORT="${{Postgres.PGPORT}}"` - **DOĞRU**
- ✅ `PGUSER="${{Postgres.PGUSER}}"` - **DOĞRU**
- ✅ `RAILWAY_DOCKERFILE_PATH="admin-panel.Dockerfile"` - **DOĞRU**

### Eksik/Opsiyonel Variables:
- ⚠️ `ADMIN_USERNAME` - **YOK** (Varsayılan: `admin` kullanılacak - SORUN DEĞİL)

## ✅ Cravex4 (Matrix Synapse) Variables

### Mevcut Variables:
- ✅ `POSTGRES_DB="${{Postgres.PGDATABASE}}"` - **DOĞRU**
- ✅ `POSTGRES_HOST="${{Postgres.PGHOST}}"` - **DOĞRU**
- ✅ `POSTGRES_PASSWORD="${{Postgres.PGPASSWORD}}"` - **DOĞRU**
- ✅ `POSTGRES_PORT="${{Postgres.PGPORT}}"` - **DOĞRU**
- ✅ `POSTGRES_USER="${{Postgres.PGUSER}}"` - **DOĞRU**
- ✅ `SYNAPSE_PUBLIC_BASEURL="https://matrix-synapse.up.railway.app/"` - **DOĞRU**
- ✅ `SYNAPSE_SERVER_NAME="matrix-synapse.up.railway.app"` - **DOĞRU**
- ✅ `WEB_CLIENT_LOCATION="https://surprising-emotion-production.up.railway.app"` - **DOĞRU**

## 🔍 Kritik Kontroller

### 1. Admin User Kontrolü

Matrix Synapse'de admin user'ın var olup olmadığını kontrol et:

```sql
SELECT name, password_hash, admin, deactivated
FROM users
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

**Beklenen:**
- `name`: `@admin:matrix-synapse.up.railway.app`
- `admin`: `1` (true)
- `deactivated`: `0` (false)
- `password_hash`: `$2b$12$...` (bcrypt hash)

### 2. Admin Password Test

Admin Panel'de admin user ile login denemesi yap:
- Username: `admin`
- Password: `GüçlüBirŞifre123!`

Eğer login başarısız olursa, admin user'ın şifresi Matrix Synapse'de farklı olabilir.

### 3. Matrix Admin API Test

Railway Admin Panel loglarında şu logları ara:
```
[INFO] No admin token found, attempting auto-login for @admin:matrix-synapse.up.railway.app...
[INFO] Auto-login successful! Token obtained: ...
```

Eğer bu loglar görünmüyorsa veya `Auto-login failed` görünüyorsa:
- Admin user'ın şifresi yanlış olabilir
- `ADMIN_PASSWORD` environment variable'ı yanlış olabilir

## 🚨 Olası Sorunlar ve Çözümler

### Sorun 1: Admin User Yok veya Şifre Yanlış

**Belirti:**
- `Auto-login failed: 403 - Invalid username or password`
- Kullanıcı oluşturma başarısız

**Çözüm:**
1. Matrix Synapse'de admin user'ı kontrol et
2. Admin user'ın şifresini `GüçlüBirŞifre123!` olarak ayarla
3. Railway Admin Panel'i restart et

### Sorun 2: ADMIN_PASSWORD Yanlış

**Belirti:**
- `Matrix Admin API requires admin token`
- Auto-login başarısız

**Çözüm:**
1. Railway Dashboard → Admin Panel → Variables
2. `ADMIN_PASSWORD` değerini kontrol et
3. Matrix Synapse'deki admin user şifresi ile eşleştiğinden emin ol

### Sorun 3: SYNAPSE_URL Yanlış

**Belirti:**
- `Connection timeout` veya `Connection refused`
- Matrix Admin API çağrıları başarısız

**Çözüm:**
1. `SYNAPSE_URL` değerini kontrol et: `https://matrix-synapse.up.railway.app`
2. Matrix Synapse servisinin çalıştığından emin ol

## ✅ Test Adımları

1. **Admin Panel Login Test:**
   - Admin Panel'e git: `https://considerate-adaptation-production.up.railway.app/`
   - Login: `admin` / `GüçlüBirŞifre123!`
   - Başarılı olmalı ✅

2. **Yeni Kullanıcı Oluşturma Test:**
   - Admin Panel → Kullanıcılar → Yeni Kullanıcı
   - Username: `test5`
   - Password: `12344321`
   - Oluştur
   - Railway Admin Panel loglarında şu logları ara:
     ```
     [INFO] Auto-login successful! Token obtained: ...
     [INFO] User created via Matrix API. Verifying password...
     [INFO] Password verification successful!
     ```

3. **Login Test:**
   - Element Web'e git
   - Login: `test5` / `12344321`
   - Başarılı olmalı ✅

4. **Password Reset Test:**
   - Admin Panel → Kullanıcılar → `test5` → Şifre Değiştir
   - Yeni şifre: `12345678`
   - Kaydet
   - Element Web'de yeni şifre ile login dene
   - Başarılı olmalı ✅

## 📝 Notlar

- `ADMIN_USERNAME` environment variable'ı yok ama sorun değil (varsayılan `admin` kullanılacak)
- Tüm PostgreSQL variables Railway shared Postgres kullanıyor (doğru)
- `SYNAPSE_URL` ve `HOMESERVER_DOMAIN` aynı domain'i kullanıyor (doğru)

## 🎯 Sonuç

**Variables doğru görünüyor!** 

Şimdi test et:
1. Yeni kullanıcı oluştur
2. Login dene
3. Password reset dene

Eğer sorun olursa Railway Admin Panel loglarını kontrol et.
