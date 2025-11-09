# 🔧 RAILWAY ADMIN PANEL ENVIRONMENT VARIABLES

## 📋 Mevcut Variables (Doğru ✅)

Railway Dashboard → Admin Panel (`considerate-adaptation`) → **Variables**:

```
PGDATABASE="${{Postgres.PGDATABASE}}"
PGHOST="${{Postgres.PGHOST}}"
PGPASSWORD="${{Postgres.PGPASSWORD}}"
PGPORT="${{Postgres.PGPORT}}"
PGUSER="${{Postgres.PGUSER}}"
RAILWAY_DOCKERFILE_PATH="admin-panel.Dockerfile"
```

---

## ⚠️ EKSİK VARIABLES (EKLENMELİ!)

### 1. HOMESERVER_DOMAIN (KRİTİK! ⚠️)

**Neden Önemli:**
- Kullanıcı oluştururken domain'i belirler
- Eğer yoksa veya yanlışsa: `@user:localhost` oluşur (yanlış!)
- Doğru olmalı: `@user:matrix-synapse.up.railway.app`

**Railway'de Ekleyin:**
```
HOMESERVER_DOMAIN="matrix-synapse.up.railway.app"
```

### 2. SYNAPSE_URL (Önerilir)

**Neden Önemli:**
- Matrix Admin API'yi kullanmak için gerekli
- Kullanıcı oluştururken önce API'yi dener, sonra database'e yazar

**Railway'de Ekleyin:**
```
SYNAPSE_URL="https://matrix-synapse.up.railway.app"
```

### 3. ADMIN_PASSWORD (Opsiyonel ama Önerilir)

**Neden Önemli:**
- Admin panel login şifresi (şu an hardcoded: `admin123`)
- Güvenlik için environment variable'dan alınmalı

**Railway'de Ekleyin:**
```
ADMIN_PASSWORD="GüçlüBirŞifre123!"
```

---

## ✅ TAM VARIABLE LİSTESİ

Railway Dashboard → Admin Panel → **Variables** → **Add Variable**:

### Zorunlu:
```
HOMESERVER_DOMAIN="matrix-synapse.up.railway.app"
```

### Önerilen:
```
SYNAPSE_URL="https://matrix-synapse.up.railway.app"
ADMIN_PASSWORD="GüçlüBirŞifre123!"
```

### Zaten Var (Postgres Reference):
```
PGDATABASE="${{Postgres.PGDATABASE}}"
PGHOST="${{Postgres.PGHOST}}"
PGPASSWORD="${{Postgres.PGPASSWORD}}"
PGPORT="${{Postgres.PGPORT}}"
PGUSER="${{Postgres.PGUSER}}"
```

---

## 🎯 ADIM ADIM EKLEME

### Railway Dashboard'da:

1. **Railway Dashboard'a gidin:**
   - https://railway.app/dashboard
   - `cravexv5` projesini seçin
   - `considerate-adaptation` (Admin Panel) servisini seçin

2. **Variables sekmesine gidin:**
   - Admin Panel servisi → **Variables** sekmesi

3. **Yeni variable ekleyin:**
   - **"New Variable"** butonuna tıklayın
   - **Name:** `HOMESERVER_DOMAIN`
   - **Value:** `matrix-synapse.up.railway.app`
   - **"Add"** butonuna tıklayın

4. **Diğer variable'ları ekleyin:**
   - `SYNAPSE_URL` = `https://matrix-synapse.up.railway.app`
   - `ADMIN_PASSWORD` = `GüçlüBirŞifre123!` (opsiyonel)

5. **Redeploy yapın:**
   - Variables eklendikten sonra **Deployments** → **Redeploy**
   - Veya otomatik deploy başlayacak

---

## 🔍 DOĞRULAMA

### 1. Variables Kontrolü

Railway Dashboard → Admin Panel → **Variables**:
- ✅ `HOMESERVER_DOMAIN` = `matrix-synapse.up.railway.app`
- ✅ `SYNAPSE_URL` = `https://matrix-synapse.up.railway.app`
- ✅ PostgreSQL variables mevcut

### 2. Kullanıcı Oluşturma Testi

1. Admin Panel'e gidin: `https://considerate-adaptation-production.up.railway.app/`
2. Login yapın (admin / admin123)
3. Yeni kullanıcı oluşturun:
   - Username: `testuser`
   - Password: `Test123!`
4. Başarı mesajını kontrol edin

### 3. Veritabanında Kontrol

Railway Dashboard → PostgreSQL → **Query**:

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
WHERE name LIKE '%testuser%';
```

**Beklenen sonuç:**
- ✅ `@testuser:matrix-synapse.up.railway.app`
- ❌ `@testuser:localhost` (yanlış - HOMESERVER_DOMAIN eksik!)

---

## ⚠️ ÖNEMLİ NOTLAR

### HOMESERVER_DOMAIN Eksikse:
- ❌ Kullanıcılar `@user:localhost` olarak oluşur
- ❌ Element Web'de login çalışmaz
- ❌ Veritabanında yanlış domain görünür

### HOMESERVER_DOMAIN Doğruysa:
- ✅ Kullanıcılar `@user:matrix-synapse.up.railway.app` olarak oluşur
- ✅ Element Web'de login çalışır
- ✅ Veritabanında doğru domain görünür

---

## 📋 CHECKLIST

- [ ] Railway Dashboard → Admin Panel → Variables açtım
- [ ] `HOMESERVER_DOMAIN` = `matrix-synapse.up.railway.app` ekledim
- [ ] `SYNAPSE_URL` = `https://matrix-synapse.up.railway.app` ekledim (opsiyonel)
- [ ] `ADMIN_PASSWORD` ekledim (opsiyonel)
- [ ] Admin Panel'i redeploy ettim
- [ ] Kullanıcı oluşturma testi yaptım
- [ ] Veritabanında domain'i kontrol ettim

---

**SONUÇ:** `HOMESERVER_DOMAIN` variable'ını **MUTLAKA** ekleyin! Bu olmadan kullanıcılar yanlış domain ile oluşturulur.


