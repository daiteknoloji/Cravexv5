# 🔍 Log Toplama Rehberi - Kullanıcı Oluşturma ve Login Sorunları

## 📋 Gerekli Loglar

### 1. **Railway Admin Panel Logları** (Kullanıcı Oluşturma Sırasında)

**Adımlar:**
1. Railway Dashboard'a git: https://railway.app
2. Admin Panel servisini seç
3. **Logs** sekmesine git
4. Yeni bir kullanıcı oluştur (örn: `testuser` / `12345678`)
5. Oluşturma sırasındaki tüm logları kopyala

**Aranacak Loglar:**
```
[DEBUG] Created user @testuser:matrix-synapse.up.railway.app
[DEBUG] Password hash verification test (bcrypt.checkpw)
[INFO] Password hash verification PASSED!
```

---

### 2. **Railway Matrix Synapse Logları** (Login Denemesi Sırasında)

**Adımlar:**
1. Railway Dashboard'a git
2. **Matrix Synapse** servisini seç
3. **Logs** sekmesine git
4. Element Web'de login denemesi yap
5. Login denemesi sırasındaki tüm logları kopyala

**Aranacak Loglar:**
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
```

---

### 3. **Element Web Console Logları** (Login Denemesi Sırasında)

**Adımlar:**
1. Element Web'i aç: https://surprising-emotion-production.up.railway.app
2. **F12** tuşuna bas (Developer Tools)
3. **Console** sekmesine git
4. **Clear console** butonuna tıkla
5. Login denemesi yap
6. Console'daki tüm hataları kopyala

**Aranacak Loglar:**
```
Failed to load resource: the server responded with a status of 403
matrix-synapse.up.railway.app/_matrix/client/v3/login
```

---

### 4. **Veritabanı Kontrolü** (SQL Sorguları)

Railway PostgreSQL'e bağlan ve şu sorguları çalıştır:

```sql
-- Kullanıcı bilgilerini kontrol et
SELECT 
    name, 
    password_hash, 
    deactivated, 
    admin, 
    creation_ts,
    is_guest
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Password hash formatını kontrol et
SELECT 
    name,
    LEFT(password_hash, 10) as hash_start,
    LENGTH(password_hash) as hash_length,
    password_hash LIKE '$2b$12$%' as is_bcrypt_format
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';

-- Kullanıcının profile'ını kontrol et
SELECT * FROM profiles WHERE user_id = '@testuser:matrix-synapse.up.railway.app';

-- Kullanıcının user_directory'de olup olmadığını kontrol et
SELECT * FROM user_directory WHERE user_id = '@testuser:matrix-synapse.up.railway.app';
```

---

## 🎯 Örnek Senaryo

1. **Yeni kullanıcı oluştur:**
   - Username: `testuser`
   - Password: `12345678`

2. **Railway Admin Panel Loglarını al:**
   - Kullanıcı oluşturma sırasındaki tüm loglar

3. **Element Web'de login dene:**
   - Username: `testuser`
   - Password: `12345678`

4. **Railway Matrix Synapse Loglarını al:**
   - Login denemesi sırasındaki tüm loglar

5. **Element Web Console Loglarını al:**
   - Console'daki tüm hatalar

6. **Veritabanı sorgularını çalıştır:**
   - Yukarıdaki SQL sorgularını çalıştır ve sonuçları paylaş

---

## 📝 Log Formatı

Lütfen logları şu formatta paylaşın:

```
=== RAILWAY ADMIN PANEL LOGS ===
[log içeriği buraya]

=== RAILWAY MATRIX SYNAPSE LOGS ===
[log içeriği buraya]

=== ELEMENT WEB CONSOLE LOGS ===
[log içeriği buraya]

=== DATABASE QUERY RESULTS ===
[SQL sorgu sonuçları buraya]
```

---

## ⚠️ Önemli Notlar

1. **Password hash verification PASSED** görünüyorsa ama login çalışmıyorsa:
   - Matrix Synapse'in password hash'i okuma şeklinde sorun olabilir
   - Kullanıcı deactivated durumda olabilir
   - Matrix Synapse'in beklediği bazı tablolar eksik olabilir

2. **403 Forbidden** hatası alıyorsanız:
   - Password hash formatı yanlış olabilir
   - Kullanıcı Matrix Synapse'de düzgün oluşturulmamış olabilir
   - Matrix Synapse'in beklediği bazı tablolar eksik olabilir

3. **CORS hatası** görüyorsanız:
   - Bu admin panel ile ilgili değil, Matrix Synapse'in CORS ayarları ile ilgili

---

## 🔧 Hızlı Test

Eğer hızlı bir test yapmak isterseniz:

```sql
-- Mevcut çalışan bir kullanıcının password hash formatını kontrol et
SELECT 
    name,
    LEFT(password_hash, 30) as hash_start,
    LENGTH(password_hash) as hash_length
FROM users 
WHERE name LIKE '@admin:%' 
LIMIT 1;

-- Yeni oluşturulan kullanıcının password hash formatını karşılaştır
SELECT 
    name,
    LEFT(password_hash, 30) as hash_start,
    LENGTH(password_hash) as hash_length
FROM users 
WHERE name = '@testuser:matrix-synapse.up.railway.app';
```

Bu iki sorgunun sonuçlarını karşılaştırın. Format aynı olmalı!

