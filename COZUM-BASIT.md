# 🎯 Basit Çözüm - Sadece Sorun Çıkartan Kullanıcıları Sil

## Sorun
Synapse crash oluyor çünkü veritabanında farklı domain'de kullanıcılar var.

## ✅ ÇÖZÜM (2 Seçenek)

### SEÇENEK 1: Railway'de Domain'i Değiştir (ÖNERİLEN)

Loglardan görüldüğü üzere Synapse `matrix-synapse-production.up.railway.app` ile başlamaya çalışıyor ama veritabanında başka domain'de kullanıcılar var.

**Yapılacaklar:**
1. Railway dashboard → Synapse servisi → **Variables**
2. `SYNAPSE_SERVER_NAME` değerini kontrol et
3. Eğer `cravex1-production.up.railway.app` ise → `matrix-synapse-production.up.railway.app` yap
4. Eğer `matrix-synapse-production.up.railway.app` ise → `cravex1-production.up.railway.app` yap
5. **Save** → Servis otomatik redeploy olacak

**Bu şekilde Synapse veritabanındaki kullanıcılarla uyumlu domain ile başlayacak!**

---

### SEÇENEK 2: Sadece Sorunlu Domain'deki Kullanıcıları Sil

Eğer domain değiştirmek istemiyorsan, sadece sorun çıkartan domain'deki kullanıcıları sil:

#### Railway Dashboard'dan:

1. Railway dashboard → PostgreSQL servisi → **Data** sekmesi
2. **Query** veya **SQL Editor** bul
3. Şu SQL'i çalıştır (eğer `matrix-synapse-production` domain'indeki kullanıcıları silmek istiyorsan):

```sql
DELETE FROM users WHERE name LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM user_ips WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM user_filters WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM user_directory WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM profiles WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM access_tokens WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
DELETE FROM devices WHERE user_id LIKE '%:matrix-synapse-production.up.railway.app';
```

VEYA eğer `cravex1-production` domain'indeki kullanıcıları silmek istiyorsan:

```sql
DELETE FROM users WHERE name LIKE '%:cravex1-production.up.railway.app';
DELETE FROM user_ips WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM user_filters WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM user_directory WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM profiles WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM access_tokens WHERE user_id LIKE '%:cravex1-production.up.railway.app';
DELETE FROM devices WHERE user_id LIKE '%:cravex1-production.up.railway.app';
```

---

## 🔍 Önce Kontrol Et

Railway dashboard → PostgreSQL → **Data** → **Query** sekmesinde şunu çalıştır:

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi 
FROM users 
GROUP BY split_part(name, ':', 2);
```

Bu komut hangi domain'de kaç kullanıcı olduğunu gösterir.

**Sonra:**
- Eğer `matrix-synapse-production.up.railway.app` domain'inde kullanıcılar varsa → Railway'de `SYNAPSE_SERVER_NAME`'i `matrix-synapse-production.up.railway.app` yap
- Eğer `cravex1-production.up.railway.app` domain'inde kullanıcılar varsa → Railway'de `SYNAPSE_SERVER_NAME`'i `cravex1-production.up.railway.app` yap

---

## 💡 EN KOLAY YOL

Loglardan görüldüğü üzere Synapse `matrix-synapse-production.up.railway.app` ile başlamaya çalışıyor ama veritabanında başka domain'de kullanıcılar var.

**Çözüm:** Railway'de `SYNAPSE_SERVER_NAME`'i veritabanındaki kullanıcıların domain'ine göre ayarla!

1. Railway dashboard → PostgreSQL → Data → Query
2. `SELECT DISTINCT split_part(name, ':', 2) as domain FROM users;` çalıştır
3. Hangi domain çıkıyorsa → Railway'de `SYNAPSE_SERVER_NAME`'i o domain yap
4. Synapse otomatik başlayacak!


