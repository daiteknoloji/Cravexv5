# Railway Synapse Server Name Güncelleme - SON ÇÖZÜM

## Sorun
Synapse servisi `cravex1-production.up.railway.app` ile başlamaya çalışıyor, ancak veritabanında `cravexv5-production.up.railway.app` ve `localhost` domain'lerinde kullanıcılar var. Bu uyumsuzluk Synapse'in crash olmasına neden oluyor.

## Çözüm
Railway'deki `SYNAPSE_SERVER_NAME` environment variable'ını `cravexv5-production.up.railway.app` olarak güncelleyin.

## Adımlar

### 1. Railway Dashboard'a Giriş Yapın
- https://railway.app adresine gidin
- Giriş yapın

### 2. Cravexv5 Synapse Servisini Bulun
- Projenizdeki **Cravexv5** servisini bulun
- Servise tıklayın

### 3. Variables Sekmesine Gidin
- Sol menüden **Variables** sekmesine tıklayın

### 4. SYNAPSE_SERVER_NAME'i Güncelleyin
- `SYNAPSE_SERVER_NAME` variable'ını bulun
- Değerini şu şekilde güncelleyin:
  ```
  cravexv5-production.up.railway.app
  ```
- Eğer variable yoksa, **New Variable** butonuna tıklayın ve ekleyin:
  - **Name**: `SYNAPSE_SERVER_NAME`
  - **Value**: `cravexv5-production.up.railway.app`

### 5. Servisi Yeniden Başlatın
- Variables'ı kaydettikten sonra, Railway otomatik olarak servisi yeniden deploy edecektir
- Veya manuel olarak **Deployments** sekmesinden **Redeploy** butonuna tıklayabilirsiniz

### 6. Logları Kontrol Edin
- **Deployments** sekmesinden en son deployment'ı seçin
- **View Logs** butonuna tıklayın
- Loglarda şu satırları görmelisiniz:
  ```
  Server hostname: cravexv5-production.up.railway.app
  Public Base URL: https://cravexv5-production.up.railway.app/
  ```
- Eğer hata yoksa, Synapse başarıyla başlamış demektir!

## Doğrulama
Synapse başarıyla başladıktan sonra:
1. Element Web'de giriş yapmayı deneyin
2. Admin panel'den kullanıcıları kontrol edin
3. Her şey çalışıyorsa, sorun çözülmüştür!

## Notlar
- `start.sh` script'i artık herhangi bir `server_name` değerini dinamik olarak replace edebilir
- Bu sayede gelecekte `server_name` değişiklikleri daha kolay yapılabilir
- Veritabanındaki mevcut kullanıcılar (`cravexv5-production.up.railway.app` ve `localhost` domain'lerinde) korunacaktır


