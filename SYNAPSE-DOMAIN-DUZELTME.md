# Synapse Domain Düzeltme - Kullanıcıları Koruyarak

## 🔍 Sorun

Veritabanında `cravexv5-production.up.railway.app` domain'inde kullanıcılar var:
- @1canli:cravexv5-production.up.railway.app
- @2canli:cravexv5-production.up.railway.app
- @zohan:cravexv5-production.up.railway.app
- @stark:cravexv5-production.up.railway.app
- @u1:localhost
- @u2:localhost

Ama Synapse şimdi `matrix-synapse-production.up.railway.app` olarak çalışmaya çalışıyor, bu yüzden crash oluyor.

## ✅ Çözüm: Synapse'i `cravexv5-production.up.railway.app` Olarak Çalıştır

Kullanıcıları korumak için Synapse'i veritabanındaki domain ile eşleştirmemiz gerekiyor.

### Adım 1: Railway Environment Variable'ı Güncelle

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Variables** sekmesi:

`SYNAPSE_SERVER_NAME` değerini şu şekilde güncelleyin:
```
cravexv5-production.up.railway.app
```

### Adım 2: Synapse'i Yeniden Başlat

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **"Deploy"** veya servisi yeniden başlatın.

### Adım 3: Logları Kontrol Et

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **"Logs"** sekmesinde şunları kontrol edin:

✅ **Beklenen log mesajları:**
```
Server hostname: cravexv5-production.up.railway.app
Public Base URL: https://cravexv5-production.up.railway.app/
Setting up server
```

❌ **Crash hatası OLMAMALI:**
```
Exception: Found users in database not native to...
```

### Adım 4: Element Web Config'i Güncelle

Synapse `cravexv5-production.up.railway.app` olarak çalıştığı için, Element Web config'ini de güncellememiz gerekiyor.

`www/element-web/config.json` dosyasında:
```json
{
    "default_server_config": {
        "m.homeserver": {
            "base_url": "https://cravexv5-production.up.railway.app",
            "server_name": "cravexv5-production.up.railway.app"
        }
    },
    "room_directory": {
        "servers": ["cravexv5-production.up.railway.app"]
    }
}
```

### Adım 5: Netlify Redirect'leri Güncelle

`netlify.toml` dosyasında:
```toml
[[redirects]]
  from = "/_matrix/*"
  to = "https://cravexv5-production.up.railway.app/_matrix/:splat"
  status = 200
  force = true
  headers = {X-From = "Netlify"}

[[redirects]]
  from = "/.well-known/*"
  to = "https://cravexv5-production.up.railway.app/.well-known/:splat"
  status = 200
  force = true
  headers = {X-From = "Netlify"}
```

## 📝 Notlar

- Bu değişiklik kullanıcıları koruyacak
- Synapse `cravexv5-production.up.railway.app` olarak çalışacak
- Tüm mevcut kullanıcılar çalışmaya devam edecek
- V1.0.0 tag'inde `matrix-synapse-production.up.railway.app` vardı, ama kullanıcıları korumak için `cravexv5-production.up.railway.app` kullanacağız

## ⚠️ Önemli

- `localhost` domain'indeki kullanıcılar (@u1, @u2) sorun yaratabilir
- Eğer `localhost` domain'inde kullanıcılar varsa, bunları da `cravexv5-production.up.railway.app` domain'ine taşımanız gerekebilir
- Veya `localhost` domain'indeki kullanıcıları silmeniz gerekebilir (ama kullanıcı bunları korumak istiyor)

