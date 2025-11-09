# Aktif/Pasif Yapma Test Rehberi

## Durum Kontrolü

### Pasif Yapma İşlemi:
1. ✅ Matrix API ile deactivate ediliyor
2. ✅ Access token'lar siliniyor (logout)
3. ✅ Devices siliniyor
4. ✅ Veritabanı güncelleniyor (`deactivated = 1`)

### Aktif Yapma İşlemi:
1. ✅ Matrix API ile activate ediliyor (`deactivated: False`)
2. ✅ Veritabanı güncelleniyor (`deactivated = 0`)
3. ⚠️ Matrix API timeout alırsa sadece veritabanı güncelleniyor

## Test Adımları

### 1. Kullanıcıyı Pasif Yap
- Admin Panel → Kullanıcılar → Pasif Yap
- Beklenen: Kullanıcı hemen logout olmalı

### 2. Kullanıcıyı Aktif Yap
- Admin Panel → Kullanıcılar → Aktif Yap
- Beklenen: Kullanıcı login olabilmeli

### 3. Login Testi
- Element Web'den login olmayı deneyin
- Beklenen: Login başarılı olmalı

## Sorun Giderme

### Eğer Aktif Yapıldıktan Sonra Login Olamıyorsa:

1. **Matrix API Timeout Kontrolü:**
   - Railway loglarını kontrol edin
   - "Matrix API timeout" mesajı görünüyor mu?

2. **Veritabanı Kontrolü:**
   ```sql
   SELECT name, deactivated FROM users WHERE name = '@kullanici:matrix-synapse.up.railway.app';
   ```
   - `deactivated = 0` olmalı

3. **Manuel Aktif Yapma:**
   - Veritabanında `deactivated = 0` yapın
   - Kullanıcı login olabilmeli

## Notlar

- Matrix API kullanılamazsa sadece veritabanı güncelleniyor
- Bu durumda Matrix Synapse kullanıcıyı hala pasif görebilir
- En iyi çözüm: Matrix API'nin çalışmasını sağlamak

