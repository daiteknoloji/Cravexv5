# Media Cache Veritabanı Tasarımı

## 🎯 Amaç
Media dosyalarını kendi veritabanımızda saklayarak:
- Matrix Synapse'a bağımlılığı azaltmak
- Daha hızlı erişim sağlamak (cache)
- Offline erişim mümkün kılmak

---

## 📊 Veritabanı Şeması

### `media_cache` Tablosu

```sql
CREATE TABLE IF NOT EXISTS media_cache (
    id SERIAL PRIMARY KEY,
    media_id VARCHAR(255) NOT NULL UNIQUE,
    server_name VARCHAR(255) NOT NULL,
    mxc_url TEXT NOT NULL,
    media_data BYTEA NOT NULL,
    content_type VARCHAR(255),
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    sender_user_id VARCHAR(255),
    event_id VARCHAR(255),
    INDEX idx_media_id (media_id),
    INDEX idx_server_name (server_name),
    INDEX idx_last_accessed (last_accessed)
);
```

### Alternatif: Base64 Encoding (Daha Az Verimli)

Eğer BYTEA yerine TEXT kullanmak isterseniz:

```sql
CREATE TABLE IF NOT EXISTS media_cache (
    id SERIAL PRIMARY KEY,
    media_id VARCHAR(255) NOT NULL UNIQUE,
    server_name VARCHAR(255) NOT NULL,
    mxc_url TEXT NOT NULL,
    media_data_base64 TEXT NOT NULL,  -- Base64 encoded
    content_type VARCHAR(255),
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    sender_user_id VARCHAR(255),
    event_id VARCHAR(255),
    INDEX idx_media_id (media_id),
    INDEX idx_server_name (server_name),
    INDEX idx_last_accessed (last_accessed)
);
```

---

## 🔧 Python Implementation

### 1. Tablo Oluşturma Fonksiyonu

```python
def init_media_cache_table():
    """Media cache tablosunu oluştur"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_cache (
                id SERIAL PRIMARY KEY,
                media_id VARCHAR(255) NOT NULL UNIQUE,
                server_name VARCHAR(255) NOT NULL,
                mxc_url TEXT NOT NULL,
                media_data BYTEA NOT NULL,
                content_type VARCHAR(255),
                file_size BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                sender_user_id VARCHAR(255),
                event_id VARCHAR(255)
            )
        """)
        
        # Index'leri oluştur
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_media_cache_media_id 
            ON media_cache(media_id)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_media_cache_server_name 
            ON media_cache(server_name)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_media_cache_last_accessed 
            ON media_cache(last_accessed)
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("[INFO] Media cache table initialized")
    except Exception as e:
        print(f"[ERROR] Failed to create media_cache table: {e}")
```

### 2. Media Cache'e Kaydetme Fonksiyonu

```python
def save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type=None, sender_user_id=None, event_id=None):
    """Media dosyasını cache'e kaydet"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        file_size = len(media_data) if isinstance(media_data, bytes) else len(media_data.encode())
        
        cur.execute("""
            INSERT INTO media_cache 
            (media_id, server_name, mxc_url, media_data, content_type, file_size, sender_user_id, event_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (media_id) 
            DO UPDATE SET
                media_data = EXCLUDED.media_data,
                content_type = EXCLUDED.content_type,
                file_size = EXCLUDED.file_size,
                last_accessed = CURRENT_TIMESTAMP,
                access_count = media_cache.access_count + 1
        """, (media_id, server_name, mxc_url, media_data, content_type, file_size, sender_user_id, event_id))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"[INFO] Media cached: {media_id} ({file_size} bytes)")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to cache media: {e}")
        return False
```

### 3. Media Cache'den Okuma Fonksiyonu

```python
def get_media_from_cache(media_id):
    """Media dosyasını cache'den oku"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT media_data, content_type, file_size, sender_user_id, event_id
            FROM media_cache
            WHERE media_id = %s
        """, (media_id,))
        
        row = cur.fetchone()
        
        if row:
            # Access count ve last_accessed güncelle
            cur.execute("""
                UPDATE media_cache
                SET access_count = access_count + 1,
                    last_accessed = CURRENT_TIMESTAMP
                WHERE media_id = %s
            """, (media_id,))
            conn.commit()
            
            cur.close()
            conn.close()
            
            return {
                'media_data': row[0],  # BYTEA
                'content_type': row[1],
                'file_size': row[2],
                'sender_user_id': row[3],
                'event_id': row[4],
                'cached': True
            }
        
        cur.close()
        conn.close()
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get media from cache: {e}")
        return None
```

### 4. Güncellenmiş Proxy Endpoint

