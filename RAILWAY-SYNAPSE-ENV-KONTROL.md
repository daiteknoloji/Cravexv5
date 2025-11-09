# Railway Synapse Environment Variable Kontrolü

## 🔍 Sorun

Synapse (`cravex1-production.up.railway.app`) crash oluyor ve 500 hatası veriyor. Bu, Synapse'in `server_name`'inin yanlış ayarlanmış olmasından kaynaklanıyor olabilir.

## ✅ Çözüm

### 1. Railway Dashboard'dan Environment Variable'ları Kontrol Edin

1. **Railway Dashboard** → **Cravexv5** projesine gidin
2. **Synapse** servisini seçin
3. **"Variables"** sekmesine gidin
4. `SYNAPSE_SERVER_NAME` environment variable'ını kontrol edin

### 2. `SYNAPSE_SERVER_NAME` Değerini Güncelleyin

`SYNAPSE_SERVER_NAME` değeri şu olmalı:
```
matrix-synapse-production.up.railway.app
```

Eğer `cravex1-production.up.railway.app` ise, şu şekilde güncelleyin:
1. **"Variables"** sekmesinde `SYNAPSE_SERVER_NAME` değerini bulun
2. **"Edit"** butonuna tıklayın
3. Değeri `matrix-synapse-production.up.railway.app` olarak güncelleyin
4. **"Save"** butonuna tıklayın

### 3. Synapse Servisini Yeniden Başlatın

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Deployments"** sekmesine gidin
3. **"Redeploy"** butonuna tıklayın
4. Deploy'in tamamlanmasını bekleyin

### 4. Synapse Loglarını Kontrol Edin

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Logs"** sekmesine gidin
3. Synapse'in başarıyla başladığını ve `server_name: matrix-synapse-production.up.railway.app` olduğunu doğrulayın

## ⚠️ Önemli Not

V1.0.0'da Synapse'in `server_name`'i `matrix-synapse-production.up.railway.app` olmalı. Eğer Railway'deki environment variable `cravex1-production.up.railway.app` ise, Synapse crash olacaktır.

## 🔍 Kontrol

Deploy tamamlandıktan sonra:
1. `https://matrix-synapse-production.up.railway.app/_matrix/client/versions` adresini açın
2. 200 OK yanıtı almalısınız
3. Eğer hala 500 hatası alıyorsanız, Synapse loglarını kontrol edin


