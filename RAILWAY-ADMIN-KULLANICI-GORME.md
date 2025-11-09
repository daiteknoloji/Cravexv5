# 🔍 RAILWAY'DE ADMIN KULLANICIYI GÖRME REHBERİ

## 📊 Veritabanı Bilgileri

**Admin kullanıcısı şu veritabanına kaydedildi:**
- **Platform:** Railway
- **Database:** PostgreSQL
- **Database Name:** `railway` (veya `synapse`)
- **Table:** `users`
- **Kullanıcı ID:** `@admin:matrix-synapse.up.railway.app`

---

## 🎯 YÖNTEM 1: Railway Dashboard'dan (ÖNERİLEN)

### Adım 1: Railway Dashboard'a Gidin
1. https://railway.app/dashboard
2. `cravexv5` projesini seçin
3. **PostgreSQL** servisini bulun

### Adım 2: Query Sekmesini Açın
1. PostgreSQL servisi → **Query** sekmesi
2. Veya **Data** → **Query**

### Adım 3: SQL Sorgusu Çalıştırın

**Tüm kullanıcıları görmek için:**
```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    is_guest,
    admin,
    deactivated,
    creation_ts,
    TO_TIMESTAMP(creation_ts/1000) as olusturma_tarihi
FROM users
ORDER BY creation_ts DESC;
```

**Sadece admin kullanıcısını görmek için:**
```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    admin,
    deactivated,
    TO_TIMESTAMP(creation_ts/1000) as olusturma_tarihi
FROM users
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

---

## 🎯 YÖNTEM 2: Railway CLI ile

### Adım 1: Railway CLI Kurulumu
```bash
npm i -g @railway/cli
railway login
```

### Adım 2: PostgreSQL'e Bağlan
```bash
railway connect
```

### Adım 3: SQL Sorgusu Çalıştır
```sql
SELECT name, admin, deactivated FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';
```

---

## 🎯 YÖNTEM 3: PowerShell Script ile

Yeni bir script oluşturabilirim:

```powershell
# Railway PostgreSQL'e bağlan ve kullanıcıları listele
$railwayDbUrl = "postgresql://postgres:PASSWORD@HOST:PORT/railway"

# Kullanıcıları listele
psql $railwayDbUrl -c "SELECT name, admin, deactivated FROM users;"
```

---

## 📋 KULLANICI BİLGİLERİ

**Oluşturulan admin kullanıcısı:**
- **User ID:** `@admin:matrix-synapse.up.railway.app`
- **Username:** `admin`
- **Domain:** `matrix-synapse.up.railway.app`
- **Admin:** `true` (1)
- **Deactivated:** `false` (0)
- **Created:** Az önce oluşturuldu

---

## 🔍 DETAYLI SORGULAR

### Kullanıcı Sayısı:
```sql
SELECT COUNT(*) as toplam_kullanici FROM users;
```

### Admin Kullanıcıları:
```sql
SELECT name, admin, deactivated 
FROM users 
WHERE admin = true;
```

### Domain Bazında Kullanıcılar:
```sql
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2);
```

### Son Oluşturulan Kullanıcılar:
```sql
SELECT 
    name,
    TO_TIMESTAMP(creation_ts/1000) as olusturma_tarihi,
    admin
FROM users
ORDER BY creation_ts DESC
LIMIT 10;
```

---

## 📍 VERİTABANI KONUMU

**Railway PostgreSQL:**
- **Host:** Railway tarafından yönetiliyor
- **Database:** `railway` veya `synapse`
- **User:** `postgres`
- **Password:** Railway environment variable'da

**Önemli Tablolar:**
- `users` - Kullanıcı bilgileri
- `profiles` - Kullanıcı profilleri
- `rooms` - Odalar
- `events` - Mesajlar ve event'ler
- `room_memberships` - Kullanıcı-oda ilişkileri

---

## ✅ HIZLI KONTROL

Railway Dashboard → PostgreSQL → Query sekmesinde şu sorguyu çalıştırın:

```sql
SELECT name, admin FROM users WHERE name LIKE '%admin%';
```

Bu sorgu admin kullanıcısını gösterecek!

---

**Not:** Railway Dashboard'dan Query sekmesi en kolay yöntemdir. SQL bilgisi gerektirmez, sadece sorguyu kopyala-yapıştır yapın!


