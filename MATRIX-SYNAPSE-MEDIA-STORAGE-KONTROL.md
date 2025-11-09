# Matrix Synapse Media Storage Kontrol Rehberi

## 🎯 Amaç
Matrix Synapse'de media dosyalarının gerçekten var olup olmadığını kontrol etmek.

---

## 📋 YÖNTEM 1: Railway Dashboard'dan Kontrol (Kolay)

### Adım 1: Railway Dashboard'a Gidin
1. **Railway Dashboard**'u açın: https://railway.app
2. **Projenizi** seçin
3. **Matrix Synapse** servisini bulun

### Adım 2: Volumes/Storage Kontrolü
1. Matrix Synapse servisine tıklayın
2. **"Settings"** sekmesine gidin
3. **"Volumes"** veya **"Storage"** bölümünü bulun
4. Media dosyalarının nerede saklandığını görün

**Not:** Railway'de media dosyaları genellikle bir volume'da saklanır.

---

## 📋 YÖNTEM 2: Railway Terminal'den Kontrol (İleri Seviye)

### Adım 1: Railway Terminal'i Açın
1. Railway Dashboard'da Matrix Synapse servisine gidin
2. **"Deployments"** sekmesine gidin
3. **"View Logs"** veya **"Open Terminal"** butonuna tıklayın

### Adım 2: Media Storage Klasörünü Bulun
Matrix Synapse'de media dosyaları genellikle şu klasörde saklanır:
```
/var/synapse/media_store/
```

VEYA Railway'de:
```
/data/media_store/
```

### Adım 3: Media Dosyasını Kontrol Edin
Terminal'de şu komutları çalıştırın:

```bash
# Media storage klasörüne git
cd /var/synapse/media_store/

# VEYA Railway'de
cd /data/media_store/

# Media ID'sine göre dosyayı bul
# Media ID: HQtoyORnVrJmhoFLGhWQZZQD
# Dosya genellikle şu formatta saklanır: {media_id[0]}/{media_id[1]}/{media_id}
# Örnek: H/Q/HQtoyORnVrJmhoFLGhWQZZQD

# Dosyayı ara
find . -name "*HQtoyORnVrJmhoFLGhWQZZQD*"

# VEYA klasör yapısına göre kontrol et
ls -la H/Q/ 2>/dev/null || echo "Klasör bulunamadı"

# Dosya varsa bilgilerini göster
ls -lh H/Q/HQtoyORnVrJmhoFLGhWQZZQD 2>/dev/null || echo "Dosya bulunamadı"
```

---

## 📋 YÖNTEM 3: SQL ile Media Referanslarını Kontrol Et

### Adım 1: Database Client'ı Açın
1. Railway Dashboard'da **PostgreSQL** servisine gidin
2. **"Connect"** veya **"Query"** butonuna tıklayın
3. Database client'ı açın

### Adım 2: Media Referanslarını Kontrol Edin

**Media ID ile event'i bul:**
```sql
SELECT 
    e.event_id,
    e.sender,
    e.room_id,
    e.origin_server_ts,
    ej.json::json->'content'->>'url' as mxc_url,
    ej.json::json->'content'->'info'->>'size' as file_size
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json::json->'content'->>'url' LIKE '%HQtoyORnVrJmhoFLGhWQZZQD%';
```

**Tüm media referanslarını listele:**
```sql
SELECT 
    COUNT(*) as total_media_messages,
    COUNT(DISTINCT ej.json::json->'content'->>'url') as unique_media_urls
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE e.type = 'm.room.message'
  AND ej.json::json->'content'->>'url' IS NOT NULL
  AND ej.json::json->'content'->>'url' LIKE 'mxc://%';
```

**Belirli bir media ID'nin kaç mesajda kullanıldığını bul:**
```sql
SELECT 
    ej.json::json->'content'->>'url' as mxc_url,
    COUNT(*) as usage_count
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json::json->'content'->>'url' LIKE '%HQtoyORnVrJmhoFLGhWQZZQD%'
GROUP BY ej.json::json->'content'->>'url';
```

---

## 📋 YÖNTEM 4: Matrix Synapse Loglarını Kontrol Et

### Adım 1: Railway Loglarını Açın
1. Railway Dashboard'da Matrix Synapse servisine gidin
2. **"Logs"** sekmesine gidin

### Adım 2: Media İle İlgili Logları Arayın
Loglarda şu mesajları arayın:
- `Media file not found`
- `Media ID: HQtoyORnVrJmhoFLGhWQZZQD`
- `404` veya `M_NOT_FOUND`

**Örnek log mesajları:**
```
[WARN] Media file not found: HQtoyORnVrJmhoFLGhWQZZQD
[ERROR] 404: Media not found
```

---

## 🔍 Media Dosyası Neden Bulunamıyor?

### Olası Nedenler:

1. **Media dosyası silinmiş**
   - Matrix Synapse'den silinmiş olabilir
   - Storage temizliği yapılmış olabilir

2. **Media dosyası başka sunucuda**
   - Federasyon ile başka bir Matrix sunucusunda olabilir
   - MXC URL'deki `server_name` farklı olabilir

3. **Media dosyası henüz yüklenmemiş**
   - Upload işlemi tamamlanmamış olabilir
   - Event var ama dosya yok

4. **Storage path yanlış**
   - Matrix Synapse'in media storage path'i farklı olabilir
   - Railway'de volume mount edilmemiş olabilir

---

## ✅ Kontrol Listesi

- [ ] SQL'de event var mı? (Media referansı var mı?)
- [ ] Media storage klasöründe dosya var mı?
- [ ] Matrix Synapse loglarında hata var mı?
- [ ] MXC URL'deki server_name doğru mu?
- [ ] Railway volume mount edilmiş mi?

---

## 📝 Notlar

- **Media dosyası yoksa**, Element Web cache'den gösteriyor olabilir
- **Media dosyası başka sunucudaysa**, federasyon URL'i kullanılmalı
- **Media dosyası silinmişse**, admin panelde görünmemesi normaldir

---

## 🎯 Sonuç

Eğer:
- ✅ **SQL'de event var** ama **storage'da dosya yok** → Dosya silinmiş
- ✅ **SQL'de event var** ve **storage'da dosya var** → URL formatı yanlış olabilir
- ❌ **SQL'de event yok** → Mesaj silinmiş veya hiç gönderilmemiş

Bu bilgileri bana gönderin, çözümü birlikte bulalım! 🚀

