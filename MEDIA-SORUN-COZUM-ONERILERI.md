# Media Sorunu Çözüm Önerileri

## 🔍 Sorun Analizi

Loglardan görülen durum:
- ✅ Token bulunuyor: `syt_Y2FuLmNha2ly_VNR...`
- ✅ Client API v3 deneniyor
- ❌ Tüm endpoint'ler 404 döndürüyor: `{"errcode":"M_NOT_FOUND","error":"Not found"}`

## 🎯 Olası Nedenler

### 1. Media Dosyaları Matrix Synapse'ta Yok
- Media dosyaları silinmiş olabilir
- Media dosyaları farklı bir storage'da (S3, local disk) ve erişilemiyor
- Media dosyaları başka bir Matrix server'da (federasyon)

### 2. Matrix Synapse Media Server Çalışmıyor
- Media server servisi çalışmıyor olabilir
- Media server farklı bir URL'de çalışıyor olabilir
- Railway deployment'ında media server ayrı bir servis olabilir

### 3. Element Web Farklı Bir Yöntem Kullanıyor
- Element Web cache'den gösteriyor olabilir
- Element Web farklı bir Matrix server'a bağlanıyor olabilir
- Element Web media'ya farklı bir endpoint'ten erişiyor olabilir

## 💡 Çözüm Önerileri

### Çözüm 1: Element Web'in Kullandığı URL'yi Kontrol Et

Element Web'in network tab'ını açın ve bir resim yüklerken hangi URL'yi kullandığını kontrol edin:

1. Browser Developer Tools'u açın (F12)
2. Network tab'ına gidin
3. Element Web'de bir resim gösterin
4. Network tab'ında media request'ini bulun
5. Hangi URL kullanılıyor kontrol edin

Muhtemelen şu formatlardan biri:
- `https://matrix-synapse.up.railway.app/_matrix/client/v3/download/matrix-synapse.up.railway.app/{media_id}`
- `https://matrix-synapse.up.railway.app/_matrix/media/v1/download/{media_id}?allow_redirect=true`
- Başka bir Matrix server URL'i

### Çözüm 2: Matrix Synapse Media Server'ı Kontrol Et

Railway'de Matrix Synapse servisinin loglarını kontrol edin:

1. Railway Dashboard'a gidin
2. Matrix Synapse servisini bulun
3. Logs'u açın
4. Media request'leri için hata mesajları var mı kontrol edin

### Çözüm 3: Media Dosyalarının Varlığını Kontrol Et

Database'de media referanslarını kontrol edin:

```sql
-- Media ID'nin hangi event'lerde kullanıldığını bul
SELECT 
    e.event_id,
    e.sender,
    e.room_id,
    e.type,
    to_timestamp(e.origin_server_ts/1000) as timestamp,
    (ej.json::jsonb)->'content'->>'url' as mxc_url
FROM events e
JOIN event_json ej ON e.event_id = ej.event_id
WHERE (ej.json::jsonb)->'content'->>'url' LIKE '%MqnlVpJGrlhqFyWcITBVhcvH%'
ORDER BY e.origin_server_ts DESC
LIMIT 5;
```

### Çözüm 4: Element Web'in Base URL'ini Kullan

Element Web'in kullandığı base URL'i environment variable olarak ekleyin:

```python
# Element Web'in kullandığı base URL
ELEMENT_BASE_URL = os.getenv('ELEMENT_BASE_URL', 'https://matrix-synapse.up.railway.app')

# Media URL formatı
media_url = f'{ELEMENT_BASE_URL}/_matrix/client/v3/download/{server_name}/{media_id}'
```

### Çözüm 5: Media Dosyalarını Element Web'den Proxy Et

Eğer Element Web'de görünüyorsa, Element Web'in kullandığı URL'yi direkt kullanabiliriz:

```python
# Element Web'in media URL formatını kullan
element_media_url = f'{synapse_url}/_matrix/client/v3/download/{server_name}/{media_id}?allow_redirect=true'
```

## 🔧 Hızlı Test

Element Web'de bir resim açın ve browser console'da şunu çalıştırın:

```javascript
// Element Web'in media URL formatını bul
const mediaUrl = 'mxc://matrix-synapse.up.railway.app/MqnlVpJGrlhqFyWcITBVhcvH';
const client = window.mxMatrixClient;
const httpUrl = client.mxcUrlToHttp(mediaUrl);
console.log('Element Web Media URL:', httpUrl);
```

Bu URL'yi admin panel'de kullanabiliriz.

## 📊 Sonraki Adımlar

1. Element Web'in network tab'ını kontrol edin
2. Hangi URL formatını kullandığını bulun
3. O URL formatını admin panel'de kullanın

Eğer Element Web farklı bir URL kullanıyorsa, o URL'yi paylaşın ve admin panel'i ona göre güncelleyelim.

