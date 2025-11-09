# Admin Password Reset Çözümü

## Sorun
- Admin user şifresi Matrix Synapse'de `GüçlüBirŞifre123!` değil
- `can.cakir` ile login başarılı ✅
- Admin Panel'de `ADMIN_PASSWORD="GüçlüBirŞifre123!"` ama Matrix Synapse'deki admin user şifresi farklı

## Çözüm: Admin User Şifresini Reset Et

### Seçenek 1: can.cakir Token'ı ile Matrix Admin API Kullan (ÖNERİLEN)

`can.cakir` kullanıcısının token'ını kullanarak admin user'ın şifresini reset et:

1. **Railway PostgreSQL'e bağlan**
2. **can.cakir'in token'ını bul:**
```sql
SELECT token, user_id
FROM access_tokens
WHERE user_id = '@can.cakir:matrix-synapse.up.railway.app'
ORDER BY id DESC
LIMIT 1;
```

3. **Matrix Admin API ile admin user şifresini reset et:**
```bash
curl -X POST "https://matrix-synapse.up.railway.app/_synapse/admin/v1/reset_password/@admin:matrix-synapse.up.railway.app" \
  -H "Authorization: Bearer CAN_CAKIR_TOKEN_BURAYA" \
  -H "Content-Type: application/json" \
  -d '{"new_password": "GüçlüBirŞifre123!", "logout_devices": false}'
```

### Seçenek 2: PostgreSQL'de Password Hash Güncelle (HIZLI)

Railway PostgreSQL'de admin user'ın password_hash'ini `GüçlüBirŞifre123!` şifresinin bcrypt hash'i ile güncelle:

1. **Python script ile bcrypt hash oluştur:**
```python
import bcrypt
password = "GüçlüBirŞifre123!"
salt = bcrypt.gensalt(rounds=12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
print(password_hash)
```

2. **PostgreSQL'de güncelle:**
```sql
UPDATE users 
SET password_hash = '$2b$12$...BURAYA_OLUSTURULAN_HASH...'
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

### Seçenek 3: ADMIN_PASSWORD'ü Mevcut Şifreye Eşleştir

Eğer Matrix Synapse'deki admin user şifresini biliyorsan:

1. **Railway Dashboard → Admin Panel → Variables**
2. **`ADMIN_PASSWORD` değerini Matrix Synapse'deki admin user şifresi ile eşleştir**
3. **Admin Panel'i restart et**

## Hızlı Çözüm: PostgreSQL'de Password Hash Güncelle

En hızlı çözüm PostgreSQL'de password_hash'i güncellemek:

### Adım 1: Python ile Hash Oluştur

```python
import bcrypt
password = "GüçlüBirŞifre123!"
salt = bcrypt.gensalt(rounds=12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
print(password_hash)
```

Bu komutu çalıştır ve çıktıyı kopyala.

### Adım 2: PostgreSQL'de Güncelle

Railway PostgreSQL'e bağlan ve şu SQL'i çalıştır (hash'i yukarıdaki çıktı ile değiştir):

```sql
UPDATE users 
SET password_hash = '$2b$12$...OLUSTURULAN_HASH_BURAYA...'
WHERE name = '@admin:matrix-synapse.up.railway.app';

-- Kontrol et
SELECT name, password_hash, admin, deactivated
FROM users
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

### Adım 3: Matrix Synapse Restart

Railway Dashboard → Matrix Synapse servisi → **Restart**

### Adım 4: Test Et

1. **Element Web'de admin login dene:**
   - Username: `admin`
   - Password: `GüçlüBirŞifre123!`
2. **Başarılı olmalı** ✅

## Notlar

- `can.cakir` ile login başarılı, bu kullanıcının admin yetkisi varsa Matrix Admin API kullanılabilir
- Admin user şifresi Matrix Synapse'de farklı olduğu için auto-login başarısız oluyor
- Password hash'i güncelledikten sonra Matrix Synapse restart gerekli

## Sonraki Adım

1. ✅ Password hash'i PostgreSQL'de güncelle
2. ✅ Matrix Synapse'i restart et
3. ✅ Element Web'de admin login test et
4. ✅ Admin Panel'de yeni kullanıcı oluşturmayı test et

Sonuçları paylaş!

