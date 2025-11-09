# Synapse Durum Kontrolü ve Şema Oluşturma

## 🔍 Sorun

`relation "users" does not exist` hatası, Synapse'in veritabanı şemasını henüz oluşturmadığını gösteriyor.

## ✅ Kontrol Adımları

### 1. Synapse Loglarını Kontrol Et

Railway Dashboard → **Cravexv5** → **"Logs"** sekmesinden Synapse loglarını kontrol edin.

**Başarılı şema oluşturma logları şöyle görünür:**
```
✅ Preparing database...
✅ Creating database schema...
✅ Database schema created successfully
✅ Starting server...
✅ Server started successfully
```

**Eğer hata varsa:**
```
❌ Error creating database schema
❌ Exception: ...
❌ Found users in database not native to...
```

### 2. Synapse Servisinin Durumunu Kontrol Et

- Railway Dashboard → **Cravexv5** → **"Metrics"** sekmesi
- Veya **"Logs"** sekmesinde sürekli log geliyorsa çalışıyordur

## 🛠️ Çözüm

### Senaryo 1: Synapse Henüz Başlamadı

Eğer loglar boşsa veya Synapse henüz başlamadıysa:

1. **Railway Dashboard** → **Cravexv5**
2. **"Deployments"** → **"Redeploy"**
3. Logları izleyin - şema oluşturma işlemini göreceksiniz

### Senaryo 2: Synapse Crash Oluyor

Eğer Synapse crash oluyorsa, logları paylaşın. Muhtemelen:
- Database bağlantı sorunu
- Configuration sorunu
- Server name sorunu (hala devam ediyor olabilir)

### Senaryo 3: Şema Oluşturma İşlemi Devam Ediyor

Synapse ilk başlangıçta şema oluşturma işlemi yapar ve bu **1-2 dakika** sürebilir. Bu süre içinde:
- ✅ Logları izleyin
- ✅ "Creating database schema..." mesajını bekleyin
- ✅ İşlem tamamlanana kadar bekleyin

## ⏱️ Bekleme Süresi

Synapse ilk başlangıçta:
1. Database bağlantısını kontrol eder
2. Şema versiyonunu kontrol eder
3. Şema yoksa oluşturur (1-2 dakika)
4. Server'ı başlatır

**Toplam süre: 2-3 dakika olabilir**

## 🚨 Hala Sorun Varsa

Eğer Synapse şemayı oluşturamıyorsa:

1. **Logları kontrol edin** ve paylaşın
2. **Database bağlantısını kontrol edin:**
   - Railway Dashboard → PostgreSQL → "Settings" → Environment Variables
   - `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT` doğru mu?

3. **Synapse konfigürasyonunu kontrol edin:**
   - Railway Dashboard → Cravexv5 → "Settings" → Environment Variables
   - `SYNAPSE_SERVER_NAME` doğru mu? (`cravex1-production.up.railway.app`)

## 📋 Şema Oluşturma Sonrası

Şema oluşturulduktan sonra:
- ✅ `users` tablosu oluşacak
- ✅ Admin panelden kullanıcı kaydedebilirsiniz
- ✅ Tüm Synapse tabloları hazır olacak

## 💡 Önemli Not

**Admin panelden kullanıcı kaydetmeye çalışmadan önce:**
- Synapse'in tamamen başlamış olması gerekiyor
- Şema oluşturma işleminin tamamlanmış olması gerekiyor
- Loglarda "Server started successfully" mesajını görmelisiniz


