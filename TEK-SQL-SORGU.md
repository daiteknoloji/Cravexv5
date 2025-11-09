# Tek SQL Sorgusu - Tüm Kullanıcılar ve Domain'leri

Railway PostgreSQL'de çalıştırın:

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY domain, name;
```

## 📋 Bu sorgu size şunu gösterecek:
- **kullanici_id**: Tam kullanıcı ID'si (örn: `@kullanici:domain.com`)
- **kullanici_adi**: Kullanıcı adı (örn: `kullanici`)
- **domain**: Domain adı (örn: `domain.com`)

## 🚀 Railway'de Çalıştırma:

### Yöntem 1: Railway Dashboard
1. Railway Dashboard → PostgreSQL servisinizi seçin
2. "Data" sekmesi → "Query" butonuna tıklayın
3. Yukarıdaki SQL sorgusunu yapıştırın
4. "Run Query" ile çalıştırın

### Yöntem 2: Railway CLI
```bash
railway run --service <postgres-service-name> psql -c "SELECT name as kullanici_id, split_part(name, ':', 1) as kullanici_adi, split_part(name, ':', 2) as domain FROM users ORDER BY domain, name;"
```

## 💡 Örnek Çıktı:

```
kullanici_id                    | kullanici_adi | domain
--------------------------------+---------------+----------------------------------
@user1:cravex1-production...   | user1         | cravex1-production.up.railway.app
@user2:cravex1-production...   | user2         | cravex1-production.up.railway.app
@admin:matrix-synapse-prod...  | admin         | matrix-synapse-production.up.railway.app
```

Bu çıktıyı paylaşın, hangi domain'lerde sorun olduğunu görelim!


