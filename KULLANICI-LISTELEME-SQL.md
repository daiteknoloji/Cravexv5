# Kullanıcı Listeleme SQL Sorguları

Railway PostgreSQL servisine bağlanıp şu sorguları çalıştırın:

## 🎯 Hızlı Kontrol - Domain Bazında Kullanıcı Sayıları

```sql
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

Bu sorgu size şunu gösterecek:
- Hangi domain'lerde kullanıcı var
- Her domain'de kaç kullanıcı var

## 📋 Tüm Kullanıcıları Listele

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain,
    created_ts as olusturulma_tarihi
FROM users
ORDER BY domain, name;
```

## 🔍 Her Domain'den Örnek Kullanıcılar

```sql
SELECT 
    split_part(name, ':', 2) as domain,
    name as kullanici_id,
    created_ts as olusturulma_tarihi
FROM (
    SELECT 
        name,
        created_ts,
        split_part(name, ':', 2) as domain,
        ROW_NUMBER() OVER (PARTITION BY split_part(name, ':', 2) ORDER BY created_ts DESC) as rn
    FROM users
) ranked
WHERE rn <= 3
ORDER BY domain, created_ts DESC;
```

## 📝 Railway'de Çalıştırma

### Yöntem 1: Railway Dashboard
1. Railway Dashboard'a gidin
2. PostgreSQL servisinizi seçin
3. "Data" sekmesine gidin
4. "Query" butonuna tıklayın
5. Yukarıdaki sorgulardan birini yapıştırın ve çalıştırın

### Yöntem 2: Railway CLI
```bash
railway run --service <postgres-service-name> psql -c "SELECT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi FROM users GROUP BY split_part(name, ':', 2) ORDER BY kullanici_sayisi DESC;"
```

### Yöntem 3: Railway Shell
```bash
railway run --service <postgres-service-name> psql
```
Sonra SQL sorgularını direkt çalıştırabilirsiniz.

## 💡 Beklenen Sonuç

Eğer sorun yoksa, sadece şunu görmelisiniz:
```
domain                                    | kullanici_sayisi
------------------------------------------+------------------
cravex1-production.up.railway.app        |                18
```

Eğer sorun varsa, şunu görebilirsiniz:
```
domain                                    | kullanici_sayisi
------------------------------------------+------------------
cravex1-production.up.railway.app        |                18
matrix-synapse-production.up.railway.app  |                 5
```

Bu durumda, `matrix-synapse-production.up.railway.app` domain'li kullanıcıları silmeniz gerekecek.


