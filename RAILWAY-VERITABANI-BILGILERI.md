# Railway Veritabanı Bilgileri

## 🔍 Hangi Veritabanını Kullanıyoruz?

Railway'deki **Cravexv5** projesinde Synapse servisi, Railway'in otomatik olarak bağladığı **PostgreSQL** servisini kullanıyor.

## 📊 Veritabanı Bağlantı Bilgileri

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Variables** sekmesinde şu environment variable'lar var:

```bash
POSTGRES_DB="${{Postgres.PGDATABASE}}"
POSTGRES_HOST="${{Postgres.PGHOST}}"
POSTGRES_PASSWORD="${{Postgres.PGPASSWORD}}"
POSTGRES_PORT="${{Postgres.PGPORT}}"
POSTGRES_USER="${{Postgres.PGUSER}}"
```

Bu değerler Railway'in **template syntax**'ı ile otomatik olarak ayarlanıyor. Yani:

- **PostgreSQL Servisi:** Railway'deki **Postgres** servisi (Cravexv5 projesine bağlı)
- **Veritabanı Adı:** `${{Postgres.PGDATABASE}}` değeri (genellikle `railway` veya `postgres`)
- **Host:** `${{Postgres.PGHOST}}` (genellikle `postgres.railway.internal` veya Railway'in internal host'u)
- **Port:** `${{Postgres.PGPORT}}` (genellikle `5432`)
- **Kullanıcı:** `${{Postgres.PGUSER}}` (genellikle `postgres`)

## 🔎 Gerçek Değerleri Kontrol Etme

### Yöntem 1: Railway Dashboard'dan

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi → **Variables** sekmesi
2. `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER` değerlerini kontrol edin
3. Bu değerler gerçek PostgreSQL bağlantı bilgilerini gösterir

### Yöntem 2: Railway Dashboard → Postgres Servisi

1. **Railway Dashboard** → **Cravexv5** → **Postgres** servisi
2. **"Settings"** sekmesinde veritabanı bilgilerini görebilirsiniz
3. **"Query"** sekmesinden SQL sorguları çalıştırabilirsiniz

### Yöntem 3: Synapse Loglarından

Synapse başladığında loglarda şunu göreceksiniz:
```
🗄️  Database: postgres.railway.internal:5432
```

Bu, Synapse'in hangi PostgreSQL host'una bağlandığını gösterir.

## 📝 Önemli Notlar

1. **Veritabanı Adı:** Railway'de genellikle `railway` veya `postgres` olur
2. **Host:** Railway'in internal network'ünde `postgres.railway.internal` olarak görünür
3. **Port:** Genellikle `5432` (PostgreSQL default port)
4. **Kullanıcı:** Genellikle `postgres` (superuser)

## 🛠️ Veritabanına Bağlanma

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesinden SQL sorguları çalıştırabilirsiniz.

Veya Railway CLI kullanarak:
```bash
railway connect postgres
```

## ⚠️ DİKKAT

- Railway'deki PostgreSQL servisi **paylaşımlı** bir servis olabilir
- Veritabanı adı genellikle `railway` veya `postgres` olur
- Tüm Synapse tabloları `public` schema'sında oluşturulur
- Veritabanını temizlemek için `DROP SCHEMA public CASCADE` kullanın


