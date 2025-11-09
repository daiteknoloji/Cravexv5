# Synapse Server Name Sorunu - Final Çözüm

## 🔍 Durum

Tüm tablolarda (`users`, `room_memberships`, `profiles`, `user_directory`) sadece `cravex1-production.up.railway.app` domain'i var. Ama Synapse hala hata veriyor.

Bu durum, Synapse'in **metadata/config tablolarında** eski `server_name` kaydı olduğunu gösteriyor.

## 🔎 Adım 1: Metadata Tablolarını Kontrol Et

Railway PostgreSQL'de şu sorguyu çalıştırın:

```sql
-- Schema version tablosunu kontrol et
SELECT * FROM schema_version;

-- Tüm tabloları listele
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- "server_name" içeren kolonları bul
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND (column_name LIKE '%server%' OR column_name LIKE '%name%' OR column_name LIKE '%domain%')
ORDER BY table_name, column_name;
```

## 💡 Çözüm: Veritabanını Tamamen Temizle

Synapse'in metadata'sında eski `server_name` kaydı var ve bunu temizlemenin en garantili yolu **veritabanını tamamen temizlemek**.

### ⚠️ ÖNEMLİ: Önce Yedek Alın!

1. Railway Dashboard → PostgreSQL servisinizi seçin
2. "Settings" sekmesi → "Backups" bölümü
3. "Create Backup" butonuna tıklayın

### 🗑️ Veritabanını Temizle

Railway PostgreSQL'de şu SQL'i çalıştırın:

```sql
-- Tüm tabloları sil
DROP SCHEMA public CASCADE;

-- Schema'yı yeniden oluştur
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

### 🚀 Synapse'i Yeniden Başlat

1. Railway Dashboard → Cravexv5 (Synapse) servisinizi seçin
2. "Deployments" sekmesi → "Redeploy" butonuna tıklayın
3. Veya servisi durdurup tekrar başlatın

Synapse başladığında:
- ✅ Otomatik olarak şemayı yeniden oluşturacak
- ✅ `server_name: cravex1-production.up.railway.app` ile kaydedecek
- ✅ Artık hata vermeyecek

### 📝 Notlar

- Bu işlem **TÜM VERİLERİ SİLECEKTİR** (kullanıcılar, odalar, mesajlar, vb.)
- Eğer verileri korumak istiyorsanız, önce yedek alın
- Synapse başladıktan sonra kullanıcılar yeniden kayıt olabilir
- Odalar yeniden oluşturulabilir

## 🎯 Alternatif: Sadece Metadata'yı Temizle (Deneysel)

Eğer verileri korumak istiyorsanız, önce metadata tablolarını kontrol edin ve sadece onları temizleyin. Ama bu garantili değil.

```sql
-- Schema version'ı sıfırla (DİKKAT: Bu Synapse'i bozabilir!)
-- Sadece metadata tablolarını bulduktan sonra deneyin
TRUNCATE TABLE schema_version;
```

**Öneri:** En garantili çözüm veritabanını tamamen temizlemektir.


