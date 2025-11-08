# 🔧 RAILWAY SYNAPSE SERVER_NAME DÜZELTME REHBERİ

**Sorun:** Synapse server_name hatası - veritabanı ile config uyumsuzluğu

---

## ❌ HATA

```
Exception: Found users in database not native to cravex1-production.up.railway.app!
You cannot change a synapse server_name after it's been configured
```

**Log'da görünen:** `matrix-synapse-production.up.railway.app`  
**Config'de olan:** `cravex1-production.up.railway.app`

---

## 🔍 SORUN ANALİZİ

1. Veritabanında `matrix-synapse-production.up.railway.app` server name'i ile kayıtlı kullanıcılar var
2. Config dosyasında `cravex1-production.up.railway.app` kullanılıyor
3. Synapse server_name bir kez ayarlandıktan sonra değiştirilemez
4. Railway environment variable'ı yanlış ayarlanmış olabilir

---

## ✅ ÇÖZÜM ADIMLARI

### Adım 1: Railway Environment Variable Kontrolü

1. **Railway Dashboard'a git:** https://railway.app
2. **Synapse servisini seç**
3. **Variables sekmesine git**
4. **`SYNAPSE_SERVER_NAME` değerini kontrol et**

**Beklenen Değer:** `matrix-synapse-production.up.railway.app`

### Adım 2: Environment Variable'ı Düzelt

Eğer `SYNAPSE_SERVER_NAME` değeri `cravex1-production.up.railway.app` ise:

1. **Değeri sil**
2. **Yeni değer ekle:** `matrix-synapse-production.up.railway.app`
3. **Kaydet**

### Adım 3: Synapse Servisini Redeploy Et

1. **Railway Dashboard → Synapse Service**
2. **Deployments sekmesi**
3. **"Redeploy" butonuna tıkla**
4. **Logları izle**

### Adım 4: Logları Kontrol Et

Başarılı başlatma logları:

```
✅ Configuration complete!
📍 Server: matrix-synapse-production.up.railway.app
🗄️  Database: postgres.railway.internal:5432

🚀 Starting Synapse...
Server hostname: matrix-synapse-production.up.railway.app
Setting up server
```

**Hata görmemeli:**
- ❌ `Exception: Found users in database not native to...`
- ❌ `You cannot change a synapse server_name...`

---

## 🔄 ALTERNATİF ÇÖZÜM: Config Dosyasını Güncelle

Eğer Railway environment variable'ı değiştiremiyorsanız:

### Dosya: `synapse-railway-config/homeserver.yaml`

```yaml
server_name: "matrix-synapse-production.up.railway.app"
public_baseurl: "https://matrix-synapse-production.up.railway.app/"
```

### Dosya: `synapse-railway-config/start.sh`

`start.sh` dosyası zaten doğru çalışıyor, sadece environment variable'ın doğru olması gerekiyor.

---

## ⚠️ ÖNEMLİ NOTLAR

1. **Server Name Değiştirilemez:** Synapse server_name bir kez ayarlandıktan sonra değiştirilemez. Bu Matrix protokolünün bir gereksinimidir.

2. **Veritabanı Uyumluluğu:** Server name veritabanındaki kullanıcı kayıtları ile bağlantılıdır. Değiştirmek için veritabanını sıfırlamak gerekir (veri kaybı olur).

3. **Environment Variable Önceliği:** Railway environment variables config dosyalarından önceliklidir. Her zaman Railway Dashboard'dan kontrol edin.

---

## 📋 KONTROL LİSTESİ

- [ ] Railway Dashboard'da `SYNAPSE_SERVER_NAME` değerini kontrol ettim
- [ ] Değer `matrix-synapse-production.up.railway.app` olarak ayarlandı
- [ ] Synapse servisini redeploy ettim
- [ ] Logları kontrol ettim - hata yok
- [ ] Synapse başarıyla başladı

---

**Son Güncelleme:** 8 Kasım 2025  
**Durum:** ⚠️ Railway environment variable düzeltilmesi gerekiyor

