# Veritabanını Tamamen Temizleme

## 🔍 Sorun

Loglar gösteriyor ki şema hala var: `Existing schema is 92 (+15 deltas)`

Bu demek oluyor ki `DROP SCHEMA public CASCADE` komutu çalışmadı veya Synapse şemayı tekrar oluşturdu.

## 🛠️ Çözüm: Veritabanını Tamamen Temizle

### Adım 1: Synapse Servisini Durdur

**ÖNEMLİ:** Synapse çalışırken şemayı silemezsiniz!

1. Railway Dashboard → **Cravexv5** (Synapse) servisinizi seçin
2. **"Settings"** → **"Stop"** butonuna tıklayın
3. Servisin durduğunu doğrulayın

### Adım 2: Veritabanını Temizle

Railway PostgreSQL'de şu SQL'i çalıştırın:

```sql
-- 1. Tüm bağlantıları kes
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = current_database()
  AND pid <> pg_backend_pid();

-- 2. Tüm tabloları sil
DROP SCHEMA public CASCADE;

-- 3. Schema'yı yeniden oluştur
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- 4. Doğrulama: Şema boş mu?
SELECT COUNT(*) as tablo_sayisi 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

**Sonuç 0 olmalı!** Eğer 0 değilse, şema hala var demektir.

### Adım 3: Synapse'i Yeniden Başlat

1. Railway Dashboard → **Cravexv5**
2. **"Settings"** → **"Start"** butonuna tıklayın
3. Logları izleyin

Synapse başladığında:
- ✅ Şemayı otomatik oluşturacak
- ✅ `server_name: cravex1-production.up.railway.app` ile kaydedecek
- ✅ Artık hata olmayacak

## 📋 Beklenen Loglar

Başarılı başlangıçta şunları görmelisiniz:

```
✅ Preparing database...
✅ Creating database schema...
✅ Database schema created successfully
✅ Starting server...
✅ Server started successfully
```

**Artık "Found users in database not native to..." hatası olmamalı!**

## ⚠️ ÖNEMLİ NOTLAR

1. **Synapse'i durdurmadan şemayı silemezsiniz** - Bağlantılar engelleyecektir
2. **Şema silindikten sonra Synapse'i hemen başlatın** - Synapse şemayı otomatik oluşturacak
3. **Tüm veriler silinecek** - Kullanıcılar, odalar, mesajlar, vb.

## 🔍 Sorun Devam Ederse

Eğer hala sorun varsa:

1. **Şema kontrolü:**
```sql
SELECT COUNT(*) as tablo_sayisi 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

2. **Schema version kontrolü:**
```sql
SELECT * FROM schema_version;
```

Eğer bu sorgular sonuç döndürüyorsa, şema hala var demektir. Tekrar silin.


