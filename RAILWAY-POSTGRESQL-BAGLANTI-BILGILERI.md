# Railway PostgreSQL Bağlantı Bilgileri

## 📋 Cravexv5 Projesi - PostgreSQL Bağlantı Bilgileri

### Environment Variables (Railway Template Syntax)

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Variables** sekmesinde:

```bash
POSTGRES_DB="${{Postgres.PGDATABASE}}"
POSTGRES_HOST="${{Postgres.PGHOST}}"
POSTGRES_PASSWORD="${{Postgres.PGPASSWORD}}"
POSTGRES_PORT="${{Postgres.PGPORT}}"
POSTGRES_USER="${{Postgres.PGUSER}}"
```

**Not:** Bu değerler Railway'in template syntax'ı ile otomatik olarak ayarlanıyor.

## 🔍 Gerçek Değerleri Bulma

### Yöntem 1: Railway Dashboard'dan (EN KOLAY)

1. **Railway Dashboard** → **Cravexv5** projesine gidin
2. **Postgres** servisini seçin
3. **"Variables"** sekmesine gidin
4. Şu bilgileri göreceksiniz:
   - `PGHOST` → Host adresi
   - `PGPORT` → Port (genellikle 5432)
   - `PGDATABASE` → Veritabanı adı (genellikle `railway` veya `postgres`)
   - `PGUSER` → Kullanıcı adı (genellikle `postgres`)
   - `PGPASSWORD` → Şifre

### Yöntem 2: Railway CLI ile

```bash
railway connect postgres
```

Bu komut size bağlantı bilgilerini ve connection string'i gösterecek.

### Yöntem 3: Synapse Loglarından

Synapse başladığında loglarda şunu göreceksiniz:
```
🗄️  Database: postgres.railway.internal:5432
```

## 📝 DBeaver Bağlantı Ayarları

### Örnek Bağlantı Bilgileri

```
Host: postgres.railway.internal
Port: 5432
Database: railway (veya postgres)
Username: postgres
Password: [Railway'den alınan şifre]
```

### Connection String Formatı

```
postgresql://postgres:password@postgres.railway.internal:5432/railway
```

## 🔐 Railway PostgreSQL Bağlantı Bilgileri (Tahmini)

Railway'in genel yapısına göre:

```
Host: postgres.railway.internal (internal network)
      VEYA Railway'in verdiği external host (eğer varsa)
Port: 5432
Database: railway (veya postgres)
Username: postgres
Password: [Railway'deki PGPASSWORD değeri]
```

## ⚠️ ÖNEMLİ NOTLAR

1. **Internal Network:** Railway servisleri arasında `postgres.railway.internal` kullanılır
2. **External Access:** Dışarıdan bağlanmak için Railway'in external host'unu kullanmanız gerekir
3. **Password:** Railway'deki `PGPASSWORD` environment variable'ından şifreyi alın
4. **SSL:** Railway PostgreSQL SSL gerektirebilir, DBeaver'da SSL ayarlarını kontrol edin

## 🚀 Hızlı Bağlantı

### Railway Dashboard Query Sekmesi (EN KOLAY)

1. **Railway Dashboard** → **Cravexv5** → **Postgres** servisi
2. **"Query"** sekmesine tıklayın
3. SQL sorgularını buraya yapıştırıp çalıştırın
4. **Bağlantı bilgilerine gerek yok!**

### Railway CLI

```bash
railway connect postgres
```

## 📋 DBeaver'da Bağlantı Oluşturma

1. **DBeaver** → **Database** → **New Database Connection**
2. **PostgreSQL** seçin
3. **Main** sekmesinde:
   - **Host:** `postgres.railway.internal`
   - **Port:** `5432`
   - **Database:** `railway` (veya Railway'deki database adı)
   - **Username:** `postgres`
   - **Password:** Railway'deki şifre
4. **Test Connection** → **Finish**

## 🔍 Gerçek Değerleri Kontrol Etme

Railway Dashboard'dan gerçek değerleri kontrol etmek için:

1. **Railway Dashboard** → **Cravexv5** → **Postgres** servisi → **Variables**
2. VEYA **Railway Dashboard** → **Cravexv5** → **Postgres** servisi → **Settings** → **Networking**

Buradan gerçek host, port, database, username ve password bilgilerini görebilirsiniz.


