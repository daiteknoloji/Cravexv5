# ✅ NAVICAT DOĞRU BAĞLANTI BİLGİLERİ

## 🎯 RAILWAY POSTGRESQL BAĞLANTI BİLGİLERİ

Railway Networking'den aldığınız bilgiler:

```
Public Networking Domain: ballast.proxy.rlwy.net
Public Networking Port: 57560
PostgreSQL Port: 5432
```

---

## 🔧 NAVICAT BAĞLANTI AYARLARI

Navicat → Connection "1" → **Edit Connection**:

### General Tab:
```
Connection Name: Railway PostgreSQL
Host: ballast.proxy.rlwy.net
Port: 57560  ⚠️ ÖNEMLİ: Public networking port'unu kullanın!
Initial Database: railway (veya postgres)
User Name: postgres
Password: [Railway Variables'dan PGPASSWORD]
Save password: ✅
```

### ÖNEMLİ:
- **Host:** `ballast.proxy.rlwy.net` (Railway public domain)
- **Port:** `57560` (Public networking port - PostgreSQL port 5432 değil!)
- **Database:** `railway` veya `postgres`
- **Username:** `postgres` (veya Railway Variables'dan `PGUSER`)

---

## 📋 ADIM ADIM

1. **Navicat'ı açın**
2. **Connection "1" → Right Click → Edit Connection**
3. **General Tab'da güncelleyin:**
   ```
   Host: ballast.proxy.rlwy.net
   Port: 57560
   Initial Database: railway
   User Name: postgres
   Password: [Railway Variables'dan PGPASSWORD]
   ```
4. **Test Connection** butonuna tıklayın
5. Başarılı olursa **OK**

---

## 🔍 RAILWAY VARIABLES KONTROLÜ

Railway Dashboard → PostgreSQL → **Variables** sekmesinden:

```
PGUSER=postgres (veya başka bir değer)
PGPASSWORD=[şifre]
PGDATABASE=railway (veya postgres)
```

Bu bilgileri Navicat'ta kullanın.

---

## ⚠️ ÖNEMLİ NOTLAR

### Port Farkı:
- **Public Networking Port:** `57560` (Railway proxy port'u)
- **PostgreSQL Port:** `5432` (Internal port)
- **Navicat'ta:** `57560` kullanın! ✅

### Host:
- **Public Domain:** `ballast.proxy.rlwy.net` ✅
- **Internal Domain:** `postgres.railway.internal` ❌ (Navicat için çalışmaz)

---

## ✅ BAŞARILI BAĞLANTI KONTROLÜ

Navicat'ta bağlandıktan sonra:

1. **Database listesi görünmeli:**
   - `railway`
   - `postgres`

2. **Tables görünmeli:**
   - `users`
   - `profiles`
   - `user_directory`

3. **Query çalıştırın:**
   ```sql
   SELECT COUNT(*) FROM users;
   ```

---

## 🎯 ÖZET

**Navicat Connection Settings:**

```
Host: ballast.proxy.rlwy.net
Port: 57560
Database: railway
Username: postgres
Password: [Railway Variables'dan]
```

**Railway Variables'dan alınacak:**
- Railway Dashboard → PostgreSQL → Variables → `PGPASSWORD`

---

**SONUÇ:** Navicat'ta `ballast.proxy.rlwy.net:57560` kullanın ve bağlanın!


