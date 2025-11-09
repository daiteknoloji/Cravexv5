# Veritabanı Kontrol Adımları

## 🔍 Railway'de Veritabanını Kontrol Etme

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesine gidin.

## 📊 Adım 1: Hangi Domain'ler Var?

Aşağıdaki sorguyu çalıştırın ve sonucu paylaşın:

```sql
SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as kullanici_sayisi
FROM users
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
```

**Bu sorgu size şunu gösterecek:**
- `cravex1-production.up.railway.app` → X kullanıcı
- `matrix-synapse-production.up.railway.app` → Y kullanıcı
- vb.

## 📋 Adım 2: Tüm Kullanıcıları Listele

Eğer hangi kullanıcıların hangi domain'de olduğunu görmek istiyorsanız:

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 1) as kullanici_adi,
    split_part(name, ':', 2) as domain
FROM users
ORDER BY domain, name;
```

## 🎯 Beklenen Sonuç

Eğer Synapse crash oluyorsa, muhtemelen şunu göreceksiniz:

```
domain                                    | kullanici_sayisi
------------------------------------------|------------------
cravex1-production.up.railway.app        | 18
```

Ama Synapse şimdi `matrix-synapse-production.up.railway.app` olarak çalışmaya çalışıyor, bu yüzden crash oluyor.

## ✅ Çözüm

Eğer `cravex1-production.up.railway.app` domain'inde kullanıcılar varsa:

1. **Seçenek 1:** Veritabanını tamamen temizle (tüm kullanıcıları sil)
2. **Seçenek 2:** Synapse'i `cravex1-production.up.railway.app` olarak çalıştır (ama bu V1.0.0'a uygun değil)

## 📝 Sonuçları Paylaşın

Lütfen **Adım 1** sorgusunun sonucunu paylaşın, böylece hangi domain'lerin olduğunu görebilirim ve doğru çözümü önerebilirim.


