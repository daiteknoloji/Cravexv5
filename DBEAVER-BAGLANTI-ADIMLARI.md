# DBeaver Railway PostgreSQL Bağlantı Adımları

## 🔐 Bağlantı Bilgileri

### Railway PostgreSQL Bağlantı Ayarları

```
Host: ballast.proxy.rlwy.net (Public Networking)
      VEYA postgres.railway.internal (Private Networking)
Port: 57560 (Public)
      VEYA 5432 (Private)
Database: railway (veya postgres)
Username: postgres
Password: BttVVxjSQvmpfthXVfDCPtvQKBywBPuH
```

## 📋 DBeaver'da Bağlantı Oluşturma

### Adım 1: Yeni Bağlantı Oluştur

1. **DBeaver**'ı açın
2. **Database** → **New Database Connection** tıklayın
3. **PostgreSQL** seçin ve **Next** tıklayın

### Adım 2: Bağlantı Bilgilerini Girin

**Main** sekmesi:

**Public Networking (Dışarıdan bağlanmak için):**
- **Host:** `ballast.proxy.rlwy.net`
- **Port:** `57560`
- **Database:** `railway` (veya `postgres`)
- **Username:** `postgres`
- **Password:** `BttVVxjSQvmpfthXVfDCPtvQKBywBPuH`

**Private Networking (Railway içinden):**
- **Host:** `postgres.railway.internal`
- **Port:** `5432`
- **Database:** `railway` (veya `postgres`)
- **Username:** `postgres`
- **Password:** `BttVVxjSQvmpfthXVfDCPtvQKBywBPuH`

### Adım 3: SSL Ayarları (Opsiyonel)

**Driver Properties** sekmesi:
- `ssl` → `true`
- `sslmode` → `require`

### Adım 4: Test ve Bağlan

1. **"Test Connection"** butonuna tıklayın
2. Eğer driver eksikse, DBeaver otomatik olarak indirecek
3. Bağlantı başarılıysa **"Finish"** tıklayın

## 🔗 Connection String Formatı

### Public Networking:
```
postgresql://postgres:BttVVxjSQvmpfthXVfDCPtvQKBywBPuH@ballast.proxy.rlwy.net:57560/railway
```

### Private Networking:
```
postgresql://postgres:BttVVxjSQvmpfthXVfDCPtvQKBywBPuH@postgres.railway.internal:5432/railway
```

## 🚀 Hızlı Bağlantı (URL ile)

DBeaver'da **URL** sekmesini kullanarak:

1. **New Database Connection** → **PostgreSQL**
2. **URL** sekmesine gidin
3. Connection string'i yapıştırın:
   ```
   postgresql://postgres:BttVVxjSQvmpfthXVfDCPtvQKBywBPuH@ballast.proxy.rlwy.net:57560/railway
   ```
4. **Test Connection** → **Finish**

## ⚠️ ÖNEMLİ NOTLAR

1. **Public Networking:** Dışarıdan bağlanmak için `ballast.proxy.rlwy.net:57560` kullanın
2. **Private Networking:** Railway içinden bağlanmak için `postgres.railway.internal:5432` kullanın
3. **Database:** Genellikle `railway` veya `postgres` olur
4. **SSL:** Railway PostgreSQL SSL gerektirebilir, SSL ayarlarını kontrol edin

## 🔍 Sorun Giderme

### Bağlantı Kurulamıyorsa

1. **Public Networking** açık mı kontrol edin (Railway Dashboard → Postgres → Settings → Networking)
2. **SSL** ayarlarını kontrol edin (Driver Properties → ssl: true, sslmode: require)
3. **Firewall** ayarlarını kontrol edin
4. **Database adını** kontrol edin (`railway` veya `postgres`)

### SSL Hatası Alıyorsanız

DBeaver'da:
1. **Driver Properties** sekmesine gidin
2. `ssl` → `true` ekleyin
3. `sslmode` → `require` ekleyin

## 📝 Alternatif: Railway Dashboard Query Sekmesi

En kolay yöntem Railway Dashboard'dan:

1. **Railway Dashboard** → **Cravexv5** → **Postgres** servisi
2. **"Query"** sekmesine tıklayın
3. SQL sorgularını buraya yapıştırıp çalıştırın
4. **Bağlantı bilgilerine gerek yok!**


