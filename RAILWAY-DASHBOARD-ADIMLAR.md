# 🚂 RAILWAY DASHBOARD ADIMLARI

**Railway dashboard'da ne yapacaksınız - Adım adım**

---

## 📊 GENEL BAKIŞ

Railway'de **3 servis** oluşturacaksınız:

```
┌─────────────────────────────────────────┐
│         RAILWAY PROJECT                 │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────┐      │
│  │  1. PostgreSQL (Database)    │      │
│  │     - Otomatik kurulum       │      │
│  │     - SQL veritabanı         │      │
│  └──────────────────────────────┘      │
│                                         │
│  ┌──────────────────────────────┐      │
│  │  2. Matrix Synapse           │      │
│  │     - Backend API            │      │
│  │     - Port 8008              │      │
│  │     - PostgreSQL'e bağlı     │      │
│  └──────────────────────────────┘      │
│                                         │
│  ┌──────────────────────────────┐      │
│  │  3. Admin Panel              │      │
│  │     - Mesaj okuma paneli     │      │
│  │     - Port 9000              │      │
│  │     - PostgreSQL'e bağlı     │      │
│  └──────────────────────────────┘      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🗄️ SQL NEDİR? (AÇIKLAMA)

### PostgreSQL = SQL Veritabanı

**SQL (Structured Query Language)** = Veritabanı dili

Railway'de kullanacağınız **PostgreSQL**, bir SQL veritabanı sistemidir:

- ✅ **Mesajları** saklar
- ✅ **Kullanıcıları** saklar
- ✅ **Odaları** saklar
- ✅ **Tüm chat verilerini** saklar

**Basitçe:** PostgreSQL = Verilerinizin saklandığı yer (SQL database)

Railway bunu **otomatik** kuracak, siz **hiçbir şey yapmanıza gerek yok**!

---

## 🎯 ADIM ADIM RAILWAY KURULUMU

### ADIM 1: Railway'e Giriş Yap

1. https://railway.app
2. **Start a New Project** tıkla
3. GitHub ile giriş yap (önerilen)

---

### ADIM 2: Yeni Proje Oluştur

1. **Dashboard** → **New Project**
2. İsim ver: `Cravex Chat`
3. **Empty Project** seç

---

### ADIM 3: PostgreSQL Ekle (Database)

#### 3.1 Database Servis Oluştur

1. Proje içinde **New** → **Database** → **Add PostgreSQL**
2. Railway otomatik kuracak (30 saniye)
3. ✅ PostgreSQL hazır!

#### 3.2 Otomatik Oluşan Variables

Railway otomatik bu değişkenleri oluşturur:

```bash
PGHOST=containers-us-west-xxx.railway.app
PGPORT=5432
PGUSER=postgres
PGPASSWORD=xxxxxxxxxxxxx
PGDATABASE=railway
DATABASE_URL=postgresql://postgres:xxx@host:5432/railway
```

**Bu değişkenleri not almaya gerek YOK!** Railway otomatik paylaşır.

---

### ADIM 4: Matrix Synapse Servis Ekle

#### 4.1 GitHub Repo Bağla

1. Proje içinde **New** → **GitHub Repo**
2. Repo seç: `www-backup` (sizin repo adınız)
3. **Deploy** tıkla

#### 4.2 Settings Ayarla

1. Service seçiliyken → **Settings** sekmesi
2. **Root Directory**: `/` (değiştirme)
3. **Start Command**: `/start.sh` (otomatik algılanır)

#### 4.3 Variables Ekle

**Variables** sekmesi → **New Variable**

Her satırı ayrı ayrı ekleyin:

```bash
# PostgreSQL (Reference variables)
POSTGRES_HOST=${{Postgres.PGHOST}}
POSTGRES_PORT=${{Postgres.PGPORT}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
POSTGRES_DB=${{Postgres.PGDATABASE}}

# Synapse Config
SYNAPSE_SERVER_NAME=${{RAILWAY_PUBLIC_DOMAIN}}
WEB_CLIENT_LOCATION=https://element-xxx.netlify.app

# Secrets (ÖNEMLİ: Değiştirin!)
REGISTRATION_SHARED_SECRET=SuperGizliKayitAnahtari2024!XyZ
MACAROON_SECRET_KEY=SuperGizliMacaroon2024!AbC
FORM_SECRET=SuperGizliForm2024!DeF
```

**NOT:** 
- `${{Postgres.PGHOST}}` = PostgreSQL servisinden otomatik al
- `WEB_CLIENT_LOCATION` = Netlify'den alacağınız Element Web URL'i (sonra güncelleyin)
- Tüm SECRET değerlerini **mutlaka değiştirin!**

#### 4.4 Domain Al

1. **Settings** → **Networking** → **Generate Domain**
2. Domain oluşacak: `synapse-production-xxxx.up.railway.app`
3. **Bu URL'i not alın!** ✍️ (Netlify'de kullanacaksınız)

---

### ADIM 5: Admin Panel Servis Ekle

#### 5.1 Yeni Servis Oluştur

1. **Aynı projede** → **New** → **GitHub Repo**
2. **Aynı repo'yu** seç: `www-backup`
3. **Deploy** tıkla

#### 5.2 Settings Ayarla

1. **Settings** sekmesi
2. **Custom Start Command** (önemli!):
   ```
   python -u admin-panel-server.py
   ```
3. **Root Directory**: `/` (değiştirme)

#### 5.3 Variables Ekle

**Variables** sekmesi → **New Variable**

```bash
# PostgreSQL (Shared from Postgres service)
PGHOST=${{Postgres.PGHOST}}
PGPORT=${{Postgres.PGPORT}}
PGUSER=${{Postgres.PGUSER}}
PGPASSWORD=${{Postgres.PGPASSWORD}}
PGDATABASE=${{Postgres.PGDATABASE}}

# Flask Config
PORT=9000
FLASK_ENV=production
```

#### 5.4 Domain Al

1. **Settings** → **Networking** → **Generate Domain**
2. Domain oluşacak: `admin-production-xxxx.up.railway.app`
3. **Bu URL'i not alın!** ✍️

---

## ✅ RAILWAY TAMAMLANDI!

### Not Aldığınız URL'ler:

```
✍️ Synapse URL: https://synapse-production-xxxx.up.railway.app
✍️ Admin Panel URL: https://admin-production-xxxx.up.railway.app
```

Bu URL'leri **Netlify config güncellemesi** için kullanacaksınız!

---

## 🔍 DEPLOYMENT KONTROLÜ

### Her Servisin Durumu:

1. **PostgreSQL**: 
   - Status: **Active** ✅
   - Variables: Otomatik oluştu ✅

2. **Matrix Synapse**:
   - Status: **Deploying...** → **Active** ✅
   - Logs: `Starting Matrix Synapse on Railway...` ✅
   - Domain: Oluşturuldu ✅

3. **Admin Panel**:
   - Status: **Deploying...** → **Active** ✅
   - Logs: `CRAVEX ADMIN PANEL` ✅
   - Domain: Oluşturuldu ✅

---

## 🧪 TEST ETME

### 1. Synapse API Test

Tarayıcıda açın:
```
https://synapse-production-xxxx.up.railway.app/_matrix/client/versions
```

Başarılı ise:
```json
{
  "versions": ["r0.0.1", "r0.1.0", ...]
}
```

### 2. Admin Panel Test

Tarayıcıda açın:
```
https://admin-production-xxxx.up.railway.app
```

Login ekranı görmelisiniz:
- Username: `admin`
- Password: `admin123`

---

## 📊 RAILWAY VARIABLES REFERANS TABLOSU

| Variable | Nereden Gelir? | Örnek Değer |
|----------|----------------|-------------|
| `${{Postgres.PGHOST}}` | PostgreSQL servisinden | containers-us-west-xxx.railway.app |
| `${{Postgres.PGPORT}}` | PostgreSQL servisinden | 5432 |
| `${{Postgres.PGUSER}}` | PostgreSQL servisinden | postgres |
| `${{Postgres.PGPASSWORD}}` | PostgreSQL servisinden | xxxx (otomatik) |
| `${{Postgres.PGDATABASE}}` | PostgreSQL servisinden | railway |
| `${{RAILWAY_PUBLIC_DOMAIN}}` | Railway otomatik | synapse-production-xxxx.up.railway.app |

---

## 💰 MALIYET TAKİBİ

Railway Dashboard → **Usage** sekmesi:

- CPU kullanımı
- Memory kullanımı
- Network kullanımı
- **Tahmini maliyet**

**İlk ay:** $5 ücretsiz kredi
**Sonrası:** ~$12-18/ay (kullanıma göre)

---

## 🔧 SORUN GİDERME

### Deployment Failed

1. **Logs** sekmesine git
2. Hata mesajını oku
3. Yaygın hatalar:
   - `POSTGRES_HOST not set` → Variables kontrol et
   - `Port already in use` → Birden fazla servis aynı port kullanıyor
   - `Build failed` → Dockerfile hatası (nadiren olur)

### Variables Paylaşılmıyor

1. PostgreSQL servisinin adı `Postgres` olmalı
2. `${{Postgres.PGHOST}}` syntax doğru yazılmalı
3. Servislerin aynı projede olması gerekli

---

## 📚 SONRAKİ ADIMLAR

Railway deployment tamamlandıktan sonra:

1. ✅ **Netlify'deki config'leri güncelle** (Synapse URL ile)
2. ✅ **Element Web'i yeniden deploy et**
3. ✅ **Test et**
4. 🎉 **Canlıda!**

Detaylı adımlar: `RAILWAY-NETLIFY-DEPLOYMENT-GUIDE.md`

---

**Başarılar! Railway deployment'ı bu kadar basit!** 🚀

