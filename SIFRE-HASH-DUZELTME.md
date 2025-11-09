# Şifre Hash Düzeltme Rehberi

## Sorun
Kullanıcı oluşturulduktan sonra login olamıyor. Şifre hash'i veritabanında var ama Matrix Synapse doğrulayamıyor.

## Matrix Synapse Şifre Hash Formatı

Matrix Synapse bcrypt kullanır ama özel bir format bekler:
- Format: `$2b$12$...` (bcrypt, 12 rounds)
- Hash uzunluğu: 60 karakter
- Salt: Otomatik oluşturulur

## Kontrol Edilmesi Gerekenler

1. **Mevcut Admin Kullanıcısının Hash'ini Kontrol Et:**
```sql
SELECT name, password_hash FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';
```

2. **Yeni Kullanıcının Hash'ini Kontrol Et:**
```sql
SELECT name, password_hash FROM users WHERE name = '@9test:matrix-synapse.up.railway.app';
```

3. **Hash Formatını Karşılaştır:**
- İkisi de `$2b$12$` ile başlamalı
- İkisi de 60 karakter olmalı
- Format aynı olmalı

## Olası Sorunlar

1. **Hash Formatı Yanlış:** Python bcrypt ile oluşturulan hash Matrix Synapse tarafından okunamıyor olabilir
2. **Encoding Sorunu:** Hash string olarak kaydedilirken encoding sorunu olabilir
3. **Salt Sorunu:** Salt doğru oluşturulmamış olabilir

## Çözüm

Matrix Synapse'in kendi şifre hash mekanizmasını kullanmak en iyisi. Ama Matrix API kullanılamıyorsa, doğru format ile hash oluşturmalıyız.

