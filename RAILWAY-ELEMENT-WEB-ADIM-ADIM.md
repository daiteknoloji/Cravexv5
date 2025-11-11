# 🔧 Element Web Railway Build - Adım Adım Çözüm

**Tarih:** 2025-01-11  
**Hata:** `stat /www/element-web/Dockerfile: not a directory`

---

## ⚠️ SORUN

Railway Dockerfile yolunu bulamıyor veya yanlış yorumluyor. Bu, root directory ve Dockerfile path ayarlarının uyumsuzluğundan kaynaklanıyor.

---

## ✅ ÇÖZÜM - ADIM ADIM

### Adım 1: Railway Dashboard'a Gidin

1. https://railway.app/dashboard
2. `cravexv5` projesini seçin
3. `surprising-emotion` servisini seçin

---

### Adım 2: Root Directory'yi Ayarlayın

1. **Settings** → **General** sekmesine gidin
2. **Root Directory** alanını bulun
3. Değeri şu şekilde ayarlayın:
   ```
   www/element-web
   ```
4. **Save** butonuna tıklayın

**ÖNEMLİ:** Root directory mutlaka `www/element-web` olmalı!

---

### Adım 3: Build Ayarlarını Kontrol Edin

1. **Settings** → **Build** sekmesine gidin
2. **Config File** alanını kontrol edin:
   - `railway-element-web.json` seçili olmalı
   - Eğer seçili değilse, seçin
3. **Dockerfile Path** alanını kontrol edin:
   - Değer: `Dockerfile` olmalı (sadece `Dockerfile`, başka bir şey değil!)
   - Eğer farklı bir değer varsa, `Dockerfile` olarak değiştirin
4. **Builder** alanını kontrol edin:
   - `DOCKERFILE` seçili olmalı
5. **Save** butonuna tıklayın

---

### Adım 4: Config Dosyasını Doğrulayın

Railway config dosyası (`railway-element-web.json`) şu şekilde olmalı:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**ÖNEMLİ:** `dockerfilePath` değeri sadece `Dockerfile` olmalı, `www/element-web/Dockerfile` değil!

---

### Adım 5: Redeploy Yapın

1. **Deploy** sekmesine gidin
2. **Redeploy** butonuna tıklayın
3. Build loglarını izleyin

---

## ✅ BEKLENEN SONUÇ

Build loglarında şunu görmelisiniz:

```
[internal] load build definition from Dockerfile
```

**Hata mesajı görünmemeli:**
- ❌ `failed to read dockerfile`
- ❌ `not a directory`
- ❌ `no such file or directory`

---

## 🔍 SORUN GİDERME

### Hata Devam Ederse:

1. **Root Directory Kontrolü:**
   - Settings → General → Root Directory
   - Değer: `www/element-web` olmalı
   - Eğer boşsa veya farklıysa, `www/element-web` olarak ayarlayın

2. **Dockerfile Path Kontrolü:**
   - Settings → Build → Dockerfile Path
   - Değer: `Dockerfile` olmalı (sadece `Dockerfile`)
   - Eğer `www/element-web/Dockerfile` ise, `Dockerfile` olarak değiştirin

3. **Config Dosyası Kontrolü:**
   - Repository'de `railway-element-web.json` dosyasının doğru olduğundan emin olun
   - `dockerfilePath` değeri `Dockerfile` olmalı

4. **Railway Cache Temizliği:**
   - Bazen Railway cache'i sorun yaratabilir
   - Settings → Build → Clear Build Cache (varsa)
   - Veya servisi silip yeniden oluşturun

---

## 📋 KONTROL LİSTESİ

- [ ] Root Directory: `www/element-web` ✅
- [ ] Dockerfile Path: `Dockerfile` ✅
- [ ] Builder: `DOCKERFILE` ✅
- [ ] Config File: `railway-element-web.json` ✅
- [ ] Config dosyasında `dockerfilePath: "Dockerfile"` ✅
- [ ] Redeploy yapıldı ✅

---

## 🎯 ALTERNATİF ÇÖZÜM

Eğer yukarıdaki adımlar işe yaramazsa, Railway'de root directory'yi boş bırakıp Dockerfile path'i `www/element-web/Dockerfile` olarak ayarlayın:

1. **Root Directory:** (boş/proje root)
2. **Dockerfile Path:** `www/element-web/Dockerfile`

Bu durumda config dosyasını da güncellemeniz gerekir:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "www/element-web/Dockerfile"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

**Son Güncelleme:** 2025-01-11  
**Hazırlayan:** AI Assistant

