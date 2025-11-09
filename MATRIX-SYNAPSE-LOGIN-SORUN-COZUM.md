# Matrix Synapse Login Sorunu Çözüm Rehberi

## Sorun
Matrix Synapse loglarında şu hata görünüyor:
```
Failed password login for user @test1:matrix-synapse.up.railway.app
SynapseError: 403 - Invalid username or password
```

Admin Panel loglarında ise:
```
Password hash verification PASSED! Login should work!
```

Bu, password hash'in veritabanında doğru kaydedildiğini ama Matrix Synapse'in bunu okuyamadığını gösteriyor.

## Olası Nedenler

1. **Matrix Synapse Cache'i Güncel Değil**
   - Matrix Synapse password hash'leri cache'liyor olabilir
   - Yeni kullanıcılar veya password değişiklikleri cache'e yansımamış olabilir

2. **Password Hash Formatı Uyumsuzluğu**
   - Matrix Synapse password hash'i farklı bir formattan okuyor olabilir
   - Veritabanında TEXT/VARCHAR olarak kaydedilmiş ama Matrix Synapse BYTEA bekliyor olabilir

3. **Matrix Synapse Restart Gerekli**
   - Matrix Synapse'in yeni kullanıcıları/şifreleri tanıması için restart gerekebilir

## Çözüm Adımları

### 1. Matrix Synapse'i Yeniden Başlat (ÖNCE BUNU DENE!)

Railway Dashboard → Matrix Synapse servisi → **Restart**

Bu, cache'i temizler ve yeni password hash'leri okumasını sağlar.

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
WHERE name = '@test1:matrix-synapse.up.railway.app';
```

**Beklenen Sonuç:**
- `password_hash`: `$2b$12$...` ile başlamalı
- `hash_length`: 60 karakter olmalı
- `hash_prefix`: `$2b$12$` olmalı
- `deactivated`: `0` olmalı

### 3. Matrix Synapse Loglarını Kontrol Et

Restart sonrası login denemesi yap ve logları kontrol et:

```
POST /_matrix/client/v3/login
Got login request with identifier: {'type': 'm.id.user', 'user': 'test1'}
Failed password login for user @test1:matrix-synapse.up.railway.app
```

Eğer hala aynı hata varsa, Matrix Synapse password hash'i okurken bir sorun var demektir.

### 4. Password Hash Formatını Kontrol Et

Matrix Synapse password hash'i şu formatta bekliyor:
- Format: `$2b$12$...` (bcrypt)
- Tip: TEXT/VARCHAR (string)
- Uzunluk: 60 karakter

Admin Panel'de password hash şu şekilde kaydediliyor:
```python
salt = bcrypt.gensalt(rounds=12)
password_hash_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
password_hash = password_hash_bytes.decode('utf-8')  # TEXT/VARCHAR string
```

Bu format Matrix Synapse'in beklediği formattır.

### 5. Matrix Synapse Config Kontrolü

`homeserver.yaml` dosyasında password hash formatı kontrol edilmeli:

```yaml
password_providers:
  - module: "synapse.util.password_policies.PasswordPolicyProvider"
```

Eğer özel bir password provider varsa, bu formatı değiştirebilir.

## Hızlı Test

1. **Matrix Synapse'i Restart Et** (Railway Dashboard)
2. **Yeni bir kullanıcı oluştur** (Admin Panel)
3. **Login dene** (Element Web)
4. **Logları kontrol et** (Railway Matrix Synapse Logs)

## Notlar

- Matrix Synapse restart genellikle sorunu çözer
- Eğer restart sonrası hala sorun varsa, password hash formatını kontrol et
- Matrix Synapse cache'i bazen güncel olmayabilir, restart gerekebilir

