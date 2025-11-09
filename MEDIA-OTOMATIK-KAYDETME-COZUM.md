# Medya Otomatik Kaydetme Çözümü

## 🎯 Amaç

Tüm medya içeriklerini (resim, ses, video, dosya, emoji, anket, vb.) mesajlar gibi veritabanında saklamak. Böylece:
- ✅ Matrix Synapse'den silinse bile admin panel'de görüntülenebilir
- ✅ Cache'den bağımsız çalışır
- ✅ Tüm medya içerikleri kalıcı olarak saklanır

## 📋 Mevcut Durum

1. ✅ `media_cache` tablosu var
2. ❌ Sadece 5MB'dan küçük dosyalar cache'leniyor
3. ❌ Mesajları okurken medya dosyaları otomatik indirilmiyor
4. ❌ Sadece proxy endpoint'lerinden medya istenince cache'e kaydediliyor

## ✅ Çözüm: Otomatik Medya Kaydetme

### 1. Cache Limitini Kaldır/Artır

Şu anda `save_media_to_cache` fonksiyonu sadece 5MB'dan küçük dosyaları cache'liyor. Bunu kaldıralım veya artıralım.

### 2. Mesajları Okurken Otomatik Medya İndirme

`get_messages` ve `get_room_messages` fonksiyonlarında:
- Medya içeriği varsa kontrol et
- Cache'de yoksa Matrix Synapse'den indir
- Cache'e kaydet

### 3. Yeni Fonksiyon: `auto_cache_media_from_message`

```python
def auto_cache_media_from_message(media_url, sender, event_id, msgtype=None):
    """
    Mesajdan medya URL'sini alıp otomatik olarak cache'e kaydet
    
    Args:
        media_url: MXC URL (mxc://server.com/media_id)
        sender: Gönderen kullanıcı ID'si
        event_id: Event ID
        msgtype: Mesaj tipi (m.image, m.file, m.audio, m.video, vb.)
    
    Returns:
        bool: Başarılı ise True
    """
    # 1. MXC URL'yi parse et
    # 2. Cache'de var mı kontrol et
    # 3. Yoksa Matrix Synapse'den indir
    # 4. Cache'e kaydet
```

## 🔧 Uygulama Adımları

### ADIM 1: Cache Limitini Kaldır

`save_media_to_cache` fonksiyonundaki `MAX_CACHE_SIZE_MB = 5` limitini kaldır veya çok yüksek bir değer yap (örn: 100MB).

### ADIM 2: Otomatik Medya İndirme Fonksiyonu Ekle

Mesajları okurken medya içeriklerini otomatik olarak indirip cache'e kaydet.

### ADIM 3: Mesaj Okuma Fonksiyonlarını Güncelle

`get_messages` ve `get_room_messages` fonksiyonlarında medya içeriği varsa `auto_cache_media_from_message` fonksiyonunu çağır.

### ADIM 4: Background Job (Opsiyonel)

Eski mesajlar için background job ekle:
- Tüm mesajları tarayın
- Medya içeriği olanları bulun
- Cache'de yoksa indirip kaydedin

## 📊 Veritabanı Yapısı

Mevcut `media_cache` tablosu yeterli:

```sql
CREATE TABLE media_cache (
    id SERIAL PRIMARY KEY,
    media_id VARCHAR(255) NOT NULL UNIQUE,
    server_name VARCHAR(255) NOT NULL,
    mxc_url TEXT NOT NULL,
    media_data BYTEA NOT NULL,  -- Binary data
    content_type VARCHAR(255),
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    sender_user_id VARCHAR(255),
    event_id VARCHAR(255)
);
```

## 🎯 Avantajlar

1. ✅ **Kalıcı Saklama**: Medya dosyaları Matrix Synapse'den silinse bile admin panel'de görüntülenebilir
2. ✅ **Cache Bağımsız**: Tarayıcı cache'inden bağımsız çalışır
3. ✅ **Tüm Medya Tipleri**: Resim, ses, video, dosya, emoji, anket - hepsi saklanır
4. ✅ **Otomatik**: Mesajları okurken otomatik olarak medya dosyaları indirilir

## ⚠️ Dikkat Edilmesi Gerekenler

1. **Disk Alanı**: Tüm medya dosyaları veritabanında saklanacak, disk alanı kontrol edilmeli
2. **Performans**: Büyük dosyalar veritabanını yavaşlatabilir
3. **Backup**: Veritabanı backup'ları büyük olacak

## 🔄 Alternatif Çözümler

### Seçenek 1: Sadece Küçük Dosyaları Sakla
- 5MB'dan küçük dosyaları sakla
- Büyük dosyalar için Matrix Synapse'e bağımlı kal

### Seçenek 2: Ayrı Storage
- Medya dosyalarını PostgreSQL yerine ayrı bir storage'da sakla (S3, local filesystem, vb.)
- Veritabanında sadece referans tut

### Seçenek 3: Hybrid Yaklaşım
- Küçük dosyaları veritabanında sakla
- Büyük dosyaları ayrı storage'da sakla

## 📝 Sonraki Adımlar

1. ✅ Cache limitini kaldır/artır
2. ✅ Otomatik medya indirme fonksiyonunu ekle
3. ✅ Mesaj okuma fonksiyonlarını güncelle
4. ✅ Test et
5. ✅ Background job ekle (opsiyonel)

