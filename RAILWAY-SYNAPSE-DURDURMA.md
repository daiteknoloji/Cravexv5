# Railway'de Synapse Servisini Durdurma

## 🛑 Synapse'i Durdurma Yöntemleri

### Yöntem 1: Railway Dashboard'dan Durdurma (EN KOLAY)

1. **Railway Dashboard** → https://railway.app/ adresine gidin
2. **Cravexv5** projesini seçin
3. **Synapse** servisini bulun ve tıklayın
4. **"Settings"** sekmesine gidin
5. **"Delete Service"** butonuna tıklayın (servisi silmez, sadece durdurur)
   - VEYA
   - **"Pause"** butonuna tıklayın (eğer varsa)

**Not:** Railway'de servisleri "pause" etme özelliği yoksa, servisi silip yeniden oluşturmanız gerekebilir. Ama genellikle servisi durdurmak için:

### Yöntem 2: Servisi Geçici Olarak Durdurma

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Settings"** sekmesi
3. **"Delete Service"** butonuna tıklayın
   - Bu servisi silmez, sadece durdurur
   - Veriler korunur
   - İstediğiniz zaman yeniden deploy edebilirsiniz

### Yöntem 3: Deploy'u Durdurma

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Deployments"** sekmesine gidin
3. Aktif deployment'ı bulun
4. **"Cancel"** veya **"Stop"** butonuna tıklayın

### Yöntem 4: Environment Variable ile Durdurma

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi → **"Variables"** sekmesi
2. Yeni bir environment variable ekleyin:
   ```
   SYNAPSE_DISABLED=true
   ```
3. Servis otomatik olarak yeniden başlayacak ve çalışmayacak

## ✅ Synapse Durumunu Kontrol Etme

### Logları Kontrol Edin

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi → **"Logs"** sekmesi
2. Eğer loglar durmuşsa veya "Service stopped" mesajı görüyorsanız, Synapse durmuş demektir

### Health Check

Synapse'in çalışıp çalışmadığını kontrol etmek için:

```bash
curl https://cravexv5-production.up.railway.app/_matrix/client/versions
```

Eğer hata alırsanız veya bağlantı kurulamazsa, Synapse durmuş demektir.

## 🔄 Synapse'i Yeniden Başlatma

### Yöntem 1: Railway Dashboard'dan

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Deploy"** butonuna tıklayın
3. Veya **"Redeploy"** butonuna tıklayın

### Yöntem 2: Git Push ile

Herhangi bir değişiklik yapıp push ederseniz, Railway otomatik olarak yeniden deploy eder:

```bash
git commit --allow-empty -m "Restart Synapse"
git push origin main
```

## ⚠️ ÖNEMLİ NOTLAR

1. **Veriler Korunur:** Synapse'i durdurmak verileri silmez, sadece servisi durdurur
2. **Database Bağlantısı:** Synapse durduğunda database bağlantıları kesilir
3. **Yeniden Başlatma:** Synapse'i yeniden başlattığınızda, veritabanı şeması korunur
4. **Kullanıcı Silme:** Kullanıcı silme işlemi sırasında Synapse durmuş olmalı

## 📝 Adım Adım: Kullanıcı Silme İçin Synapse'i Durdurma

1. **Railway Dashboard** → **Cravexv5** → **Synapse** servisi
2. **"Settings"** sekmesine gidin
3. **"Delete Service"** butonuna tıklayın (servisi silmez, sadece durdurur)
4. **Logları kontrol edin** - "Service stopped" mesajını görmelisiniz
5. **PostgreSQL Query sekmesine gidin** ve kullanıcı silme sorgularını çalıştırın
6. **Kullanıcı silme işlemi tamamlandıktan sonra**, Synapse'i yeniden başlatın:
   - **"Deploy"** butonuna tıklayın
   - VEYA Git push yapın

## 🚨 Sorun Giderme

### Synapse Durmuyorsa

1. **Logları kontrol edin** - Hala çalışıyor mu?
2. **Deployments sekmesine gidin** - Aktif deployment var mı?
3. **Settings sekmesine gidin** - Servis durumu nedir?

### Synapse Yeniden Başlamıyorsa

1. **Logları kontrol edin** - Hata mesajı var mı?
2. **Environment variables kontrol edin** - `SYNAPSE_DISABLED` var mı?
3. **Database bağlantısı kontrol edin** - PostgreSQL çalışıyor mu?


