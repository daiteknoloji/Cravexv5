# 🚨 ACİL: CORS + 404 Hatası Çözümü

## ❌ Mevcut Sorunlar

1. **CORS Hatası:**
   ```
   Access to fetch at 'https://cravexv5-production.up.railway.app/_matrix/client/versions' 
   from origin 'https://cozy-dragon-54547b.netlify.app' has been blocked by CORS policy
   ```

2. **404 Not Found:**
   ```
   GET https://cravexv5-production.up.railway.app/_matrix/client/versions net::ERR_FAILED 404 (Not Found)
   ```

3. **Widget Hataları:** (İkincil sorun - CORS çözülünce düzelecek)

---

## 🔍 Sorunun Analizi

**404 hatası** şu anlama geliyor:
- Railway'deki Synapse çalışmıyor VEYA
- URL yanlış VEYA
- Railway'de port expose edilmemiş

---

## ✅ ÇÖZÜM ADIMLARI

### 1. Railway'de Synapse Durumunu Kontrol Et

Railway Dashboard → Synapse servisi → **Logs**:
- ✅ Synapse başladı mı? (`Starting synapse` mesajı var mı?)
- ✅ Port 8008'de dinliyor mu? (`Listening on` mesajı var mı?)
- ❌ Hata var mı? (PermissionError, DatabaseError, vb.)

### 2. Railway Public URL Kontrol Et

Railway Dashboard → Synapse servisi → **Settings**:
- ✅ **Public URL:** `https://cravexv5-production.up.railway.app` doğru mu?
- ✅ **Port:** `8008` expose edilmiş mi?

### 3. Railway Health Check

Browser'da direkt test edin:
```
https://cravexv5-production.up.railway.app/_matrix/client/versions
```

**Beklenen sonuç:**
- ✅ JSON response gelmeli: `{"versions": ["v1.1", "v1.2", ...]}`
- ❌ 404 veya CORS hatası = Sorun var

### 4. Railway'de Synapse Restart

Railway Dashboard → Synapse servisi → **Deployments** → **Redeploy**

---

## 🎯 HIZLI TEST

### Browser Console'da Test:

```javascript
// 1. Railway'e direkt test (CORS hatası beklenir ama 404 olmamalı)
fetch('https://cravexv5-production.up.railway.app/_matrix/client/versions')
  .then(r => r.json())
  .then(data => console.log('✅ Railway çalışıyor:', data))
  .catch(err => console.error('❌ Railway hatası:', err));

// 2. Netlify proxy üzerinden test (CORS hatası olmamalı)
fetch('/_matrix/client/versions')
  .then(r => r.json())
  .then(data => console.log('✅ Netlify proxy çalışıyor:', data))
  .catch(err => console.error('❌ Netlify proxy hatası:', err));
```

---

## 💡 ÇÖZÜMLER

### Çözüm 1: Railway Synapse Restart (ÖNERİLEN)

1. Railway Dashboard → Synapse → **Redeploy**
2. Logları kontrol et
3. 2-5 dakika bekle
4. Test et

### Çözüm 2: Railway Port Kontrolü

Railway Dashboard → Synapse → **Settings**:
- Port `8008` expose edilmiş mi kontrol et
- Public URL doğru mu kontrol et

### Çözüm 3: Netlify Proxy Kullan

Netlify redirect'leri zaten var ama çalışmıyor olabilir. 
Config.json'da homeserver URL'ini Netlify domain'i olarak ayarla (ama bu çalışmayabilir).

---

## 📋 CHECKLIST

- [ ] Railway Dashboard'da Synapse loglarını kontrol ettim
- [ ] Synapse başarıyla başladı mı kontrol ettim
- [ ] Railway public URL doğru mu kontrol ettim
- [ ] Railway port expose edilmiş mi kontrol ettim
- [ ] Browser'da direkt Railway URL'ini test ettim
- [ ] Railway'de Synapse restart yaptım

---

## 🆘 HALA ÇALIŞMIYORSA

1. **Railway Dashboard → Synapse → Logs** → Tüm logları kontrol et
2. **Railway Dashboard → Synapse → Settings** → Port ve URL ayarlarını kontrol et
3. **Railway Dashboard → Synapse → Deployments** → Yeni bir deploy tetikle

---

**ÖNEMLİ:** 404 hatası Synapse'in çalışmadığı anlamına geliyor. Önce Railway'de Synapse'in çalıştığından emin olun!


