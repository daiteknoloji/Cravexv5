# 🗑️ Veritabanını Tamamen Temizleme - Adım Adım

## ⚠️ UYARI
Bu işlem **TÜM KULLANICILARI VE MESAJLARI SİLECEK!** Geri alınamaz!

---

## 🎯 YÖNTEM 1: Railway Dashboard'dan (EN KOLAY)

### Adım 1: Railway Dashboard'a Git
1. Tarayıcıda https://railway.app aç
2. Giriş yap

### Adım 2: PostgreSQL Servisini Bul
1. Sol tarafta projenizi seç
2. **PostgreSQL** servisini bul ve tıkla

### Adım 3: Veritabanını Sil
1. Üst menüden **Data** sekmesine tıkla
2. **Delete Database** veya **Reset Database** butonunu bul
3. Tıkla ve onayla

**TAMAM! Veritabanı temizlendi!** ✅

---

## 🎯 YÖNTEM 2: Railway CLI ile (Terminal'den)

### Adım 1: Railway CLI'yi Yükle
```bash
npm i -g @railway/cli
```

### Adım 2: Railway'e Bağlan
```bash
railway login
```

### Adım 3: Projeyi Seç
```bash
railway link
```
Projenizi seçin (ok tuşları ile)

### Adım 4: Veritabanını Temizle
```bash
railway run --service postgres psql -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
```

**TAMAM! Veritabanı temizlendi!** ✅

---

## 🔄 Sonraki Adımlar

Veritabanı temizlendikten sonra:

1. **Railway'de `SYNAPSE_SERVER_NAME` ayarla:**
   - Synapse servisi → Variables → `SYNAPSE_SERVER_NAME=cravex1-production.up.railway.app`

2. **Synapse otomatik başlayacak** (veritabanı temiz olduğu için)

3. **Yeni admin kullanıcı oluştur:**
   ```bash
   railway run --service synapse register_new_matrix_user -c /tmp/homeserver.yaml -a -u admin -p GÜÇLÜ_ŞİFRE
   ```

---

## ✅ Kontrol

Synapse başladı mı kontrol et:
- Railway dashboard → Synapse servisi → Logs
- Şunu görmelisin: `📍 Server: cravex1-production.up.railway.app`


