# 🚨 CORS SORUNU - ACİL ÇÖZÜM

## ❌ Mevcut Sorun

```
Access to fetch at 'https://cravexv5-production.up.railway.app/_matrix/client/versions' 
from origin 'https://cozy-dragon-54547b.netlify.app' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present.
```

## 🔍 Sorunun Nedeni

Railway'deki Synapse CORS header'larını göndermiyor. İki çözüm var:

### Çözüm 1: Netlify Proxy Kullan (ÖNERİLEN) ✅

Netlify redirect'leri zaten var ama çalışmıyor. Bunun nedeni:
- Redirect'ler `status = 200` ile proxy yapıyor
- Ama CORS headers eksik olabilir

### Çözüm 2: Railway'de Synapse'i Güncelle

Railway'deki Synapse'in homeserver.yaml dosyası güncellenmeli ve restart edilmeli.

---

## ✅ HIZLI ÇÖZÜM ADIMLARI

### 1. Railway'de Synapse Restart Et

Railway Dashboard → Synapse servisi → **Deployments** → **Redeploy**

### 2. Railway CORS Ayarlarını Kontrol Et

Railway Dashboard → Synapse servisi → **Variables**:

Şu variable'ların olduğundan emin olun:
- `SYNAPSE_SERVER_NAME`: `cravexv5-production.up.railway.app`
- `SYNAPSE_NO_TLS`: `true`

### 3. Homeserver.yaml'ı Railway'e Push Et

`synapse-railway-config/homeserver.yaml` dosyasında CORS ayarları var:
```yaml
cors_allowed_origins:
  - "https://cozy-dragon-54547b.netlify.app"
```

Bu dosya Railway'de güncellenmiş olmalı.

### 4. Netlify Redirect'lerini Test Et

Browser console'da test edin:
```javascript
// Netlify proxy üzerinden test
fetch('/_matrix/client/versions')
  .then(r => r.json())
  .then(data => console.log('✅ Netlify proxy çalışıyor:', data))
  .catch(err => console.error('❌ Netlify proxy hatası:', err));
```

---

## 🎯 EN HIZLI ÇÖZÜM

Railway Dashboard'a gidin ve Synapse servisini **Redeploy** edin. Bu CORS ayarlarını yeniden yükleyecek.

---

## 📋 KONTROL LİSTESİ

- [ ] Railway Dashboard → Synapse → Redeploy yaptım
- [ ] Railway'de CORS ayarları doğru mu kontrol ettim
- [ ] Browser console'da Netlify proxy test ettim
- [ ] Login sayfası açılıyor mu kontrol ettim

---

**Son Güncelleme:** Şimdi


