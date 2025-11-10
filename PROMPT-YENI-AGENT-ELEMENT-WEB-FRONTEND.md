# 🎯 YENİ AGENT PROMPT - ELEMENT WEB FRONTEND DEĞİŞİKLİKLERİ

## 📋 PROJE GENEL BAKIŞ

Bu proje, **Matrix Synapse** backend + **Element Web** frontend + **Custom Admin Panel** içeren tam bir mesajlaşma platformudur. Şu anda **v3** tag'i ile GitHub'da kayıtlı ve tüm fonksiyonlar çalışır durumda.

**GitHub Repository:** `https://github.com/daiteknoloji/Cravexv5`  
**Son Tag:** `v3` (46e199a)  
**Çalışma Dizini:** `C:\Users\Can Cakir\Desktop\www-backup`

---

## 🏗️ MİMARİ YAPISI

### Servisler ve Portlar:

| Servis | Port | Açıklama | Lokal URL | Railway URL |
|--------|------|----------|-----------|-------------|
| **Element Web** | 8080 | Mesajlaşma frontend (React) | http://localhost:8080 | https://surprising-emotion-production.up.railway.app |
| **Matrix Synapse** | 8008 | Backend API (Python) | http://localhost:8008 | https://matrix-synapse.up.railway.app |
| **Custom Admin Panel** | 9000 | Railway Admin Panel (Flask/Python) | http://localhost:9000 | https://considerate-adaptation-production.up.railway.app |
| **PostgreSQL** | 5432 | Veritabanı | localhost:5432 | Railway PostgreSQL (internal) |
| **Redis** | 6379 | Cache | localhost:6379 | Railway Redis (internal) |

### Servis İlişkileri:

```
KULLANICI (Browser)
    ↓
ELEMENT WEB (React Frontend - Port 8080)
    ↓
MATRIX SYNAPSE API (Backend - Port 8008)
    ↓
POSTGRESQL (Database - Port 5432)
    ↓
REDIS (Cache - Port 6379)
```

---

## 📁 PROJE YAPISI

### Ana Klasörler:

```
www-backup/
├── www/
│   ├── element-web/          → Element Web frontend (React/TypeScript)
│   │   ├── src/              → Kaynak kodlar
│   │   ├── public/           → Statik dosyalar
│   │   ├── package.json      → Dependencies
│   │   └── config.json       → Element Web config
│   └── admin/                → Synapse Admin (React)
│       └── src/
├── admin-panel/              → Custom Admin Panel (Flask/Python)
│   ├── admin-panel-server.py → Backend API
│   └── admin-panel-ui-modern.html → Frontend UI
├── synapse-config/           → Matrix Synapse config dosyaları
│   └── homeserver.yaml       → Synapse ana config
├── docker-compose.yml        → Docker servisleri
└── *.ps1                     → PowerShell scriptleri
```

### Element Web Önemli Dosyalar:

- **`www/element-web/src/`** - Ana React/TypeScript kaynak kodları
- **`www/element-web/public/config.json`** - Element Web konfigürasyonu
- **`www/element-web/package.json`** - NPM dependencies
- **`www/element-web/.env`** - Environment variables (varsa)

---

## 🌐 RAILWAY DEPLOYMENT BİLGİLERİ

### Railway Servisleri:

1. **considerate-adaptation** (Admin Panel)
   - **URL:** https://considerate-adaptation-production.up.railway.app
   - **Type:** Python Flask
   - **Source:** `admin-panel/` klasörü
   - **Port:** 8080 (Railway otomatik)

2. **cravexv5** (Matrix Synapse)
   - **URL:** https://matrix-synapse.up.railway.app
   - **Type:** Python (Synapse)
   - **Port:** 8008

3. **surprising-emotion** (Element Web)
   - **URL:** https://surprising-emotion-production.up.railway.app
   - **Type:** Static Site / Node.js
   - **Source:** `www/element-web/` klasörü

### Railway Environment Variables:

#### Admin Panel (considerate-adaptation):
```env
HOMESERVER_DOMAIN=matrix-synapse.up.railway.app
SYNAPSE_URL=https://matrix-synapse.up.railway.app
ADMIN_PASSWORD=GüçlüBirŞifre123!
PGHOST=postgres.railway.internal
PGDATABASE=railway
PGUSER=postgres
PGPASSWORD=[Railway otomatik]
PGPORT=5432
```

#### Matrix Synapse (cravexv5):
```env
SYNAPSE_SERVER_NAME=matrix-synapse.up.railway.app
POSTGRES_HOST=postgres.railway.internal
POSTGRES_DB=railway
POSTGRES_USER=postgres
POSTGRES_PASSWORD=[Railway otomatik]
REDIS_HOST=redis.railway.internal
REDIS_PORT=6379
```

#### Element Web (surprising-emotion):
- **Not:** Element Web genellikle environment variables kullanmaz, `config.json` kullanır.

---

## 💾 POSTGRESQL VERİTABANI

### Bağlantı Bilgileri:

