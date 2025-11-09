# ✅ Railway'de Domain Ayarlama - Adım Adım

## Durum
- Veritabanında `cravex1-production.up.railway.app` domain'inde **18 kullanıcı** var
- Synapse `matrix-synapse-production.up.railway.app` ile başlamaya çalışıyor → **CRASH!**

## Çözüm: Railway'de Domain'i Ayarla

### Adım 1: Railway Dashboard'a Git
1. Tarayıcıda https://railway.app aç
2. Giriş yap
3. **Cravexv5** projesini seç

### Adım 2: Synapse Servisini Bul
1. Sol tarafta servisler listesinde **Synapse** servisini bul
2. Tıkla

### Adım 3: Variables Sekmesine Git
1. Üst menüden **Variables** sekmesine tıkla
2. Environment variables listesi görünecek

### Adım 4: SYNAPSE_SERVER_NAME'i Güncelle
1. `SYNAPSE_SERVER_NAME` variable'ını bul
2. Eğer yoksa → **+ New Variable** butonuna tıkla
3. **Name:** `SYNAPSE_SERVER_NAME`
4. **Value:** `cravex1-production.up.railway.app`
5. **Save** butonuna tıkla

### Adım 5: Bekle
- Railway otomatik olarak servisi redeploy edecek
- 1-2 dakika bekle
- Synapse başlayacak! ✅

---

## ✅ Kontrol

Synapse başladı mı kontrol et:

1. Railway dashboard → Synapse servisi → **Logs** sekmesi
2. Şunu görmelisin:
   ```
   📍 Server: cravex1-production.up.railway.app
   Server hostname: cravex1-production.up.railway.app
   ```
3. Hata yoksa → **BAŞARILI!** ✅

---

## 🎯 Özet

**Yapılacak tek şey:**
Railway dashboard → Synapse → Variables → `SYNAPSE_SERVER_NAME=cravex1-production.up.railway.app` → Save

**Bu kadar!** Synapse otomatik başlayacak ve 18 kullanıcı ile çalışacak! 🚀


