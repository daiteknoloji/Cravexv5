# Veritabanını Tamamen Temizleme (V1.0.0 için)

## 🔍 Sorun

Synapse crash oluyor çünkü veritabanında hala `cravex1-production.up.railway.app` domain'ine kayıtlı kullanıcılar var, ama Synapse şimdi `matrix-synapse-production.up.railway.app` olarak çalışmaya çalışıyor.

**Hata:**
```
Exception: Found users in database not native to matrix-synapse-production.up.railway.app!
You cannot change a synapse server_name after it's been configured
```

## ✅ Çözüm: Veritabanını Tamamen Temizle

### 1. Railway PostgreSQL'e Bağlan

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesine gidin.

### 2. Önce Domain'leri Kontrol Et

Aşağıdaki SQL sorgusunu çalıştırın:

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as user_count 
FROM users 
GROUP BY split_part(name, ':', 2)
ORDER BY user_count DESC;
```

Bu sorgu size hangi domain'lerin olduğunu gösterecek.

### 3. Synapse'i Durdurun

**ÖNEMLİ:** Synapse'i durdurmadan veritabanını temizlemeyin!

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **"Settings"** → **"Delete Service"** veya servisi durdurun.

### 4. Veritabanını Tamamen Temizle

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesinde aşağıdaki SQL komutlarını **SIRASIYLA** çalıştırın:

```sql
-- 1. Tüm bağlantıları kes
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = current_database()
  AND pid <> pg_backend_pid();
```

```sql
-- 2. Tüm tabloları sil
DROP SCHEMA public CASCADE;
```

```sql
-- 3. Schema'yı yeniden oluştur
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

```sql
-- 4. Doğrulama: Şema boş mu?
SELECT COUNT(*) as tablo_sayisi 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

**Sonuç `0` olmalı!**

### 5. Synapse'i Yeniden Başlatın

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **"Deploy"** veya servisi yeniden başlatın.

Synapse başladığında veritabanı şemasını otomatik olarak oluşturacak.

### 6. Logları Kontrol Edin

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **"Logs"** sekmesinde şunları kontrol edin:

- ✅ `Server hostname: matrix-synapse-production.up.railway.app`
- ✅ `Public Base URL: https://matrix-synapse-production.up.railway.app/`
- ✅ `Setting up server` mesajı
- ✅ Crash hatası YOK

## ⚠️ DİKKAT

Bu işlem **TÜM VERİLERİ SİLECEKTİR:**
- Tüm kullanıcılar
- Tüm odalar
- Tüm mesajlar
- Tüm medya dosyaları

Eğer önemli verileriniz varsa, önce backup alın!

## 📝 Notlar

- V1.0.0'da Synapse `matrix-synapse-production.up.railway.app` olarak çalışmalı
- Veritabanı temizlendikten sonra Synapse otomatik olarak şemayı oluşturacak
- İlk başlatmada şema oluşturma işlemi 1-2 dakika sürebilir


