# Admin Password Reset - Token ile

## Durum
- ✅ Admin Panel login: `admin` / `admin123` (hardcoded) - Çalışıyor
- ❌ Element Web login: `admin` / `GüçlüBirŞifre123!` - Çalışmıyor
- ✅ can.cakir login: Başarılı

## Çözüm: can.cakir Token'ı ile Admin User Şifresini Reset Et

### Adım 1: can.cakir'in Token'ını Bul

Railway PostgreSQL'e bağlan ve şu sorguyu çalıştır:

```sql
SELECT token, user_id, id
FROM access_tokens
WHERE user_id = '@can.cakir:matrix-synapse.up.railway.app'
ORDER BY id DESC
LIMIT 1;
```

Token'ı kopyala (örn: `syt_Y2FuLmNha2ly_...`)

### Adım 2: Matrix Admin API ile Admin User Şifresini Reset Et

Terminal'de veya Postman'de şu komutu çalıştır:

```bash
curl -X POST "https://matrix-synapse.up.railway.app/_synapse/admin/v1/reset_password/@admin:matrix-synapse.up.railway.app" \
  -H "Authorization: Bearer CAN_CAKIR_TOKEN_BURAYA" \
  -H "Content-Type: application/json" \
  -d '{"new_password": "GüçlüBirŞifre123!", "logout_devices": false}'
```

**ÖNEMLİ:** `CAN_CAKIR_TOKEN_BURAYA` yerine yukarıdaki sorgudan aldığın token'ı yapıştır.

### Adım 3: Başarı Kontrolü

Başarılı yanıt:
```json
{}
```

Hata yanıtı:
```json
{
  "errcode": "M_FORBIDDEN",
  "error": "You are not a server admin"
}
```

Eğer hata alırsan, `can.cakir` kullanıcısının admin yetkisi yok demektir.

### Adım 4: Matrix Synapse Restart

Railway Dashboard → Matrix Synapse servisi → **Restart**

### Adım 5: Element Web'de Login Test Et

1. Element Web'e git
2. Login: `admin` / `GüçlüBirŞifre123!`
3. Başarılı olmalı ✅

## Alternatif: can.cakir Admin Yetkisi Yoksa

Eğer `can.cakir` admin değilse, admin user şifresini PostgreSQL'de direkt güncelle:

### Adım 1: Python ile Hash Oluştur

```python
import bcrypt
password = "GüçlüBirŞifre123!"
salt = bcrypt.gensalt(rounds=12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
print(password_hash)
```

### Adım 2: PostgreSQL'de Güncelle

```sql
UPDATE users 
SET password_hash = '$2b$12$8GbwZmanHiZpFa9HzSgQA.0DTePvzbdGJXYI3GfIRlYCDIUJ5HP1e'
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

### Adım 3: Matrix Synapse Restart

Railway Dashboard → Matrix Synapse servisi → **Restart**

## Notlar

- Admin Panel login hardcoded (`admin123`) - Matrix Synapse'den bağımsız ✅
- Element Web login Matrix Synapse'e bağlı - Matrix Synapse'deki admin user şifresi gerekli ❌
- `ADMIN_PASSWORD` environment variable Matrix Admin API auto-login için kullanılıyor

## Sonraki Adım

1. ✅ can.cakir token'ını bul
2. ✅ Matrix Admin API ile admin user şifresini reset et
3. ✅ Matrix Synapse'i restart et
4. ✅ Element Web'de admin login test et

Sonuçları paylaş!

