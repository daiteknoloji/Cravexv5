# 🔐 LOGIN BİLGİLERİ - Element Web

## 🌐 Netlify Login Sayfası

**URL:** `https://cozy-dragon-54547b.netlify.app/#/login`

---

## 📝 GİRİŞ BİLGİLERİ

### Eğer Admin Kullanıcısı Varsa:

**Username:** `admin`  
**Password:** `Admin@2024!Guclu`  
**Homeserver:** Otomatik yüklenecek (`matrix-synapse.up.railway.app`)

---

### Eğer Admin Kullanıcısı Yoksa:

Railway'de yeni bir kullanıcı oluşturmanız gerekiyor.

#### Yöntem 1: Railway Dashboard'dan (ÖNERİLEN)

1. Railway Dashboard → Synapse servisi → **Logs**
2. Railway CLI ile kullanıcı oluşturun:

```bash
# Railway CLI ile bağlan
railway connect

# Kullanıcı oluştur
railway run register_new_matrix_user -c /data/homeserver.yaml -a -u admin
```

Şifre sorulduğunda: `Admin@2024!Guclu` girin

---

#### Yöntem 2: PowerShell Script ile

`create-railway-admin.ps1` script'ini çalıştırın:

```powershell
.\create-railway-admin.ps1
```

---

## 🆕 YENİ KULLANICI OLUŞTURMA

### Railway'de Admin Kullanıcı Oluşturma:

1. **Railway Dashboard'a gidin:**
   - https://railway.app/dashboard
   - Synapse servisini seçin

2. **Terminal'i açın:**
   - Synapse servisi → **Deployments** → **View Logs**
   - Veya **Settings** → **Shell**

3. **Kullanıcı oluşturun:**
   ```bash
   register_new_matrix_user -c /data/homeserver.yaml -a -u admin
   ```
   
   Şifre sorulduğunda: `Admin@2024!Guclu` girin

---

## ✅ TEST ETME

Login sayfasında:
1. **Username:** `admin` girin
2. **Password:** `Admin@2024!Guclu` girin
3. **Homeserver:** Otomatik yüklenecek (`matrix-synapse.up.railway.app`)
4. **Sign In** butonuna tıklayın

---

## 🆘 SORUN GİDERME

### "Invalid username or password" hatası:
- Kullanıcı Railway'de oluşturulmamış olabilir
- Yukarıdaki adımları takip ederek kullanıcı oluşturun

### "Cannot connect to server" hatası:
- Railway'de Synapse çalışıyor mu kontrol edin
- `https://matrix-synapse.up.railway.app/_matrix/client/versions` adresini test edin

---

**Not:** Railway'de kullanıcı oluşturmak için Railway Dashboard veya CLI kullanmanız gerekiyor.


