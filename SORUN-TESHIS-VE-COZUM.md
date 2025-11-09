# Synapse Server Name Sorunu - Teşhis ve Çözüm

## 🔍 Sorun

Loglar şunu gösteriyor:
- ✅ `Server hostname: cravex1-production.up.railway.app` (Synapse doğru server_name'i okuyor)
- ❌ `Exception: Found users in database not native to cravex1-production.up.railway.app!`

Bu hata, veritabanında **`cravex1-production.up.railway.app` dışında başka bir domain'e kayıtlı kullanıcılar** olduğunu gösteriyor.

## 🔎 Teşhis Adımları

Railway'de şu komutu çalıştırın:

```bash
railway run --service cravexv5 bash -c "chmod +x /app/synapse-railway-config/diagnose-server-name.sh && /app/synapse-railway-config/diagnose-server-name.sh"
```

Veya PostgreSQL servisinde direkt:

```bash
railway run --service postgres psql -c "SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as user_count FROM users GROUP BY split_part(name, ':', 2) ORDER BY user_count DESC;"
```

## 💡 Muhtemel Senaryolar

### Senaryo 1: Veritabanında `matrix-synapse-production.up.railway.app` domain'li kullanıcılar var

Eğer sorgu sonucu şöyleyse:
```
matrix-synapse-production.up.railway.app  |  5
cravex1-production.up.railway.app         |  18
```

**Çözüm:** `matrix-synapse-production.up.railway.app` domain'li kullanıcıları silin:

```sql
-- Önce kontrol edin
SELECT name FROM users WHERE split_part(name, ':', 2) = 'matrix-synapse-production.up.railway.app';

-- Sonra silin (DİKKAT: Bu kullanıcılar kalıcı olarak silinecek!)
DELETE FROM users WHERE split_part(name, ':', 2) = 'matrix-synapse-production.up.railway.app';
```

### Senaryo 2: Veritabanında başka bir domain var

Eğer sorgu sonucu başka bir domain gösteriyorsa, o domain'li kullanıcıları silmeniz gerekiyor.

## 🛠️ Hızlı Çözüm

Eğer sadece `cravex1-production.up.railway.app` domain'li kullanıcıları tutmak istiyorsanız:

```sql
-- Tüm domain'leri göster
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as user_count 
FROM users 
GROUP BY split_part(name, ':', 2) 
ORDER BY user_count DESC;

-- cravex1-production.up.railway.app dışındaki tüm kullanıcıları sil
DELETE FROM users 
WHERE split_part(name, ':', 2) != 'cravex1-production.up.railway.app';
```

**⚠️ DİKKAT:** Bu komut `cravex1-production.up.railway.app` dışındaki **TÜM** kullanıcıları siler!

## 📋 Adım Adım Çözüm

1. **Teşhis:** Railway'de domain'leri kontrol edin
2. **Karar:** Hangi domain'li kullanıcıları tutmak istediğinize karar verin
3. **Temizlik:** İstenmeyen domain'li kullanıcıları silin
4. **Yeniden Başlat:** Synapse servisini yeniden başlatın

## ✅ Doğrulama

Kullanıcıları sildikten sonra, Synapse'in başarıyla başladığını kontrol edin:

```bash
railway logs --service cravexv5
```

Başarılı başlangıçta şunu görmelisiniz:
```
Server hostname: cravex1-production.up.railway.app
...
Starting server...
```


