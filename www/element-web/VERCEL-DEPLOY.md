# 🚀 Vercel Deployment Rehberi

## 📋 Ön Hazırlık

### 1️⃣ Matrix Homeserver Ayarları

**ÖNEMLİ:** Şu anda `config.json` dosyanızda local IP adresi var (`172.20.10.3:8008`).

Production'da çalışması için Matrix sunucunuzun **public domain veya IP** adresi gerekli:

#### Seçenek A: Domain kullanıyorsanız
```json
"base_url": "https://matrix.yourdomain.com",
"server_name": "matrix.yourdomain.com"
```

#### Seçenek B: Public IP kullanıyorsanız  
```json
"base_url": "http://YOUR_PUBLIC_IP:8008",
"server_name": "YOUR_PUBLIC_IP"
```

### 2️⃣ Config Dosyasını Güncelle

Deploy öncesi `config.json` dosyasını düzenleyin:
1. `config.production.json` dosyasını açın
2. `YOUR-MATRIX-SERVER.com` kısımlarını gerçek sunucu adresinizle değiştirin
3. `config.json` dosyasını bu ayarlarla güncelleyin

## 🎯 Vercel ile Deploy

### Yöntem 1: Vercel CLI (Hızlı)

```bash
# 1. Vercel CLI'ı yükleyin (global)
npm install -g vercel

# 2. Vercel'e login olun
vercel login

# 3. Deploy edin
vercel

# İlk deploy için sorulacak sorular:
# - Set up and deploy? → Y
# - Which scope? → Hesabınızı seçin
# - Link to existing project? → N
# - Project name? → element-web (veya istediğiniz isim)
# - In which directory is your code located? → ./

# 4. Production deploy
vercel --prod
```

### Yöntem 2: Vercel Dashboard (Kolay)

1. **GitHub'a push edin:**
   ```bash
   git add .
   git commit -m "Vercel deployment hazırlığı"
   git push origin develop
   ```

2. **Vercel'e gidin:**
   - https://vercel.com adresine gidin
   - GitHub ile giriş yapın
   - "Add New Project" tıklayın
   - GitHub repo'nuzu seçin

3. **Build ayarları (Otomatik algılanacak):**
   - Framework Preset: `Other`
   - Build Command: `yarn build`
   - Output Directory: `webapp`
   - Install Command: `yarn install`

4. **Deploy** butonuna basın!

## ⚙️ Environment Variables (Opsiyonel)

Eğer farklı ortamlar için farklı config'ler kullanmak isterseniz:

1. Vercel Dashboard → Settings → Environment Variables
2. Ekleyin:
   - `MATRIX_HOMESERVER_URL` → Matrix sunucu URL'niz
   - `MATRIX_SERVER_NAME` → Matrix sunucu adınız

## 🔒 HTTPS ve Domain

### Vercel otomatik sağlar:
- ✅ HTTPS sertifikası (Let's Encrypt)
- ✅ `yourproject.vercel.app` domain
- ✅ Custom domain bağlama (ücretsiz)

### Custom domain eklemek:
1. Vercel Dashboard → Project → Settings → Domains
2. Domain adınızı girin
3. DNS kayıtlarını gösterdiği gibi ekleyin

## 🎉 Deploy Sonrası

Deploy tamamlandıktan sonra:

1. **URL'i açın** (örn: `https://element-web.vercel.app`)
2. **Matrix sunucunuza erişimi test edin**
3. **Login olmayı deneyin**

## ⚠️ Yaygın Sorunlar

### 1. Matrix sunucuya erişilemiyor
- Matrix sunucunuzun **CORS** ayarlarını kontrol edin
- Synapse için `homeserver.yaml`:
  ```yaml
  web_client_location: https://your-element-vercel-app.vercel.app
  
  listeners:
    - port: 8008
      bind_addresses: ['0.0.0.0']
      type: http
      x_forwarded: true
      resources:
        - names: [client, federation]
          compress: false
  ```

### 2. Config.json yüklenmiyor
- `config.json` dosyasının `webapp/` klasöründe olduğundan emin olun
- Build komutunu kontrol edin

### 3. Build hatası
- `node_modules` silin ve `yarn install` tekrar çalıştırın
- Node.js versiyonunu kontrol edin (>=20.0.0)

## 📊 Monitoring

Vercel otomatik sağlar:
- Real-time logs
- Performance metrics
- Error tracking
- Analytics

Dashboard'dan hepsini görebilirsiniz!

## 🔄 Otomatik Deployment

Git repo bağlıysa, her `git push` otomatik deploy tetikler:
- `main` branch → Production
- Diğer branch'ler → Preview deployment

---

**Hazır mısınız?** `vercel` komutunu çalıştırın! 🚀

