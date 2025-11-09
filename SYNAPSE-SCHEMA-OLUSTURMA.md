# Synapse Şema Oluşturma Sorunu

## 🔍 Sorun

`relation "users" does not exist` hatası, Synapse'in veritabanı şemasını henüz oluşturmadığını gösteriyor.

## 🔎 Kontrol Adımları

### 1. Synapse Loglarını Kontrol Et

Railway Dashboard → Cravexv5 → "Logs" sekmesinden Synapse loglarını kontrol edin.

**Başarılı şema oluşturma logları şöyle görünür:**
```
✅ Preparing database...
✅ Creating database schema...
✅ Database schema created successfully
✅ Starting server...
```

**Hata varsa şöyle görünür:**
```
❌ Error creating database schema
❌ Exception: ...
```

### 2. Synapse Durumunu Kontrol Et

Synapse servisinin çalışıp çalışmadığını kontrol edin:
- Railway Dashboard → Cravexv5 → "Metrics" sekmesi
- Veya "Logs" sekmesinde sürekli log geliyorsa çalışıyordur

## 🛠️ Çözüm: Şemayı Manuel Oluştur

Eğer Synapse şemayı otomatik oluşturmadıysa, manuel olarak oluşturabilirsiniz:

### Yöntem 1: Synapse'i Yeniden Başlat (Önerilen)

1. Railway Dashboard → Cravexv5
2. "Deployments" → "Redeploy"
3. Logları izleyin - şema oluşturma işlemini göreceksiniz

### Yöntem 2: Synapse CLI ile Şema Oluştur

Railway'de Synapse servisine bağlanıp şemayı manuel oluşturun:

```bash
railway run --service cravexv5 python3 -m synapse.app.homeserver --config-path /tmp/homeserver.yaml --generate-config
```

Ama bu genellikle gerekmez, Synapse otomatik oluşturur.

## 💡 En Olası Neden

Synapse henüz tam başlamadı veya crash oldu. Logları kontrol edin:

1. **Eğer Synapse crash oluyorsa:** Logları paylaşın, hatayı çözelim
2. **Eğer Synapse başlıyorsa:** Şema oluşturma işleminin tamamlanmasını bekleyin (1-2 dakika)

## ⏱️ Bekleme Süresi

Synapse ilk başlangıçta şema oluşturma işlemi yapar ve bu **1-2 dakika** sürebilir. Bu süre içinde:
- ✅ Logları izleyin
- ✅ "Creating database schema..." mesajını bekleyin
- ✅ İşlem tamamlanana kadar bekleyin

## 🚨 Hala Sorun Varsa

Eğer Synapse şemayı oluşturamıyorsa, logları paylaşın. Muhtemelen:
- Database bağlantı sorunu
- Permission sorunu
- Configuration sorunu

olabilir.


