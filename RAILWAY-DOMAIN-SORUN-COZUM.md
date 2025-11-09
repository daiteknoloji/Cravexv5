# 🚨 RAILWAY DOMAIN SORUNU - ACİL ÇÖZÜM

## ✅ İyi Haber
Synapse başarıyla çalışıyor:
- ✅ Port 8008'de dinliyor
- ✅ Database bağlantısı çalışıyor
- ✅ Tüm servisler başladı

## ❌ Sorun
Railway'in public URL'i çalışmıyor:
```
https://cravexv5-production.up.railway.app/_matrix/client/versions --> Not Found
The train has not arrived at the station.
Please check your network settings to confirm that your domain has provisioned.
```

Bu, Railway'in reverse proxy'sinin çalışmadığı veya domain'in expose edilmediği anlamına geliyor.

---

## ✅ ÇÖZÜM ADIMLARI

### 1. Railway'de Port Expose Kontrolü

Railway Dashboard → Synapse servisi → **Settings**:

1. **Port** sekmesine gidin
2. **Expose Port** kontrol edin:
   - ✅ Port `8008` expose edilmiş mi?
   - ✅ **Generate Domain** butonuna tıklayın (eğer expose edilmemişse)

### 2. Railway Public URL Kontrolü

Railway Dashboard → Synapse servisi → **Settings** → **Networking**:

1. **Public Networking** açık mı kontrol edin
2. **Generate Domain** butonuna tıklayın
3. Public URL'in `cravexv5-production.up.railway.app` olduğundan emin olun

### 3. Railway Service Settings

Railway Dashboard → Synapse servisi → **Settings**:

**Health Check Path:** `/health`
**Health Check Interval:** 30s

### 4. Railway Variables Kontrolü

Railway Dashboard → Synapse servisi → **Variables**:

Şu variable'ların olduğundan emin olun:
- `PORT`: `8008` (Railway otomatik set eder)
- `SYNAPSE_SERVER_NAME`: `cravexv5-production.up.railway.app`
- `SYNAPSE_NO_TLS`: `true` (Railway HTTPS handle ediyor)

---

## 🎯 HIZLI ÇÖZÜM

### Adım 1: Railway'de Port Expose Et

1. Railway Dashboard → Synapse servisi
2. **Settings** → **Networking**
3. **Generate Domain** butonuna tıklayın
4. Port `8008`'in expose edildiğinden emin olun

### Adım 2: Railway Restart

1. Railway Dashboard → Synapse servisi
2. **Deployments** → **Redeploy**
3. 2-5 dakika bekle

### Adım 3: Test Et

Browser'da test edin:
```
https://cravexv5-production.up.railway.app/_matrix/client/versions
```

**Beklenen sonuç:**
- ✅ JSON response: `{"versions": ["v1.1", "v1.2", ...]}`
- ❌ Hala "Not Found" = Railway domain sorunu devam ediyor

---

## 💡 ALTERNATİF ÇÖZÜM: Netlify Proxy Kullan

Eğer Railway domain'i çalışmıyorsa, Netlify proxy'yi kullanabiliriz:

1. Netlify redirect'leri zaten var (`netlify.toml`)
2. Config.json'da homeserver URL'ini Netlify domain'i olarak ayarla
3. Bu sayede CORS sorunu da çözülür

---

## 📋 CHECKLIST

- [ ] Railway Dashboard'da Synapse servisini açtım
- [ ] Settings → Networking → Generate Domain yaptım
- [ ] Port 8008 expose edilmiş mi kontrol ettim
- [ ] Railway'de Synapse restart yaptım
- [ ] Browser'da Railway URL'ini test ettim
- [ ] Hala çalışmıyorsa Netlify proxy'yi kullanmayı denedim

---

## 🆘 HALA ÇALIŞMIYORSA

1. **Railway Dashboard → Synapse → Settings → Networking**
   - Public Networking açık mı?
   - Domain generate edilmiş mi?

2. **Railway Dashboard → Synapse → Settings → Port**
   - Port 8008 expose edilmiş mi?

3. **Railway Support'a başvurun:**
   - Domain provisioning sorunu olabilir
   - Railway'in infrastructure sorunu olabilir

---

**ÖNEMLİ:** Synapse çalışıyor ama Railway'in public URL'i çalışmıyor. Railway Dashboard'da domain ayarlarını kontrol edin!


