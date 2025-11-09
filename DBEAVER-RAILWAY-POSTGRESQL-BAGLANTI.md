# DBeaver'dan Railway PostgreSQL'e Bağlanma

## 🔍 Railway PostgreSQL Bağlantı Bilgileri

### Railway Dashboard'dan Bilgileri Alma

1. **Railway Dashboard** → **Cravexv5** projesine gidin
2. **Postgres** servisini seçin
3. **"Variables"** sekmesine gidin
4. Şu bilgileri not edin:
   - `PGHOST` → Host adresi
   - `PGPORT` → Port (genellikle 5432)
   - `PGDATABASE` → Veritabanı adı (genellikle `railway` veya `postgres`)
   - `PGUSER` → Kullanıcı adı (genellikle `postgres`)
   - `PGPASSWORD` → Şifre

### Alternatif: Railway CLI ile

```bash
railway connect postgres
```

Bu komut size bağlantı bilgilerini gösterecek.

## 📋 DBeaver Bağlantı Ayarları

### 1. Yeni Bağlantı Oluşturma

1. **DBeaver**'ı açın
2. **"Database"** → **"New Database Connection"** tıklayın
3. **"PostgreSQL"** seçin ve **"Next"** tıklayın

### 2. Bağlantı Bilgilerini Girme

**Main** sekmesi:
- **Host:** `postgres.railway.internal` (Railway internal network)
  - VEYA Railway'in verdiği external host (eğer varsa)
- **Port:** `5432` (veya Railway'deki port)
- **Database:** `railway` (veya Railway'deki database adı)
- **Username:** `postgres` (veya Railway'deki kullanıcı adı)
- **Password:** Railway'deki şifre

**Driver Properties** sekmesi (opsiyonel):
- `ssl` → `true` (eğer SSL gerekiyorsa)
- `sslmode` → `require` (eğer SSL gerekiyorsa)

### 3. Test ve Bağlanma

1. **"Test Connection"** butonuna tıklayın
2. Eğer driver eksikse, DBeaver otomatik olarak indirecek
3. Bağlantı başarılıysa **"Finish"** tıklayın

## 🔐 Railway PostgreSQL Bağlantı Bilgileri (Örnek)

```
Host: postgres.railway.internal
Port: 5432
Database: railway
Username: postgres
Password: [Railway'den alınan şifre]
```

**Not:** Railway internal network'ünde `postgres.railway.internal` kullanılır. Eğer external bağlantı gerekiyorsa, Railway'in verdiği external host'u kullanın.

## 🌐 External Bağlantı (Eğer Gerekiyorsa)

Railway PostgreSQL'e external bağlantı için:

1. **Railway Dashboard** → **Cravexv5** → **Postgres** servisi
2. **"Settings"** sekmesine gidin
3. **"Public Networking"** veya **"External Access"** seçeneğini açın
4. Railway size bir external host ve port verecek
5. Bu bilgileri DBeaver'da kullanın

## ⚠️ ÖNEMLİ NOTLAR

1. **Internal Network:** Railway servisleri arasında `postgres.railway.internal` kullanılır
2. **External Access:** Dışarıdan bağlanmak için Railway'in external host'unu kullanmanız gerekir
3. **Password:** Railway'deki `PGPASSWORD` environment variable'ından şifreyi alın
4. **SSL:** Railway PostgreSQL SSL gerektirebilir, DBeaver'da SSL ayarlarını kontrol edin

## 🚀 Hızlı Bağlantı

Eğer Railway CLI kullanıyorsanız:

```bash
railway connect postgres
```

Bu komut size bağlantı bilgilerini ve connection string'i gösterecek.

## 📝 Connection String Formatı

```
postgresql://postgres:password@postgres.railway.internal:5432/railway
```

DBeaver'da bu connection string'i de kullanabilirsiniz:
1. **"New Database Connection"** → **"PostgreSQL"**
2. **"URL"** sekmesine gidin
3. Connection string'i yapıştırın

## 🔍 Sorun Giderme

### Bağlantı Kurulamıyorsa

1. **Railway Dashboard**'da Postgres servisinin çalıştığını kontrol edin
2. **Variables** sekmesinde bağlantı bilgilerini kontrol edin
3. **External Access** açık mı kontrol edin (eğer external bağlanıyorsanız)
4. **Firewall** ayarlarını kontrol edin

### SSL Hatası Alıyorsanız

DBeaver'da:
1. **Driver Properties** sekmesine gidin
2. `ssl` → `true` ekleyin
3. `sslmode` → `require` ekleyin

### Host Bulunamıyor Hatası

- Railway internal network'ünde `postgres.railway.internal` kullanın
- VEYA Railway'in verdiği external host'u kullanın
- Railway Dashboard → Postgres → Settings → Networking bölümünden kontrol edin


