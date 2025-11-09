# Netlify Config Sorunu

## 🔍 Sorun

Loglar gösteriyor ki:
- Element Web `hsName: "cravex1-production.up.railway.app"` kullanıyor (YANLIŞ)
- Ama `config.json`'da `matrix-synapse-production.up.railway.app` var (DOĞRU)
- Netlify build'i eski config'i kullanıyor olabilir

## 🛠️ Çözüm

### 1. Netlify Build Cache'ini Temizle

Netlify Dashboard'dan:
1. **Netlify Dashboard** → **cozy-dragon-54547b** → **"Deploys"**
2. **"Trigger deploy"** → **"Clear cache and deploy site"** seçeneğini işaretleyin
3. **"Deploy site"** butonuna tıklayın

### 2. Browser Cache'ini Temizle

Browser'da:
1. **Ctrl + Shift + Delete** (Windows) veya **Cmd + Shift + Delete** (Mac)
2. **"Cached images and files"** seçeneğini işaretleyin
3. **"Clear data"** butonuna tıklayın
4. Sayfayı yenileyin (**Ctrl + F5** veya **Cmd + Shift + R**)

### 3. Config.json'u Kontrol Et

`www/element-web/config.json` dosyasında şunlar olmalı:
```json
{
    "default_server_config": {
        "m.homeserver": {
            "base_url": "https://matrix-synapse-production.up.railway.app",
            "server_name": "matrix-synapse-production.up.railway.app"
        }
    }
}
```

### 4. Netlify Build Loglarını Kontrol Et

Netlify Dashboard → **"Deploys"** → Son build'in loglarını kontrol edin:
- `config.json` dosyasının doğru kopyalandığını doğrulayın
- Build'in başarılı olduğunu doğrulayın

## ⚠️ Önemli Not

Netlify build'i cache kullanıyor olabilir. **"Clear cache and deploy site"** seçeneğini kullanarak cache'i temizleyin.

## 🔍 Kontrol

Deploy tamamlandıktan sonra:
1. Browser cache'ini temizleyin
2. `https://cozy-dragon-54547b.netlify.app/config.json` adresini açın
3. `base_url` ve `server_name` değerlerinin `matrix-synapse-production.up.railway.app` olduğunu doğrulayın