**Lokal:**
- Host: `localhost`
- Port: `5432`
- Database: `synapse`
- User: `synapse_user`
- Password: `SuperGucluSifre2024!`

**Railway:**
- Host: `postgres.railway.internal` (internal) veya Railway dashboard'dan alınan public URL
- Port: `5432`
- Database: `railway` (genellikle)
- User: `postgres`
- Password: Railway dashboard'dan alınır

### Önemli Tablolar:

| Tablo | Açıklama |
|-------|----------|
| `users` | Kullanıcı bilgileri (password_hash, deactivated, admin, vb.) |
| `rooms` | Oda bilgileri (room_id, creator, is_public) |
| `room_memberships` | Oda üyelikleri (room_id, user_id, membership) |
| `events` | Tüm eventler (mesajlar, room events, vb.) |
| `event_json` | Event JSON içerikleri (mesaj içerikleri, media URLs) |
| `access_tokens` | Kullanıcı access token'ları |
| `profiles` | Kullanıcı profil bilgileri (displayname) |
| `user_directory` | Kullanıcı dizini |
| `media_cache` | Admin panel'in media cache'i |

### Önemli SQL Sorguları:

```sql
-- Tüm kullanıcıları listele
SELECT name, password_hash, deactivated, admin, creation_ts 
FROM users 
ORDER BY creation_ts DESC;

-- Tüm odaları listele
SELECT room_id, creator, is_public, 
       (SELECT COUNT(*) FROM room_memberships WHERE room_id = r.room_id AND membership = 'join') as member_count
FROM rooms r
ORDER BY member_count DESC;

-- Oda mesajlarını listele
SELECT e.event_id, e.room_id, e.sender, e.type, ej.json::json->'content'->>'body' as body
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE e.room_id = '!ROOM_ID' AND e.type = 'm.room.message'
ORDER BY e.origin_server_ts DESC;
```

---

## 🔐 GİRİŞ BİLGİLERİ

