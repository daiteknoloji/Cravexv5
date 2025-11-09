# 🚨 Railway Synapse Hızlı Çözüm

## Sorun
Synapse başlamıyor çünkü:
1. Railway'de `SYNAPSE_SERVER_NAME` environment variable'ı `matrix-synapse-production.up.railway.app` olarak ayarlı
2. Veritabanında başka bir domain'de kullanıcılar var
3. Synapse `server_name` değiştirilemez hatası veriyor

## ✅ Çözüm (2 Adım)

### Adım 1: Railway'de Environment Variable'ı Güncelle

1. Railway dashboard'a git: https://railway.app
2. Synapse servisinizi seçin
3. **Variables** sekmesine tıklayın
4. `SYNAPSE_SERVER_NAME` variable'ını bulun veya yeni oluşturun
5. Değerini şu şekilde ayarlayın:
   ```
   SYNAPSE_SERVER_NAME=cravex1-production.up.railway.app
   ```
6. **Save** butonuna tıklayın (servis otomatik redeploy olacak)

### Adım 2: Veritabanını Temizle

#### Seçenek A: Railway Dashboard'dan (Kolay)

1. Railway dashboard → PostgreSQL servisinizi seçin
2. **Data** sekmesine gidin
3. **Delete Database** veya **Reset Database** butonuna tıklayın
4. Onaylayın

#### Seçenek B: Railway CLI ile (Gelişmiş)

```bash
# Railway CLI'yi yükle (eğer yoksa)
npm i -g @railway/cli

# Railway'e login ol
railway login

# Projeyi seç
railway link

# PostgreSQL'e bağlan
railway connect postgres

# PostgreSQL shell'de şu komutları çalıştır:
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
\q
```

#### Seçenek C: Railway CLI ile Tek Komut

```bash
railway run --service postgres psql -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
```

### Adım 3: Synapse Servisini Yeniden Başlat

1. Railway dashboard → Synapse servisinizi seçin
2. **Deployments** sekmesine gidin
3. **Redeploy** butonuna tıklayın

## ✅ Kontrol

Synapse başladıktan sonra logları kontrol edin:

```bash
# Railway dashboard'dan logları görüntüleyin
# Veya Railway CLI ile:
railway logs --service synapse
```

Başarılı log örneği:
```
📍 Server: cravex1-production.up.railway.app
Server hostname: cravex1-production.up.railway.app
```

## 🔄 İlk Admin Kullanıcıyı Oluştur

Veritabanı temizlendikten sonra yeni admin kullanıcı oluşturun:

```bash
# Railway CLI ile Synapse container'ına bağlan
railway run --service synapse bash

# İçeride admin kullanıcı oluştur
register_new_matrix_user -c /tmp/homeserver.yaml -a -u admin -p GÜÇLÜ_ŞİFRE
```

## ⚠️ ÖNEMLİ NOTLAR

1. **Veritabanı temizlendikten sonra TÜM kullanıcılar ve mesajlar silinecek!**
2. `SYNAPSE_SERVER_NAME` environment variable'ı `homeserver.yaml`'daki `server_name`'i override eder
3. Railway'de environment variable ayarlandıktan sonra servis otomatik redeploy olur
4. Veritabanı temizlendikten sonra Synapse yeni domain ile başlayacak

## 🐛 Sorun Devam Ederse

1. Railway dashboard → Synapse servisi → **Variables** → `SYNAPSE_SERVER_NAME` değerini kontrol edin
2. Railway dashboard → Synapse servisi → **Logs** → Hata mesajlarını kontrol edin
3. Railway dashboard → PostgreSQL servisi → **Data** → Veritabanının temizlendiğini kontrol edin


