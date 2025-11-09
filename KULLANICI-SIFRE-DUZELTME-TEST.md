# Kullanıcı Şifre Düzeltme Test Rehberi

## Sorun
@9test kullanıcısı oluşturuldu ama login olamıyor. Şifre hash'i veritabanında var ama Matrix Synapse doğrulayamıyor.

## Çözüm Adımları

### 1. Kullanıcının Durumunu Kontrol Et
```sql
SELECT name, deactivated, admin, is_guest, locked 
FROM users 
WHERE name = '@9test:matrix-synapse.up.railway.app';
```

### 2. Şifre Hash'ini Kontrol Et
```sql
SELECT name, password_hash, LENGTH(password_hash) as hash_length
FROM users 
WHERE name = '@9test:matrix-synapse.up.railway.app';
```

### 3. Admin Kullanıcısının Hash'ini Karşılaştır
```sql
SELECT name, password_hash, LENGTH(password_hash) as hash_length
FROM users 
WHERE name = '@admin:matrix-synapse.up.railway.app';
```

### 4. Şifreyi Admin Panel'den Değiştir
1. Admin Panel'e login ol
2. @9test kullanıcısını bul
3. "Şifre" butonuna tıkla
4. Yeni şifre gir: `12344321`
5. Kaydet

### 5. Matrix API ile Şifre Sıfırla (Alternatif)
Eğer Admin Panel çalışmazsa, Matrix API ile şifreyi sıfırlayabilirsiniz.

## Notlar

- Şifre hash formatı: `$2b$12$...` (bcrypt, 12 rounds)
- Hash uzunluğu: 60 karakter olmalı
- Kullanıcı `deactivated = 0` olmalı
- Kullanıcı `locked = false` olmalı

