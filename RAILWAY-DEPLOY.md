# 🚂 Railway + Netlify Deployment Rehberi

## 🎯 Ne Deploy Ediyoruz?

- **Railway**: Matrix Synapse (Backend) - PostgreSQL + Redis
- **Netlify**: Element-web (Frontend)

---

## 📋 Adım 1: Railway'de Matrix Synapse Deploy

### 1.1 Railway Hesabı Oluştur

1. https://railway.app adresine git
2. **GitHub** ile giriş yap
3. Ücretsiz plan: **$5 ücretsiz kredi** + **500 saat/ay**

### 1.2 Yeni Proje Oluştur

**Seçenek A: GitHub Repo ile (ÖNERİLEN)**

1. Railway Dashboard → **New Project**
2. **Deploy from GitHub repo** seç
3. Repo'nuzu seç: `www-backup`
4. Root directory: `/` (proje kökü)

**Seçenek B: CLI ile**

```bash
# Railway CLI kur
npm install -g @railway/cli

# Login
railway login

# Proje oluştur
railway init

# Deploy
railway up
```

### 1.3 PostgreSQL Ekle

1. Railway Dashboard → Projenizi seç
2. **New** → **Database** → **PostgreSQL**
3. Otomatik environment variables eklenecek

### 1.4 Redis Ekle

1. Railway Dashboard → Projenizi seç
2. **New** → **Database** → **Redis**
3. Otomatik environment variables eklenecek

### 1.5 Environment Variables Ayarla

Railway Dashboard → Variables sekmesi:

```env
# PostgreSQL (Otomatik eklenir)
DATABASE_URL=postgresql://user:pass@host:port/db

# Opsiyonel: Manuel ekle
POSTGRES_PASSWORD=SuperGucluSifre2024!
SYNAPSE_SERVER_NAME=${RAILWAY_PUBLIC_DOMAIN}
ELEMENT_WEB_URL=https://your-element-web.netlify.app
```

### 1.6 Domain Al

1. Railway → Settings → **Generate Domain**
2. Size şöyle bir domain verecek: `your-project.up.railway.app`
3. Bu URL'i not alın! ✍️

---

## 📋 Adım 2: Netlify'da Element-web Deploy

### 2.1 Config.json Güncelle

Railway domain'inizi aldıktan sonra:

```bash
cd "C:\Users\Can Cakir\Desktop\www-backup\www\element-web"
notepad config.json
```

Değiştirin:
```json
{
    "default_server_config": {
        "m.homeserver": {
            "base_url": "https://YOUR-PROJECT.up.railway.app",
            "server_name": "YOUR-PROJECT.up.railway.app"
        }
    },
    ...
    "room_directory": {
        "servers": ["YOUR-PROJECT.up.railway.app"]
    }
}
```

### 2.2 Git'e Push

```bash
git add .
git commit -m "Railway + Netlify deployment ready"
git push
```

### 2.3 Netlify Deploy

**Yöntem 1: Dashboard (Kolay)**

1. https://netlify.app → **Add new site**
2. **Import from Git** → GitHub seç
3. Repo seç: `element-web`
4. Build settings:
   - Base directory: `www/element-web`
   - Build command: `yarn build`
   - Publish directory: `www/element-web/webapp`
5. **Deploy site** tıkla!

**Yöntem 2: Netlify CLI**

```bash
# CLI kur
npm install -g netlify-cli

# Login
netlify login

# Element-web dizinine git
cd "C:\Users\Can Cakir\Desktop\www-backup\www\element-web"

# Deploy
netlify deploy --prod
```

---

## 🔄 Adım 3: CORS Ayarları (ÖNEMLİ!)

Railway'deki Synapse config'ini güncelleyin:

```yaml
web_client_location: "https://your-element-web.netlify.app"
```

### Railway'de Config Güncelleme:

1. Railway Dashboard → Service seç
2. **Deployments** → En son deployment
3. **Logs** → Hataları kontrol et

Ya da:

```bash
railway run python -m synapse.app.homeserver --generate-config
```

---

## ✅ Test

### 1. Matrix Sunucu Test

```bash
curl https://YOUR-PROJECT.up.railway.app/_matrix/client/versions
```

Başarılı ise şöyle bir response göreceksiniz:
```json
{
  "versions": ["r0.0.1", "r0.1.0", ...]
}
```

### 2. Element-web Test

1. https://your-element-web.netlify.app adresini aç
2. **Create Account** veya **Sign In** deneyin
3. Sunucu otomatik algılanmalı

---

## 💰 Ücretsiz Plan Limitleri

### Railway (Ücretsiz)
- ✅ $5 kredi/ay
- ✅ 500 execution saat/ay
- ✅ Postgres + Redis dahil
- ⚠️ Küçük-orta projeler için yeterli

### Netlify (Ücretsiz)
- ✅ 100 GB bandwidth/ay
- ✅ 300 build dakika/ay
- ✅ Otomatik HTTPS
- ✅ Global CDN

---

## 🔧 Sorun Giderme

### Railway Build Hatası

```bash
# Logs kontrol et
railway logs

# Manuel restart
railway restart
```

### Netlify Build Hatası

```bash
# Logs kontrol et
netlify logs

# Local test
yarn build
```

### Matrix Bağlantı Hatası

1. Railway domain'i kontrol et
2. `config.json`'da doğru URL olduğundan emin ol
3. CORS ayarlarını kontrol et

---

## 🎉 Başarılı Deploy Sonrası

Her iki servis de çalışıyor olmalı:

- ✅ **Matrix Synapse**: `https://YOUR-PROJECT.up.railway.app`
- ✅ **Element-web**: `https://your-element-web.netlify.app`

**Artık tamamen ücretsiz ve canlıda!** 🚀

---

## 📊 Monitoring

### Railway
- Dashboard → Metrics
- CPU, RAM, Network kullanımı

### Netlify
- Dashboard → Analytics
- Bandwidth, build zamanı

---

**Hazır mısınız? Hadi başlayalım!** 🔥

