# Veritabanı Şeması Yok - Çözüm

## 🔍 Sorun

SQL sorgusu çalıştırdığınızda şu hatayı alıyorsunuz:
```
SQL Error [42P01]: ERROR: relation "users" does not exist
```

Bu, veritabanı şemasının temizlendiği ve Synapse'in henüz şemayı yeniden oluşturmadığı anlamına gelir.

## ✅ Çözüm: Synapse'i Başlatın

Synapse başladığında veritabanı şemasını otomatik olarak oluşturur.

### Adımlar:

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Deploy"** veya servisi yeniden başlatın
3. **"Logs"** sekmesini açın ve şunları kontrol edin:

### Beklenen Log Mesajları:

✅ **Şema oluşturuluyor:**
```
['main', 'state']: Checking existing schema version
['main', 'state']: No existing schema found - creating new schema
```

✅ **Şema başarıyla oluşturuldu:**
```
['main', 'state']: Applying schema version 92
```

✅ **Synapse başladı:**
```
Server hostname: matrix-synapse-production.up.railway.app
Setting up server
```

### Şema Oluşturma Süresi:

- İlk başlatmada şema oluşturma işlemi **1-3 dakika** sürebilir
- Şema oluşturulduktan sonra `users` tablosu ve diğer tüm tablolar oluşturulacak

## 🔍 Şema Durumunu Kontrol Etme

Railway Dashboard → **Cravexv5** → **Postgres** servisi → **"Query"** sekmesinde:

```sql
-- Tüm tabloları listele
SELECT 
    table_schema,
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

Eğer sonuç boşsa veya sadece birkaç sistem tablosu varsa, Synapse henüz şemayı oluşturmamış demektir.

## ⚠️ Önemli Notlar

1. **Synapse Crash Oluyorsa:** Synapse crash olursa şemayı oluşturamaz. Önce crash sorununu çözmeniz gerekir.

2. **Veritabanı Temizlendiyse:** Veritabanını temizlediyseniz (`DROP SCHEMA public CASCADE`), Synapse'i yeniden başlatmanız gerekir.

3. **İlk Başlatma:** İlk başlatmada Synapse şemayı otomatik olarak oluşturur. Bu işlem biraz zaman alabilir.

## 🛠️ Şema Oluşturma İşlemini Manuel Başlatma

Eğer Synapse şemayı otomatik olarak oluşturmuyorsa:

1. Synapse'i durdurun
2. Veritabanını kontrol edin (şema boş olmalı)
3. Synapse'i yeniden başlatın
4. Logları izleyin - şema oluşturma mesajlarını görmelisiniz

## 📝 Sonraki Adımlar

Şema oluşturulduktan sonra:

1. `users` tablosu oluşturulacak
2. Kullanıcı sorgularınız çalışacak
3. Synapse normal şekilde çalışmaya başlayacak


