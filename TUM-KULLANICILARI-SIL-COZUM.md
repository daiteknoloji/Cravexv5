# Tüm Kullanıcıları Silme - Sorun Çözümü

## ✅ Evet, Tüm Kullanıcıları Silerseniz Sorun Çözülecek!

Eğer veritabanındaki **tüm kullanıcıları** silerseniz, Synapse `matrix-synapse-production.up.railway.app` olarak başarıyla başlayacak.

## 📋 Adım Adım Çözüm

### 1. Synapse'i Durdurun

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Settings** → servisi durdurun.

**ÖNEMLİ:** Synapse çalışırken kullanıcı silme işlemi yapmayın!

### 2. Railway PostgreSQL Query Sekmesine Gidin

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesi.

### 3. Önce Kontrol Edin

Kaç kullanıcı var?

```sql
SELECT COUNT(*) as toplam_kullanici_sayisi FROM users;
```

Hangi domain'ler var?

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

### 4. Tüm Kullanıcıları Silin

Aşağıdaki SQL sorgularını **SIRASIYLA** çalıştırın:

```sql
-- 1. Önce TÜM kullanıcıların odalardaki üyeliklerini sil
DELETE FROM local_current_membership;

-- 2. TÜM room memberships'i sil
DELETE FROM room_memberships;

-- 3. TÜM user directory'den sil
DELETE FROM user_directory;

-- 4. TÜM profiles'den sil
DELETE FROM profiles;

-- 5. Son olarak TÜM users tablosundan sil
DELETE FROM users;
```

### 5. Doğrulama

Kullanıcılar silindi mi?

```sql
SELECT COUNT(*) as kalan_kullanici_sayisi FROM users;
```

**Sonuç `0` olmalı!**

### 6. Railway Environment Variable'ını Güncelleyin

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Variables** sekmesi:

`SYNAPSE_SERVER_NAME` değerini şu şekilde güncelleyin:
```
matrix-synapse-production.up.railway.app
```

### 7. Synapse'i Yeniden Başlatın

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Deploy** veya servisi yeniden başlatın.

### 8. Logları Kontrol Edin

Railway Dashboard → **Cravexv5** → **Synapse** servisi → **Logs** sekmesi:

**Beklenen log mesajları:**
```
Server hostname: matrix-synapse-production.up.railway.app
Public Base URL: https://matrix-synapse-production.up.railway.app/
Setting up server
```

**Crash hatası OLMAMALI!**

## ✅ Sonuç

- ✅ Veritabanı temizlendi
- ✅ Synapse `matrix-synapse-production.up.railway.app` olarak başlayacak
- ✅ Crash hatası olmayacak
- ✅ Yeni kullanıcılar oluşturabileceksiniz

## ⚠️ DİKKAT

- Bu işlem **GERİ ALINAMAZ!**
- **TÜM kullanıcılar** silinecek (admin dahil)
- **TÜM odalar ve mesajlar** da silinebilir (ilişkili tablolardan)
- Önemli verileriniz varsa önce **backup** alın

## 📝 Notlar

- Kullanıcıları sildikten sonra Synapse başladığında veritabanı şeması korunacak
- Yeni kullanıcılar oluşturabileceksiniz
- İlk admin kullanıcısını Synapse Admin Panel'den veya komut satırından oluşturmanız gerekecek

## 🚀 Sonraki Adımlar

1. Synapse başarıyla başladıktan sonra yeni kullanıcılar oluşturun
2. İlk admin kullanıcısını oluşturun
3. Element Web'den giriş yapıp test edin


