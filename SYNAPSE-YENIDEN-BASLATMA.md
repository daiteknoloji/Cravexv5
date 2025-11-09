# Synapse Servisini Yeniden Başlatma

## ✅ Veritabanı Temizlendi

Veritabanı başarıyla temizlendi. Şimdi Synapse servisini yeniden başlatmanız gerekiyor.

## 🚀 Adımlar

### Yöntem 1: Railway Dashboard (Önerilen)

1. **Railway Dashboard**'a gidin
2. **Cravexv5** (Synapse) servisinizi seçin
3. **"Deployments"** sekmesine gidin
4. **"Redeploy"** butonuna tıklayın
   - Veya **"Settings"** → **"Restart"** butonuna tıklayın

### Yöntem 2: Railway CLI

```bash
railway restart --service cravexv5
```

veya

```bash
railway redeploy --service cravexv5
```

## 📋 Beklenen Sonuç

Synapse başladığında loglarda şunları görmelisiniz:

```
✅ Server hostname: cravex1-production.up.railway.app
✅ Public Base URL: https://cravex1-production.up.railway.app/
✅ Starting server...
✅ Server started successfully
```

**Artık hata olmamalı!**

## 🔍 Logları Kontrol Et

Synapse başladıktan sonra logları kontrol edin:

```bash
railway logs --service cravexv5
```

Veya Railway Dashboard → Cravexv5 → "Logs" sekmesinden kontrol edin.

## ⚠️ Önemli Notlar

- Synapse başladığında **otomatik olarak şemayı yeniden oluşturacak**
- `server_name: cravex1-production.up.railway.app` ile kaydedecek
- Artık **tüm kullanıcılar ve odalar silindi** - yeniden oluşturulabilir
- İlk başlangıçta şema oluşturma biraz zaman alabilir (1-2 dakika)

## 🎯 Sonraki Adımlar

1. ✅ Synapse servisini yeniden başlatın
2. ✅ Logları kontrol edin - hata olmamalı
3. ✅ Yeni kullanıcılar kayıt olabilir
4. ✅ Odalar yeniden oluşturulabilir