```python
@app.route('/api/media/download/<server_name>/<path:media_id>')
@login_required
def proxy_media_download(server_name, media_id):
    """Proxy media download requests - önce cache'den kontrol et"""
    try:
        # 1. Önce cache'den kontrol et
        cached_media = get_media_from_cache(media_id)
        if cached_media:
            print(f"[INFO] Media served from cache: {media_id}")
            return Response(
                cached_media['media_data'],
                mimetype=cached_media['content_type'] or 'application/octet-stream',
                headers={
                    'Content-Disposition': f'inline; filename="{media_id}"',
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*',
                    'X-Cache': 'HIT'
                }
            )
        
        # 2. Cache'de yoksa Matrix Synapse'tan çek
        print(f"[INFO] Media not in cache, fetching from Matrix: {media_id}")
        synapse_url = os.getenv('SYNAPSE_URL', f'https://{server_name}')
        media_url = f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}'
        
        # ... (mevcut Matrix Synapse'tan çekme kodu)
        
        response = requests.get(media_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
        
        if response.status_code == 200:
            # Media data'yı memory'de topla
            media_data = response.content
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            # 3. Cache'e kaydet
            mxc_url = f'mxc://{server_name}/{media_id}'
            save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type)
            
            # 4. Kullanıcıya gönder
            return Response(
                media_data,
                mimetype=content_type,
                headers={
                    'Content-Disposition': f'inline; filename="{media_id}"',
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*',
                    'X-Cache': 'MISS'
                }
            )
        else:
            # ... (hata handling)
            
    except Exception as e:
        # ... (hata handling)
```

---

## ⚠️ Önemli Notlar

### Avantajlar:
- ✅ Matrix Synapse'a bağımlılık azalır
- ✅ Daha hızlı erişim (cache hit)
- ✅ Offline erişim mümkün
- ✅ Media dosyaları kontrol altında

### Dezavantajlar:
- ❌ Veritabanı boyutu çok artar (büyük dosyalar için)
- ❌ Disk kullanımı artar
- ❌ Backup/restore süreleri uzar
- ❌ Performans sorunları olabilir (çok büyük dosyalar için)

### Öneriler:
1. **Dosya boyutu limiti**: Sadece küçük dosyaları cache'le (örn: < 10MB)
2. **TTL (Time To Live)**: Eski dosyaları otomatik sil
3. **LRU Cache**: En az kullanılan dosyaları sil
4. **Hybrid Approach**: Küçük dosyalar DB'de, büyük dosyalar S3'te

---

## 🔄 Cache Temizleme Stratejileri

### 1. TTL Bazlı Temizleme

```python
def cleanup_old_media_cache(days=30):
    """30 günden eski media cache'leri temizle"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            DELETE FROM media_cache
            WHERE last_accessed < CURRENT_TIMESTAMP - INTERVAL '%s days'
        """, (days,))
        
        deleted_count = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"[INFO] Cleaned up {deleted_count} old media cache entries")
        return deleted_count
    except Exception as e:
        print(f"[ERROR] Failed to cleanup media cache: {e}")
        return 0
```

### 2. Boyut Bazlı Temizleme

```python
def cleanup_large_media_cache(max_size_mb=100):
    """Toplam cache boyutu max_size_mb'ı geçerse en eski dosyaları sil"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Toplam cache boyutunu kontrol et
        cur.execute("""
            SELECT SUM(file_size) / (1024 * 1024) as total_size_mb
            FROM media_cache
        """)
        
        total_size = cur.fetchone()[0] or 0
        
        if total_size > max_size_mb:
            # En eski dosyaları sil
            cur.execute("""
                DELETE FROM media_cache
                WHERE id IN (
                    SELECT id FROM media_cache
                    ORDER BY last_accessed ASC
                    LIMIT (SELECT COUNT(*) FROM media_cache) / 2
                )
            """)
            
            deleted_count = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            
            print(f"[INFO] Cleaned up {deleted_count} media cache entries (total was {total_size:.2f} MB)")
            return deleted_count
        
        cur.close()
        conn.close()
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to cleanup media cache: {e}")
        return 0
```

---

## 📈 İstatistikler

```python
def get_media_cache_stats():
    """Media cache istatistiklerini getir"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                COUNT(*) as total_files,
                SUM(file_size) / (1024 * 1024) as total_size_mb,
                AVG(file_size) / 1024 as avg_size_kb,
                MAX(file_size) / (1024 * 1024) as max_size_mb,
                SUM(access_count) as total_accesses,
                AVG(access_count) as avg_accesses
            FROM media_cache
        """)
        
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        return {
            'total_files': row[0] or 0,
            'total_size_mb': round(row[1] or 0, 2),
            'avg_size_kb': round(row[2] or 0, 2),
            'max_size_mb': round(row[3] or 0, 2),
            'total_accesses': row[4] or 0,
            'avg_accesses': round(row[5] or 0, 2)
        }
    except Exception as e:
        print(f"[ERROR] Failed to get media cache stats: {e}")
        return None
```

---

## 🚀 Kullanım Senaryosu

1. **İlk İstek**: Matrix Synapse'tan çek → Cache'e kaydet → Kullanıcıya gönder
2. **Sonraki İstekler**: Cache'den oku → Kullanıcıya gönder (çok daha hızlı)
3. **Periyodik Temizleme**: Eski/kullanılmayan dosyaları sil

---

## 💡 Alternatif: Hybrid Approach

Küçük dosyalar DB'de, büyük dosyalar S3'te:

```python
MAX_CACHE_SIZE_MB = 5  # 5MB'dan küçük dosyalar DB'de

if file_size < MAX_CACHE_SIZE_MB * 1024 * 1024:
    # Küçük dosya → DB'de sakla
    save_media_to_cache(...)
else:
    # Büyük dosya → S3'e kaydet (veya sadece Matrix'te bırak)
    save_to_s3(...)
```

