# 🚨 ACİL: Railway Synapse Restart

## Sorun
CORS hatası: `No 'Access-Control-Allow-Origin' header is present`

## Çözüm: Railway'de Synapse Restart

### Adımlar:

1. **Railway Dashboard'a gidin:**
   - https://railway.app/dashboard
   - `cravexv5` projesini seçin
   - Synapse servisini bulun

2. **Redeploy yapın:**
   - Synapse servisi → **Deployments** sekmesi
   - **Redeploy** butonuna tıklayın
   - Veya **Settings** → **Redeploy**

3. **Logları kontrol edin:**
   - Synapse servisi → **Logs** sekmesi
   - `Starting synapse` mesajını bekleyin
   - `Listening on` mesajını görünce hazır!

4. **Test edin:**
   - https://cozy-dragon-54547b.netlify.app/#/login
   - Browser console'da CORS hatası kalmamalı

---

## Alternatif: Railway CLI ile Restart

```bash
railway restart
```

---

**Bu işlem 2-5 dakika sürebilir.**


