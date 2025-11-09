# Railway Synapse Server Name Güncelleme

## 🔍 Sorun

Veritabanında `cravexv5-production.up.railway.app` domain'inde kullanıcılar var:
- `@1canli:cravexv5-production.up.railway.app`
- `@2canli:cravexv5-production.up.railway.app`
- `@zohan:cravexv5-production.up.railway.app`
- `@stark:cravexv5-production.up.railway.app`
- `@u1:localhost`
- `@u2:localhost`

Ama Railway'deki `SYNAPSE_SERVER_NAME` environment variable'ı `matrix-synapse-production.up.railway.app` olarak ayarlı, bu yüzden Synapse crash oluyor.

## ✅ Çözüm: Railway Environment Variable'ını Güncelle

### Adımlar:

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi → **"Variables"** sekmesi

2. `SYNAPSE_SERVER_NAME` environment variable'ını bulun

3. Değeri şu şekilde güncelleyin:
   ```
   cravexv5-production.up.railway.app
   ```

4. **"Save"** butonuna tıklayın

5. Synapse servisi otomatik olarak yeniden başlayacak

### Doğru Environment Variables:

```bash
POSTGRES_DB="${{Postgres.PGDATABASE}}"
POSTGRES_HOST="${{Postgres.PGHOST}}"
POSTGRES_PASSWORD="${{Postgres.PGPASSWORD}}"
POSTGRES_PORT="${{Postgres.PGPORT}}"
POSTGRES_USER="${{Postgres.PGUSER}}"

# ÖNEMLİ: Bu değer veritabanındaki kullanıcıların domain'i ile eşleşmeli
SYNAPSE_SERVER_NAME="cravexv5-production.up.railway.app"

WEB_CLIENT_LOCATION="https://cozy-dragon-54547b.netlify.app"
```

## 🔍 Kontrol

Synapse başladıktan sonra logları kontrol edin:

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **"Logs"** sekmesi

**Beklenen log mesajları:**
```
Server hostname: cravexv5-production.up.railway.app
Public Base URL: https://cravexv5-production.up.railway.app/
Setting up server
```

**Crash hatası OLMAMALI!**

## 📝 Notlar

- Dosyalar zaten `cravexv5-production.up.railway.app` olarak ayarlı
- Sadece Railway environment variable'ını güncellemeniz yeterli
- Kullanıcılar korunacak, silinmeyecek
- Synapse başarıyla çalışacak


