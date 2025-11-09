# Matrix Login Debug Adımları

## Sorun
Matrix Synapse restart sonrası hala login başarısız:
```
Failed password login for user @test3:matrix-synapse.up.railway.app
SynapseError: 403 - Invalid username or password
```

## Debug Adımları

### 1. Railway Admin Panel Loglarını Kontrol Et

Railway Dashboard → Admin Panel servisi → Logs

`test3` kullanıcısı oluşturulurken şu logları ara:
- `[DEBUG] Created user @test3:matrix-synapse.up.railway.app`
- `[DEBUG] Password hash verification PASSED!`
- `[INFO] Password hash verification PASSED! Login should work!`

**Eğer bu loglar görünüyorsa:** Password hash doğru kaydedilmiş demektir.

### 2. Veritabanındaki Password Hash'i Kontrol Et

Railway PostgreSQL'e bağlan ve şu sorguyu çalıştır:

```sql
SELECT 
    name,
    password_hash,
    LENGTH(password_hash) as hash_length,
    SUBSTRING(password_hash, 1, 7) as hash_prefix,
    deactivated,
    creation_ts
FROM users
WHERE name = '@test3:matrix-synapse.up.railway.app';
```

**Beklenen Sonuç:**
- `password_hash`: `$2b$12$...` ile başlamalı (60 karakter)
- `hash_length`: 60
- `hash_prefix`: `$2b$12$`
- `deactivated`: `0`

### 3. User Directory Kontrolü

Matrix Synapse login için `user_directory` tablosunda kullanıcı olmalı:

```sql
SELECT user_id, display_name, avatar_url
FROM user_directory
WHERE user_id = '@test3:matrix-synapse.up.railway.app';
```

**Eğer kullanıcı yoksa:** Bu sorunun nedeni olabilir!

### 4. Matrix Synapse Loglarını Detaylı Kontrol Et

Railway Dashboard → Matrix Synapse servisi → Logs

Login denemesi sırasında şu logları ara:
- `Got login request with identifier`
- `Failed password login`
- `password_hash` ile ilgili herhangi bir log

**Önemli:** Matrix Synapse loglarında password hash'in nasıl okunduğunu görmek için daha detaylı log seviyesi gerekebilir.

### 5. Matrix Admin API ile Password Reset Dene

Eğer database'de password hash doğru ama login çalışmıyorsa, Matrix Admin API ile password reset dene:

```python
# Railway Admin Panel'de test endpoint oluştur
POST /api/users/@test3:matrix-synapse.up.railway.app/password
{
    "password": "12344321"
}
```

Bu, Matrix Synapse'in kendi password reset mekanizmasını kullanır ve sorunu çözebilir.

## Olası Sorunlar ve Çözümler

### Sorun 1: Password Hash Formatı
**Belirti:** Hash `$2b$12$` ile başlamıyor
**Çözüm:** Admin Panel'de password hash'i yeniden oluştur

### Sorun 2: User Directory Eksik
**Belirti:** `user_directory` tablosunda kullanıcı yok
**Çözüm:** Admin Panel'de kullanıcıyı yeniden oluştur veya manuel ekle

### Sorun 3: Matrix Synapse Cache
**Belirti:** Restart sonrası hala sorun var
**Çözüm:** Matrix Synapse'i birkaç kez restart et veya password'ü Matrix Admin API ile reset et

### Sorun 4: Password Hash Encoding
**Belirti:** Hash doğru format ama login çalışmıyor
**Çözüm:** Matrix Admin API kullanarak password reset yap

## Hızlı Test

1. **Yeni kullanıcı oluştur** (`test4`, şifre: `12344321`)
2. **Railway Admin Panel loglarını kontrol et** (password hash verification PASSED görünmeli)
3. **Veritabanını kontrol et** (password hash `$2b$12$` ile başlamalı)
4. **User directory kontrolü** (kullanıcı olmalı)
5. **Login dene** (Element Web)
6. **Matrix Synapse loglarını kontrol et** (hata mesajı)

## Sonraki Adım

Eğer tüm kontroller geçti ama login hala çalışmıyorsa:
1. Matrix Admin API ile password reset yap
2. Matrix Synapse'i birkaç kez restart et
3. Matrix Synapse config dosyasını kontrol et (`homeserver.yaml`)

