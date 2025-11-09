# 🔍 Railway Matrix Synapse Log Kontrol Rehberi

## ❌ Sorun

Element Web console'da görülen hata:
```
POST https://matrix-synapse.up.railway.app/_matrix/client/v3/login [403]
Login failed M_FORBIDDEN: Invalid username or password
```

Bu, Matrix Synapse'in login'i reddettiği anlamına geliyor.

---

## 🎯 Railway Matrix Synapse Loglarını Kontrol Et

### Adımlar:

1. **Railway Dashboard'a git:** https://railway.app
2. **Matrix Synapse servisini seç**
3. **Logs sekmesine git**
4. **Element Web'de login denemesi yap:**
   - Username: `test1`
   - Password: (oluşturduğun şifre)
5. **Login denemesi sırasındaki tüm logları kopyala**

---

## 🔍 Aranacak Loglar

### 1. Login Denemesi Logları:
```
POST /_matrix/client/v3/login
M_FORBIDDEN
Invalid username or password
User @test1:matrix-synapse.up.railway.app
```

### 2. Password Hash Kontrol Logları:
```
password_hash
bcrypt.checkpw
password verification
```

### 3. Kullanıcı Bulunamadı Logları:
```
User not found
User @test1:matrix-synapse.up.railway.app
```

### 4. Database Query Logları:
```
SELECT.*FROM users
password_hash
```

---

## 📝 Örnek Log Formatı

```
2025-11-09T21:18:18.506274268Z [inf] POST /_matrix/client/v3/login
2025-11-09T21:18:18.506274268Z [err] M_FORBIDDEN: Invalid username or password
2025-11-09T21:18:18.506274268Z [err] User @test1:matrix-synapse.up.railway.app login failed
2025-11-09T21:18:18.506274268Z [err] password_hash check failed
2025-11-09T21:18:18.506274268Z [err] bcrypt.checkpw returned False
```

---

## ⚠️ Önemli Notlar

1. **Railway Matrix Synapse loglarını mutlaka kontrol et!**
2. **Login denemesi sırasındaki tüm logları kopyala**
3. **Özellikle password hash kontrol loglarını ara**

---

## 🔧 Sonraki Adımlar

1. ✅ Railway Matrix Synapse loglarını kontrol et
2. ✅ Login denemesi sırasındaki tüm logları kopyala
3. ✅ Logları paylaş

**ÖNEMLİ:** Railway Matrix Synapse logları sorunun kaynağını gösterecek!

