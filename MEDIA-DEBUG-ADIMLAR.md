# Media Debug Adımları

## 🔍 Sorun
Loglarda Media API v3 denemesi görünmüyor. Sadece thumbnail proxy'leri var.

## ✅ Test Adımları

### 1. Resim İndirme Endpoint'ini Test Edin

1. **Admin panelde bir resim içeren mesajı açın**
2. **Resmin "İndir" butonuna tıklayın** (örnek: "İndir (27.2 KB)")
3. **Railway loglarını kontrol edin**

### 2. Loglarda Arayın

Şu log mesajlarını arayın:

```
[DEBUG] Trying Matrix Media API v3 (Element Web format): https://matrix-synapse.up.railway.app/_matrix/media/v3/download/...
[DEBUG] Media API v3 response: 200
[DEBUG] ✅ Matrix Media API v3 worked!
```

VEYA

```
[DEBUG] Trying Matrix Media API v3 (Element Web format): https://matrix-synapse.up.railway.app/_matrix/media/v3/download/...
[DEBUG] Media API v3 response: 404
[DEBUG] Media API v3 response text: {"errcode":"M_NOT_FOUND","error":"Not found"}
```

### 3. Eğer Log Yoksa

Eğer Media API v3 denemesi loglarda görünmüyorsa:

1. **Browser Console'u açın** (F12 → Console)
2. **Resmin "İndir" butonuna tıklayın**
3. **Console'da hata var mı kontrol edin**
4. **Network sekmesine gidin** (F12 → Network)
5. **"İndir" butonuna tekrar tıklayın**
6. **Network'te `/api/media/download/` ile başlayan request'i bulun**
7. **Request'in status code'unu kontrol edin** (200, 404, 500, vs.)

### 4. Test URL'i

Direkt test için browser'da şu URL'i açın:

```
https://considerate-adaptation-production.up.railway.app/api/media/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD
```

VEYA

```
https://considerate-adaptation-production.up.railway.app/api/media/download/matrix-synapse.up.railway.app/JpPmAvKDuaZnUmOQyVaWRCGk
```

Bu URL'leri açtığınızda:
- **Resim görünüyorsa**: ✅ Sorun çözüldü!
- **404 hatası alıyorsanız**: Railway loglarını kontrol edin
- **500 hatası alıyorsanız**: Railway loglarını kontrol edin

### 5. Logları Bana Gönderin

Eğer Media API v3 denemesi loglarda görünüyorsa, şu bilgileri bana gönderin:

1. **Media API v3 denemesi** ile ilgili tüm log satırları
2. **Response status code** (200, 404, 500, vs.)
3. **Response text** (varsa)
4. **Hata mesajları** (varsa)

---

## 📝 Notlar

- **Thumbnail proxy'leri çalışıyor** ✅ (loglarda görünüyor)
- **Resim indirme endpoint'i test edilmeli** ⚠️
- **Media API v3 denemesi loglarda görünmüyor** ⚠️

---

## 🎯 Beklenen Sonuç

Resim indirme endpoint'ini test ettiğinizde, Railway loglarında şu mesajları görmelisiniz:

```
[INFO] ⏳ Media not in cache, fetching from Matrix: HQtoyORnVrJmhoFLGhWQZZQD
[DEBUG] Trying Matrix Media API v3 (Element Web format): https://matrix-synapse.up.railway.app/_matrix/media/v3/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD?allow_redirect=true
[DEBUG] Media API v3 response: 200
[DEBUG] ✅ Matrix Media API v3 worked!
```

VEYA (eğer başarısız olursa):

```
[INFO] ⏳ Media not in cache, fetching from Matrix: HQtoyORnVrJmhoFLGhWQZZQD
[DEBUG] Trying Matrix Media API v3 (Element Web format): https://matrix-synapse.up.railway.app/_matrix/media/v3/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD?allow_redirect=true
[DEBUG] Media API v3 response: 404
[DEBUG] Media API v3 response text: {"errcode":"M_NOT_FOUND","error":"Not found"}
[DEBUG] Trying Matrix Client API v3: https://matrix-synapse.up.railway.app/_matrix/client/v3/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD
...
```

