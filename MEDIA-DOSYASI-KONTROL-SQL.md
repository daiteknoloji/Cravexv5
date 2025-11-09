# Media Dosyası Kontrol SQL Sorguları

## ✅ Event Veritabanında Var

SQL sorgusu sonucu:
- **event_id**: `$xdSRW2B_sjOUNY7xHdqAW2tQrt2-1Wg_rmdVqqyZQc0`
- **sender**: `@can.cakir:matrix-synapse.up.railway.app`
- **mxc_url**: `mxc://matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD`

Bu, event'in veritabanında var olduğunu gösteriyor. ✅

---

## 🔍 Şimdi Kontrol Edilecekler

### 1. Media Dosyasının Storage'da Olup Olmadığı

Railway Terminal'de şu komutları çalıştırın:

```bash
# Matrix Synapse container'ına bağlan
# Railway Dashboard → Matrix Synapse → Terminal

# Media storage klasörüne git
cd /var/synapse/media_store/

# VEYA Railway'de farklı path olabilir
cd /data/media_store/

# Media ID'sine göre dosyayı bul
# Matrix Synapse media dosyalarını şu formatta saklar:
# {media_id[0]}/{media_id[1]}/{media_id}
# Örnek: H/Q/HQtoyORnVrJmhoFLGhWQZZQD

# Dosyayı ara
find . -name "*HQtoyORnVrJmhoFLGhWQZZQD*" -type f

# VEYA klasör yapısına göre kontrol et
ls -la H/Q/HQtoyORnVrJmhoFLGhWQZZQD 2>/dev/null || echo "Dosya bulunamadı"

# Dosya varsa bilgilerini göster
ls -lh H/Q/HQtoyORnVrJmhoFLGhWQZZQD 2>/dev/null || echo "Dosya yok"
```

### 2. Media Dosyasının Boyutunu Kontrol Et

SQL ile media dosyasının bilgilerini kontrol edin:

```sql
SELECT 
    e.event_id,
    e.sender,
    e.origin_server_ts,
    ej.json::json->'content'->>'url' as mxc_url,
    ej.json::json->'content'->'info'->>'size' as file_size,
    ej.json::json->'content'->'info'->>'mimetype' as mimetype,
    ej.json::json->'content'->'info'->>'w' as image_width,
    ej.json::json->'content'->'info'->>'h' as image_height
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json::json->'content'->>'url' LIKE '%HQtoyORnVrJmhoFLGhWQZZQD%';
```

Bu sorgu:
- Dosya boyutunu gösterir
- MIME type'ı gösterir
- Resim boyutlarını gösterir (varsa)

### 3. Media Dosyasının Kullanımını Kontrol Et

Aynı media dosyasının kaç mesajda kullanıldığını kontrol edin:

```sql
SELECT 
    COUNT(*) as usage_count,
    STRING_AGG(e.event_id, ', ') as event_ids
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE ej.json::json->'content'->>'url' = 'mxc://matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD';
```

---

## 🎯 Sonuç Senaryoları

### Senaryo 1: Dosya Storage'da Var ✅
- **SQL'de event var** ✅
- **Storage'da dosya var** ✅
- **Sorun**: URL formatı yanlış veya authentication sorunu
- **Çözüm**: Element Web'in kullandığı URL formatını bul ve admin panel'i güncelle

### Senaryo 2: Dosya Storage'da Yok ❌
- **SQL'de event var** ✅
- **Storage'da dosya yok** ❌
- **Sorun**: Dosya silinmiş veya upload tamamlanmamış
- **Çözüm**: Element Web cache'den gösteriyor olabilir, admin panelde görünmemesi normal

### Senaryo 3: Dosya Başka Sunucuda 🌐
- **SQL'de event var** ✅
- **Storage'da dosya yok** ❌
- **MXC URL'de server_name farklı** 🌐
- **Sorun**: Federasyon ile başka sunucudan gelmiş
- **Çözüm**: Federasyon URL'i kullanılmalı

---

## 📝 Şimdi Yapılacaklar

1. **Railway Terminal'de dosyayı kontrol et** (yukarıdaki komutları çalıştır)
2. **SQL ile dosya bilgilerini kontrol et** (yukarıdaki sorguyu çalıştır)
3. **Element Web'in kullandığı URL'yi bul** (F12 → Network → download filtrele)
4. **Sonuçları bana gönder**

---

## 🔧 Debug Bilgileri

Admin panel loglarında şu bilgileri görebilirsiniz:

```
[DEBUG] Found sender for media HQtoyORnVrJmhoFLGhWQZZQD: @can.cakir:matrix-synapse.up.railway.app
[DEBUG] Found token for sender @can.cakir:matrix-synapse.up.railway.app: syt_...
[DEBUG] Trying Matrix Media API v3: https://matrix-synapse.up.railway.app/_matrix/media/v3/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD?allow_redirect=true
[DEBUG] Media API v3 response: 404
```

Bu, admin panel'in doğru media ID'sini kullandığını ama Matrix Synapse'den dosyayı bulamadığını gösteriyor.

---

## ✅ Kontrol Listesi

- [x] SQL'de event var mı? ✅ (Var: $xdSRW2B_sjOUNY7xHdqAW2tQrt2-1Wg_rmdVqqyZQc0)
- [ ] Media storage'da dosya var mı? (Railway Terminal'de kontrol et)
- [ ] Dosya boyutu nedir? (SQL ile kontrol et)
- [ ] Element Web'in kullandığı URL nedir? (F12 → Network'ten bul)
- [ ] Matrix Synapse loglarında hata var mı? (Railway Logs'tan kontrol et)

Sonuçları paylaşın, birlikte çözelim! 🚀

