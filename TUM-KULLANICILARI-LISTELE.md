# Tüm Kullanıcıları Listeleme

## 🔍 Railway PostgreSQL'de Kullanıcıları Listeleme

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesine gidin.

## 📊 SQL Sorguları

### 1. Tüm Kullanıcıları Detaylı Listele

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    creation_ts,
    TO_TIMESTAMP(creation_ts) as olusturma_tarihi,
    admin,
    deactivated,
    is_guest
FROM users
ORDER BY domain, name;
```

**Sonuç:** Tüm kullanıcılar, domain'leri, oluşturulma tarihleri ve durumları

### 2. Domain Bazında Kullanıcı Sayısı

```sql
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi,
    COUNT(*) FILTER (WHERE admin = 1) as admin_sayisi,
    COUNT(*) FILTER (WHERE deactivated = 1) as deaktif_sayisi,
    COUNT(*) FILTER (WHERE is_guest = 1) as guest_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

**Sonuç:** Her domain'de kaç kullanıcı var, kaç admin var, kaç deaktif var

### 3. Sadece Aktif Kullanıcılar

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    TO_TIMESTAMP(creation_ts) as olusturma_tarihi
FROM users
WHERE deactivated = 0
ORDER BY domain, name;
```

**Sonuç:** Sadece aktif (deaktif edilmemiş) kullanıcılar

### 4. Sadece Admin Kullanıcılar

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    TO_TIMESTAMP(creation_ts) as olusturma_tarihi
FROM users
WHERE admin = 1
ORDER BY domain, name;
```

**Sonuç:** Sadece admin yetkisine sahip kullanıcılar

### 5. Basit Liste (Sadece Kullanıcı ID'leri)

```sql
SELECT name as kullanici_id
FROM users
ORDER BY name;
```

**Sonuç:** Sadece kullanıcı ID'leri (örn: `@user1:cravex1-production.up.railway.app`)

### 6. Domain Kontrolü (Hangi Domain'ler Var?)

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

**Sonuç:** Veritabanında hangi domain'ler var ve her birinde kaç kullanıcı var

## 🎯 En Önemli Sorgu

Eğer sadece **hangi domain'lerin olduğunu** görmek istiyorsanız:

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

Bu sorgu size şunu gösterecek:
- `cravex1-production.up.railway.app` → 18 kullanıcı
- `matrix-synapse-production.up.railway.app` → 0 kullanıcı
- vb.

## 📝 Kullanım

1. Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesi
2. Yukarıdaki sorgulardan birini seçin
3. Sorguyu kopyalayıp yapıştırın
4. **"Run Query"** butonuna tıklayın
5. Sonuçları görüntüleyin

## ⚠️ DİKKAT

- Eğer `users` tablosu yoksa, Synapse henüz başlamamış veya veritabanı temizlenmiş demektir
- Eğer sorgu hata verirse, Synapse'in veritabanı şemasını oluşturmasını bekleyin


