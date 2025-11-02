# Matrix Synapse Railway Deploy Rehberi

## 🚀 Adım Adım Kurulum

### 1️⃣ YENİ SERVİS OLUŞTUR

Railway Dashboard → Projeniz:
- **"New"** tıklayın
- **"GitHub Repo"** seçin
- Repository: `daiteknoloji/Cravexv5`
- **"Add Service"** tıklayın

Servis otomatik deploy başlayacak ama **DURUN!** ❌  
Henüz ayarları yapmadık!

---

### 2️⃣ SERVİS AYARLARI

Yeni oluşan servise tıklayın → **Settings**

#### **General:**
- **Service Name:** `matrix-synapse` (manuel yazın)

#### **Source:**
- **Root Directory:** `/` (boş bırakın)
- **Branch:** `main` ✅

#### **Build:**
- **Builder:** **Dockerfile** (dropdown'dan seçin)
- **Dockerfile Path:** `Dockerfile.synapse` (manuel yazın)

**KAYDET!** ✅

---

### 3️⃣ ENVIRONMENT VARIABLES

**Settings** → **Variables** sekmesi

Şu değişkenleri **TEK TEK** ekleyin:

```
SYNAPSE_SERVER_NAME=matrix-synapse-production.up.railway.app
```

```
WEB_CLIENT_LOCATION=https://surprising-emotion-production.up.railway.app
```

PostgreSQL bağlantısı için (Postgres servisinizin adı `Postgres` ise):

```
POSTGRES_HOST=${{Postgres.PGHOST}}
```

```
POSTGRES_PORT=${{Postgres.PGPORT}}
```

```
POSTGRES_USER=${{Postgres.PGUSER}}
```

```
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
```

```
POSTGRES_DB=${{Postgres.PGDATABASE}}
```

**NOT:** `${{Postgres.PGHOST}}` Railway'de otomatik referans verir!  
Eğer PostgreSQL servisinizin adı farklıysa (örn: `postgres-db`), o zaman:
```
POSTGRES_HOST=${{postgres-db.PGHOST}}
```

**KAYDET!** ✅

---

### 4️⃣ NETWORKING

**Settings** → **Networking** → **Public Networking**

- **"Generate Domain"** tıklayın
- Domain otomatik oluşacak: `matrix-synapse-production.up.railway.app`
- **"Target Port"** girin: `8008`

**KAYDET!** ✅

---

### 5️⃣ DEPLOY BAŞLAT

**Deployments** sekmesine gidin:
- Otomatik deploy başlayacak
- **"Deploying..."** yazacak
- Logs'u izleyin

**Beklenen Loglar:**
```
🚀 Starting Matrix Synapse on Railway...
🔑 Generating signing key...
✅ Configuration complete!
🚀 Starting Synapse...
```

**Deploy süresi:** ~2-3 dakika

---

### 6️⃣ TEST

Deploy tamamlandığında (yeşil ✅), tarayıcıda açın:

```
https://matrix-synapse-production.up.railway.app/_matrix/client/versions
```

**Beklenen Sonuç:**
```json
{
  "versions": ["r0.0.1", "r0.1.0", ...]
}
```

✅ **BAŞARILI!**

---

## 🐛 Sorun Giderme

### Hata: "Dockerfile not found"

**Çözüm:** `Dockerfile.synapse` dosyası repo'da var mı kontrol edin:
- GitHub → `daiteknoloji/Cravexv5` → `Dockerfile.synapse` dosyası görünüyor mu?

### Hata: "Database connection failed"

**Çözüm:** Variables'ları kontrol edin:
- `POSTGRES_HOST` değeri `${{Postgres.PGHOST}}` şeklinde mi?
- PostgreSQL servisi **çalışıyor** mu?

### Hata: "Port 8008 already in use"

**Çözüm:** Başka servis 8008 kullanıyor olabilir. Kontrol edin.

---

## ✅ BAŞARILI KURULUM SONRASI

### Admin Kullanıcısı Oluştur

PowerShell:
```powershell
$body = @{
    username = "admin"
    password = "Admin@2024!Guclu"
    admin = $true
    nonce = "random123"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://matrix-synapse-production.up.railway.app/_synapse/admin/v1/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

### Synapse Admin UI'a Giriş

URL: `https://synapse-admin-ui-production.up.railway.app`

- Kullanıcı: `@admin:matrix-synapse-production.up.railway.app`
- Parola: `Admin@2024!Guclu`
- Ana Sunucu URL: `https://matrix-synapse-production.up.railway.app`

---

## 🎉 TAMAMLANDI!

Artık Matrix Synapse Railway'de çalışıyor! 🚀