### Element Web:
- **Username:** `admin` (veya `@admin:matrix-synapse.up.railway.app`)
- **Password:** `GüçlüBirŞifre123!` (Railway'de)
- **Homeserver:** `https://matrix-synapse.up.railway.app`

### Custom Admin Panel:
- **Username:** `admin`
- **Password:** `admin123` (hardcoded, Railway'de `ADMIN_PASSWORD` env var kullanılır)

---

## 🎨 ELEMENT WEB FRONTEND YAPISI

### Teknoloji Stack:
- **Framework:** React 18+
- **Language:** TypeScript
- **Build Tool:** Vite (muhtemelen)
- **State Management:** React hooks, Matrix SDK
- **Styling:** CSS Modules veya SCSS

### Önemli Klasörler:

```
www/element-web/src/
├── components/          → React componentleri
│   ├── views/          → Sayfa görünümleri
│   ├── structures/     → Ana yapılar (RoomView, MatrixChat)
│   └── ...
├── stores/             → State management (RoomViewStore, etc.)
├── utils/              → Yardımcı fonksiyonlar
├── i18n/               → Çeviriler
└── index.tsx           → Ana entry point
```

### Element Web Config (`public/config.json`):

```json
{
  "default_server_config": {
    "m.homeserver": {
      "base_url": "https://matrix-synapse.up.railway.app"
    }
  },
  "default_server_name": "matrix-synapse.up.railway.app",
  "brand": "Element",
  "integrations_ui_url": "...",
  "integrations_rest_url": "...",
  "bug_report_endpoint_url": "...",
  "defaultCountryCode": "TR",
  "showLabsSettings": true,
  "features": {
    "feature_new_spinner": true,
    "feature_pinning": true,
    "feature_custom_status": true,
    "feature_custom_tags": true,
    "feature_state_counters": true
  }
}
```

### Önemli Componentler:

1. **MatrixChat** (`src/components/structures/MatrixChat.tsx`)
   - Ana chat uygulaması wrapper'ı

2. **RoomView** (`src/components/structures/RoomView.tsx`)
   - Oda görünümü (mesaj listesi, input, vb.)

3. **MessageComposer** (`src/components/views/rooms/MessageComposer.tsx`)
   - Mesaj yazma alanı

4. **TimelinePanel** (`src/components/views/rooms/TimelinePanel.tsx`)
   - Mesaj timeline'ı

---

## ✅ v3'TE ÇALIŞAN ÖZELLİKLER

### Admin Panel Özellikleri:
- ✅ Kullanıcı yönetimi (oluşturma, silme, şifre değiştirme)
- ✅ Oda yönetimi (listeleme, üye ekleme/çıkarma)
- ✅ Mesaj görüntüleme (pagination, filtreleme)
- ✅ Media görüntüleme (resim, dosya, ses mesajı)
- ✅ DM kontrolü (`is_direct` flag + oda adı kontrolü)
- ✅ Bildirim gönderme (oda sahibinden admin davet etme)
- ✅ Silinen kullanıcılar listesi
- ✅ Excel/JSON export

### Element Web Özellikleri:
- ✅ Mesajlaşma (text, image, file, voice)
- ✅ Oda oluşturma/katılma
- ✅ Kullanıcı profilleri
- ✅ Bildirimler
- ✅ Media görüntüleme
- ✅ Responsive tasarım

---

## 🚨 ÖNEMLİ NOTLAR

### Frontend Değişiklikleri İçin:

1. **Element Web'i çalıştırma:**
   ```powershell
   cd www/element-web
   yarn install  # veya npm install
   yarn start    # veya npm start
   ```

2. **Build için:**
   ```powershell
   yarn build    # Production build
   ```

3. **Config değişiklikleri:**
   - `public/config.json` dosyasını düzenle
   - Railway'de deploy etmek için `www/element-web/` klasörünü push et

4. **Matrix SDK kullanımı:**
   - Element Web, Matrix JavaScript SDK kullanır
   - `matrix-js-sdk` paketi ile Matrix API'ye bağlanır
   - Client instance: `MatrixClient`

5. **State Management:**
   - React hooks kullanılır
   - `RoomViewStore` gibi store'lar var
   - Matrix SDK event'leri dinlenir

### Railway Deploy İçin:

1. **Element Web deploy:**
   - Railway'de `surprising-emotion` servisi
   - Source: `www/element-web/` klasörü
   - Build command: `yarn build` veya `npm run build`
   - Output: `dist/` veya `build/` klasörü

2. **Auto-deploy:**
   - Railway Git bağlantısı aktif
   - `main` branch'e push → otomatik deploy

---

## 🔧 YARDIMCI KOMUTLAR

### Lokal Geliştirme:

```powershell
# Tüm servisleri başlat
.\BASLAT.ps1

# Durum kontrolü
.\DURUM.ps1

# Tüm servisleri durdur
.\DURDUR.ps1

# Element Web'i başlat
cd www/element-web
yarn start
```

### Railway İşlemleri:

```powershell
# Git push (auto-deploy tetikler)
git add .
git commit -m "message"
git push origin main

# Railway CLI (varsa)
railway status
railway logs
railway redeploy
```

---

## 📝 SON DEĞİŞİKLİKLER (v3)

### v3 Tag İçeriği:

1. **DM Kontrolü Düzeltildi:**
   - `is_direct` flag kontrolü eklendi
   - Oda adı kontrolü eklendi (DM'ler genelde adı yok)
   - Backend ve frontend'de kontrol var

2. **Bildirim Sorunu Çözüldü:**
   - Oda sahibinden admin davet etme eklendi
   - Admin odaya ekleniyor → invite gönderebiliyor
   - Bildirimler Element Web'e gidiyor

3. **Çift Hata Mesajı Sorunu Çözüldü:**
   - Frontend'de API çağrısından önce DM kontrolü
   - Tek hata mesajı gösteriliyor

---

## 🎯 FRONTEND DEĞİŞİKLİKLERİ İÇİN ÖNERİLER

1. **Element Web'i değiştirirken:**
   - `www/element-web/src/` klasöründe çalış
   - TypeScript type'larına dikkat et
   - Matrix SDK API'lerini kullan
   - Component lifecycle'ına dikkat et

2. **Styling için:**
   - CSS Modules veya SCSS kullan
   - Element Web'in mevcut stil sistemine uyumlu ol
   - Responsive tasarımı koru

3. **Test için:**
   - Lokal'de `yarn start` ile test et
   - Railway'de deploy etmeden önce build'i kontrol et
   - Matrix Synapse API'ye bağlantıyı kontrol et

4. **Deploy için:**
   - Değişiklikleri commit et
   - `main` branch'e push et
   - Railway otomatik deploy edecek
   - Logları kontrol et

---

## 🔗 ÖNEMLİ LİNKLER

- **GitHub Repo:** https://github.com/daiteknoloji/Cravexv5
- **Railway Dashboard:** https://railway.app
- **Element Web Docs:** https://element.io/develop
- **Matrix Spec:** https://spec.matrix.org/
- **Matrix JS SDK:** https://github.com/matrix-org/matrix-js-sdk

---

## ⚠️ DİKKAT EDİLMESİ GEREKENLER

1. **Hiçbir fonksiyonu bozma** - Mevcut özellikler çalışır durumda
2. **Backend API'yi değiştirme** - Sadece frontend değişiklikleri yap
3. **Database şemasını değiştirme** - Sadece frontend'deki görünümü değiştir
4. **Environment variables'ı değiştirme** - Railway'deki ayarları koru
5. **v3 tag'ini koru** - Yeni değişiklikler için yeni branch/commit kullan

---

## 📞 YARDIM İÇİN

- **Proje Dokümantasyonu:** `PROJE-ANALIZ-VE-MAPPING-OZET.md`
- **Kullanım Kılavuzu:** `KULLANIM-KILAVUZU.md`
- **Railway Ayarları:** `RAILWAY-SETTINGS-BACKUP-REHBER.md`

---

**Son Güncelleme:** v3 (46e199a) - DM kontrolü ve bildirim sorunu çözüldü  
**Durum:** ✅ Tüm fonksiyonlar çalışır durumda

