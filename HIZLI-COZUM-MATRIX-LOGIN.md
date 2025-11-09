# 🚀 Hızlı Çözüm - Matrix Login Sorunu

## ❌ Sorun

Kullanıcı oluşturma çalışıyor, password hash doğru, ama Matrix Synapse login'i reddediyor (403 Forbidden).

## ✅ Hızlı Çözüm Adımları

### 1. Railway Matrix Synapse'i Yeniden Başlat

**Railway Dashboard → Matrix Synapse servisi → Restart**

Bu, cache sorununu çözebilir.

---

### 2. Railway Matrix Synapse Loglarını Kontrol Et

**Railway Dashboard → Matrix Synapse → Logs**

Element Web'de login denemesi yap:
- Username: `test1`
- Password: (oluşturduğun şifre)

Login denemesi sırasındaki tüm logları kopyala.

**Aranacak loglar:**
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
User @test1:matrix-synapse.up.railway.app
password_hash
bcrypt.checkpw
```

---

### 3. Element Web'de Username Formatını Kontrol Et

Element Web'de login yaparken:
- ✅ Username: `test1` (sadece username)
- ❌ Username: `@test1:matrix-synapse.up.railway.app` (full user ID - YANLIŞ!)

---

### 4. Veritabanını Kontrol Et

```sql
-- Kullanıcının deactivated durumunu kontrol et
SELECT 
    name,
    deactivated,
    is_guest,
    LEFT(password_hash, 30) as hash_start
FROM users 
WHERE name = '@test1:matrix-synapse.up.railway.app';

-- Eğer deactivated = 1 ise, 0 yap
UPDATE users 
SET deactivated = 0 
WHERE name = '@test1:matrix-synapse.up.railway.app';
```

---

## 🔧 Sorun Devam Ederse

Railway Matrix Synapse loglarını mutlaka kontrol et! Bu loglar sorunun kaynağını gösterecek.

**Örnek log formatı:**
```
2025-11-09T21:18:18.506274268Z [inf] POST /_matrix/client/v3/login
2025-11-09T21:18:18.506274268Z [err] M_FORBIDDEN: Invalid username or password
2025-11-09T21:18:18.506274268Z [err] User @test1:matrix-synapse.up.railway.app login failed
```

---

## ⚠️ Önemli Notlar

1. **Matrix Synapse'i yeniden başlat** - Cache sorununu çözebilir
2. **Railway Matrix Synapse loglarını kontrol et** - Sorunun kaynağını gösterir
3. **Element Web'de username formatını kontrol et** - Sadece username, full user ID değil

---

## 📝 Sonraki Adımlar

1. ✅ Matrix Synapse'i yeniden başlat
2. ✅ Railway Matrix Synapse loglarını kontrol et
3. ✅ Element Web'de login dene
4. ✅ Logları paylaş

**ÖNEMLİ:** Railway Matrix Synapse loglarını mutlaka kontrol et! Bu loglar sorunun kaynağını gösterecek.

