# Railway Cravexv5 Synapse Servisi - Doğru Environment Variables

## ✅ Doğru Environment Variables

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Variables** sekmesinde şu değerler olmalı:

```bash
# PostgreSQL Connection (Railway Template Syntax - DOĞRU)
POSTGRES_DB="${{Postgres.PGDATABASE}}"
POSTGRES_HOST="${{Postgres.PGHOST}}"
POSTGRES_PASSWORD="${{Postgres.PGPASSWORD}}"
POSTGRES_PORT="${{Postgres.PGPORT}}"
POSTGRES_USER="${{Postgres.PGUSER}}"

# Synapse Server Name (DOĞRU ✅)
SYNAPSE_SERVER_NAME="matrix-synapse-production.up.railway.app"

# Web Client Location (DÜZELTİLMELİ ❌)
WEB_CLIENT_LOCATION="https://cozy-dragon-54547b.netlify.app"
```

## ❌ Mevcut Hatalı Değer

```bash
WEB_CLIENT_LOCATION="ttps://surprising-emotion-production.up.railway.app"
```

**Sorunlar:**
1. `ttps://` yerine `https://` olmalı (h eksik)
2. Railway URL'i yerine Netlify URL'i olmalı
3. `surprising-emotion-production.up.railway.app` yerine `cozy-dragon-54547b.netlify.app` olmalı

## 🔧 Düzeltme Adımları

### 1. Railway Dashboard'dan Düzeltin

1. **Railway Dashboard** → **Cravexv5** projesine gidin
2. **Synapse** servisini seçin
3. **"Variables"** sekmesine gidin
4. `WEB_CLIENT_LOCATION` environment variable'ını bulun
5. **"Edit"** butonuna tıklayın
6. Değeri şu şekilde güncelleyin:
   ```
   https://cozy-dragon-54547b.netlify.app
   ```
7. **"Save"** butonuna tıklayın

### 2. Alternatif Netlify URL (Eğer farklı bir URL kullanıyorsanız)

Eğer `vcravex1.netlify.app` kullanıyorsanız:
```
https://vcravex1.netlify.app
```

### 3. Synapse Servisini Yeniden Başlatın

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Deployments"** sekmesine gidin
3. **"Redeploy"** butonuna tıklayın
4. Deploy'in tamamlanmasını bekleyin

## ✅ Kontrol

Deploy tamamlandıktan sonra:
1. Synapse loglarını kontrol edin:
   - **Railway Dashboard** → **Cravexv5** → **Synapse** → **"Logs"**
   - `web_client_location: https://cozy-dragon-54547b.netlify.app` görünmeli
2. `https://matrix-synapse-production.up.railway.app/_matrix/client/versions` adresini açın
   - 200 OK yanıtı almalısınız

## 📝 Özet

- ✅ `SYNAPSE_SERVER_NAME` → DOĞRU (`matrix-synapse-production.up.railway.app`)
- ✅ PostgreSQL variables → DOĞRU (Railway template syntax)
- ❌ `WEB_CLIENT_LOCATION` → DÜZELTİLMELİ (`https://cozy-dragon-54547b.netlify.app`)


