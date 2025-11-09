# 🚀 RAILWAY'DE KULLANICI OLUŞTURMA - HIZLI REHBER

## ❌ Sorun
Login sayfasında "yanlış kullanıcı adı şifre" hatası alıyorsunuz.

**Sebep:** Railway'de henüz kullanıcı oluşturulmamış.

---

## ✅ ÇÖZÜM: PowerShell Script ile

### Adım 1: Script'i Çalıştırın

PowerShell'de şu komutu çalıştırın:

```powershell
cd "C:\Users\Can Cakir\Desktop\www-backup"
.\create-railway-admin.ps1
```

### Adım 2: Beklenen Çıktı

Script başarılı olursa:
```
========================================
  SUCCESS! ADMIN USER CREATED!
========================================

LOGIN CREDENTIALS:

  Element Web (Chat):
  URL: https://cozy-dragon-54547b.netlify.app/#/login
  Username: admin
  Password: Admin@2024!Guclu
```

---

## 🔧 ALTERNATİF: Railway Dashboard'dan

### Adım 1: Railway Dashboard'a Gidin
1. https://railway.app/dashboard
2. Synapse servisini seçin

### Adım 2: Terminal Açın
1. Synapse servisi → **Deployments** → **View Logs**
2. Veya **Settings** → **Shell**

### Adım 3: Kullanıcı Oluşturun
```bash
register_new_matrix_user -c /data/homeserver.yaml -a -u admin
```

Şifre sorulduğunda: `Admin@2024!Guclu` girin

---

## 🎯 SONRAKI ADIM: LOGIN

Kullanıcı oluşturulduktan sonra:

1. **Login sayfasına gidin:**
   ```
   https://cozy-dragon-54547b.netlify.app/#/login
   ```

2. **Giriş bilgileri:**
   - Username: `admin`
   - Password: `Admin@2024!Guclu`
   - Homeserver: Otomatik yüklenecek

3. **Sign In** butonuna tıklayın

---

## 🆘 SORUN GİDERME

### Script "Could not get nonce" hatası veriyorsa:
- Railway'de Synapse çalışıyor mu kontrol edin
- `https://matrix-synapse.up.railway.app/_matrix/client/versions` adresini test edin

### Script "Invalid MAC" hatası veriyorsa:
- `homeserver.yaml`'daki `registration_shared_secret` değerini kontrol edin
- Script'teki `$sharedSecret` değeri ile eşleşmeli

### Hala "yanlış kullanıcı adı şifre" hatası alıyorsanız:
- Kullanıcı oluşturuldu mu kontrol edin
- Railway Dashboard → Synapse → Logs → Kullanıcı oluşturma mesajlarını kontrol edin

---

**ÖNEMLİ:** Script'i çalıştırdıktan sonra 1-2 dakika bekleyin, sonra login deneyin!


