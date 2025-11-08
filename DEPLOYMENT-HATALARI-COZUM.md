# 🚨 DEPLOYMENT HATALARI VE ÇÖZÜMLERİ

**Tarih:** 8 Kasım 2025  
**Durum:** İki kritik deployment hatası tespit edildi

---

## ❌ SORUN 1: NETLIFY BUILD HATASI

### Hata:
```
error Your lockfile needs to be updated, but yarn was run with `--frozen-lockfile`.
```

### Neden:
- Netlify build sırasında `yarn install --frozen-lockfile` çalıştırılıyor
- `yarn.lock` dosyası güncel değil (package.json ile uyumsuz)
- `--frozen-lockfile` flag'i lockfile'ın değişmemesini garanti eder, bu yüzden hata veriyor

### Çözüm:

#### Adım 1: Yarn Lock Dosyasını Güncelle
```powershell
cd www\element-web
yarn install
```

Bu komut `yarn.lock` dosyasını güncelleyecek.

#### Adım 2: Değişiklikleri Commit ve Push Et
```powershell
git add www/element-web/yarn.lock
git commit -m "fix: Update yarn.lock for Netlify build"
git push
```

#### Alternatif Çözüm: Netlify Build Command Değiştir
Eğer lockfile güncellemesi sorun çıkarırsa, Netlify build command'ını değiştirebilirsiniz:

**Netlify Dashboard → Site Settings → Build & Deploy → Build Command:**
```
cd www/element-web && yarn install && yarn build
```

`--frozen-lockfile` flag'ini kaldırın.

---

## ❌ SORUN 2: RAILWAY SYNAPSE SERVER_NAME HATASI

### Hata:
```
Exception: Found users in database not native to cravex1-production.up.railway.app!
You cannot change a synapse server_name after it's been configured
```

### Neden:
- Veritabanında `matrix-synapse-production.up.railway.app` server name'i ile kayıtlı kullanıcılar var
- Config dosyasında `cravex1-production.up.railway.app` kullanılıyor
- Synapse server_name bir kez ayarlandıktan sonra değiştirilemez
- `start.sh` script'i server name'i değiştirmeye çalışıyor ama veritabanı uyumsuz

### Log Analizi:
```
📍 Server: matrix-synapse-production.up.railway.app  ← Log'da görünen
📍 Server: cravex1-production.up.railway.app           ← Config'de olan
```

### Çözüm:

#### Seçenek 1: Railway Environment Variable'ı Düzelt (ÖNERİLEN)

Railway Dashboard'da Synapse servisinin environment variables'ını kontrol edin:

1. **Railway Dashboard → Synapse Service → Variables**
2. `SYNAPSE_SERVER_NAME` değerini kontrol edin
3. Eğer `cravex1-production.up.railway.app` ise, **`matrix-synapse-production.up.railway.app`** olarak değiştirin
4. Redeploy yapın

**Neden:** Veritabanında zaten `matrix-synapse-production.up.railway.app` ile kayıtlı kullanıcılar var, bu yüzden server name'i bu olarak tutmak gerekiyor.

#### Seçenek 2: Config Dosyasını Güncelle

Eğer Railway environment variable'ı değiştiremiyorsanız, config dosyasını güncelleyin:

**Dosya:** `synapse-railway-config/homeserver.yaml`

```yaml
server_name: "matrix-synapse-production.up.railway.app"
public_baseurl: "https://matrix-synapse-production.up.railway.app/"
```

**Dosya:** `synapse-railway-config/start.sh`

`start.sh` dosyasında zaten doğru server name'e çevirme var, ama başlangıç değeri yanlış olabilir. Kontrol edin:

```bash
# Line 29-30: Bu satırlar doğru çalışıyor mu?
sed -i "s|server_name: \"matrix-synapse-production.up.railway.app\"|server_name: \"$SYNAPSE_SERVER_NAME\"|g" $DATA_DIR/homeserver.yaml
```

#### Seçenek 3: Veritabanını Sıfırla (⚠️ VERİ KAYBI)

Eğer veritabanındaki veriler önemli değilse:

1. Railway Dashboard → PostgreSQL Service → Delete
2. Yeni PostgreSQL servisi oluştur
3. Synapse'i yeniden deploy et
4. Yeni server name ile başlayacak

**⚠️ UYARI:** Bu işlem tüm kullanıcıları, odaları ve mesajları siler!

---

## 📋 KONTROL LİSTESİ

### Netlify Build:
- [ ] `www/element-web/yarn.lock` dosyasını güncelle (`yarn install`)
- [ ] Değişiklikleri commit ve push et
- [ ] Netlify build loglarını kontrol et
- [ ] Build başarılı olursa deploy'u test et

### Railway Synapse:
- [ ] Railway Dashboard'da `SYNAPSE_SERVER_NAME` environment variable'ını kontrol et
- [ ] Değer `matrix-synapse-production.up.railway.app` olmalı
- [ ] Eğer farklıysa, `matrix-synapse-production.up.railway.app` olarak güncelle
- [ ] Synapse servisini redeploy et
- [ ] Logları kontrol et - server name hatası gitmeli
- [ ] Synapse başarıyla başlamalı

---

## 🔍 DOĞRULAMA

### Netlify Build Başarılı:
```bash
# Netlify Dashboard'da build loglarını kontrol et
# "Build successful" mesajını görmeli
```

### Railway Synapse Başarılı:
```bash
# Railway Dashboard'da Synapse loglarını kontrol et
# Şu hatayı görmemeli:
# "Exception: Found users in database not native to..."
# "You cannot change a synapse server_name..."

# Bunun yerine şunu görmeli:
# "Server hostname: matrix-synapse-production.up.railway.app"
# "Setting up server" → başarılı başlatma
```

---

## 📝 NOTLAR

1. **Server Name Değiştirilemez:** Synapse server_name bir kez ayarlandıktan sonra değiştirilemez. Bu Matrix protokolünün bir gereksinimidir.

2. **Yarn Lockfile:** Netlify production build'lerde `--frozen-lockfile` kullanır çünkü reproducible build'ler için önemlidir. Lockfile'ı her zaman güncel tutmak gerekiyor.

3. **Environment Variables:** Railway environment variables'ı config dosyalarından önceliklidir. Her zaman Railway Dashboard'dan kontrol edin.

---

**Son Güncelleme:** 8 Kasım 2025  
**Durum:** ⚠️ İki kritik hata tespit edildi, çözümler hazırlandı

