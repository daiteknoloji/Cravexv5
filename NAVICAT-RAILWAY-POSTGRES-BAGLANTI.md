# 🔌 NAVICAT İLE RAILWAY POSTGRESQL BAĞLANTISI

## 📋 RAILWAY'DEN BAĞLANTI BİLGİLERİNİ ALMA

### Adım 1: Railway Dashboard'a Gidin

1. **Railway Dashboard:** https://railway.app/dashboard
2. **Projenizi seçin:** `cravexv5`
3. **PostgreSQL servisini seçin**

### Adım 2: Connection Info'yu Bulun

Railway Dashboard → PostgreSQL servisi → **Variables** sekmesi:

Şu variable'ları bulun:
- `PGHOST` - Host adresi
- `PGPORT` - Port (genellikle `5432`)
- `PGDATABASE` - Database adı
- `PGUSER` - Kullanıcı adı
- `PGPASSWORD` - Şifre

**VEYA:**

Railway Dashboard → PostgreSQL servisi → **Connect** sekmesi:
- Railway otomatik connection string gösterir

---

## 🔧 NAVICAT BAĞLANTI AYARLARI

### Yöntem 1: Railway Public Domain (Önerilen)

**Navicat → New Connection → PostgreSQL:**

```
Connection Name: Railway PostgreSQL
Host: [Railway PostgreSQL Public Domain]
Port: 5432
Initial Database: railway (veya PGDATABASE değeri)
User Name: [PGUSER değeri]
Password: [PGPASSWORD değeri]
```

**Railway Public Domain'i bulmak için:**
- Railway Dashboard → PostgreSQL servisi → **Networking** sekmesi
- **Public Domain** bölümünde domain'i göreceksiniz
- Örnek: `postgres-production.up.railway.app`

### Yöntem 2: Railway Internal Domain (Sadece Railway içinden)

**Navicat → New Connection → PostgreSQL:**

```
Connection Name: Railway PostgreSQL (Internal)
Host: postgres.railway.internal
Port: 5432
Initial Database: railway
User Name: [PGUSER değeri]
Password: [PGPASSWORD değeri]
```

**⚠️ NOT:** Bu yöntem sadece Railway network içinden çalışır (VPN gerekebilir).

---

## 📝 ADIM ADIM NAVICAT KURULUMU

### 1. Navicat'ı Açın

- Navicat → **File** → **New Connection** → **PostgreSQL**

### 2. General Tab Ayarları

```
Connection Name: Railway PostgreSQL
Host: [Railway Public Domain]
Port: 5432
Initial Database: railway
User Name: [PGUSER]
Password: [PGPASSWORD]
Save password: ✅ (işaretli)
```

### 3. Advanced Tab (Opsiyonel)

```
Connection Timeout: 30
Keep-Alive Interval: 30
```

### 4. SSL Tab (Gerekirse)

Railway PostgreSQL SSL kullanıyorsa:
```
SSL Mode: Require
```

### 5. Test Connection

- **Test Connection** butonuna tıklayın
- Başarılı olursa: ✅ "Connection successful"
- Hata alırsanız: Bağlantı bilgilerini kontrol edin

### 6. OK ve Bağlan

- **OK** butonuna tıklayın
- Connection listesinde görünecek
- Çift tıklayarak bağlanın

---

## 🔍 RAILWAY'DEN BAĞLANTI BİLGİLERİNİ BULMA

### Method 1: Variables Sekmesi

Railway Dashboard → PostgreSQL → **Variables**:

```
PGHOST=postgres.railway.internal (veya public domain)
PGPORT=5432
PGDATABASE=railway
PGUSER=postgres
PGPASSWORD=[şifre]
```

### Method 2: Connect Sekmesi

Railway Dashboard → PostgreSQL → **Connect**:

Railway otomatik connection string gösterir:
```
postgresql://postgres:[password]@[host]:5432/railway
```

Bu string'i parse ederek bilgileri çıkarabilirsiniz.

### Method 3: Networking Sekmesi

Railway Dashboard → PostgreSQL → **Networking**:

- **Public Domain:** PostgreSQL public domain'i
- **Port:** 5432

---

## ⚠️ SORUN GİDERME

### "Connection refused" Hatası

**Sorun:** Railway PostgreSQL public domain'e erişilemiyor.

**Çözüm:**
1. Railway Dashboard → PostgreSQL → **Networking**
2. **Public Networking** aktif mi kontrol edin
3. **Public Domain** oluşturun (yoksa)

### "Authentication failed" Hatası

**Sorun:** Kullanıcı adı veya şifre yanlış.

**Çözüm:**
1. Railway Dashboard → PostgreSQL → **Variables**
2. `PGUSER` ve `PGPASSWORD` değerlerini kontrol edin
3. Navicat'ta doğru değerleri girin

### "Database does not exist" Hatası

**Sorun:** Database adı yanlış.

**Çözüm:**
1. Railway Dashboard → PostgreSQL → **Variables**
2. `PGDATABASE` değerini kontrol edin
3. Genellikle `railway` veya `postgres` olur

### "Connection timeout" Hatası

**Sorun:** Railway PostgreSQL'e erişilemiyor.

**Çözüm:**
1. Railway Dashboard → PostgreSQL → **Networking**
2. **Public Domain** aktif mi kontrol edin
3. Firewall ayarlarını kontrol edin

---

## ✅ BAŞARILI BAĞLANTI KONTROLÜ

Navicat'ta bağlandıktan sonra:

1. **Database listesini görün:**
   - `railway` database'i görünmeli
   - `postgres` database'i görünmeli

2. **Tables listesini görün:**
   - `users` tablosu görünmeli
   - `profiles` tablosu görünmeli
   - `user_directory` tablosu görünmeli

3. **Query çalıştırın:**
   ```sql
   SELECT COUNT(*) FROM users;
   ```

---

## 📋 HIZLI REFERANS

**Navicat PostgreSQL Connection Settings:**

```
Host: [Railway Public Domain]
Port: 5432
Database: railway
Username: [PGUSER]
Password: [PGPASSWORD]
```

**Railway Dashboard'dan alınacak bilgiler:**
- Railway Dashboard → PostgreSQL → **Variables**
- Railway Dashboard → PostgreSQL → **Networking** → **Public Domain**

---

**SONUÇ:** Railway Dashboard'dan PostgreSQL connection bilgilerini alın ve Navicat'ta yapılandırın!


