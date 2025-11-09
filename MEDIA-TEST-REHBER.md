# Media Test Rehberi

## 🧪 Test Adımları

### 1. Admin Panelde Resim Açmayı Deneyin

1. **Admin panele gidin**: `https://considerate-adaptation-production.up.railway.app/`
2. **Mesajlar** sekmesine gidin
3. **Bir resim içeren mesajı** açın
4. **Resmin görünüp görünmediğini** kontrol edin

---

### 2. Railway Loglarına Bakın

Eğer resim hala görünmüyorsa:

1. **Railway Dashboard**'a gidin
2. **Admin Panel** servisini seçin
3. **Logs** sekmesine gidin
4. **Şu log mesajlarını arayın**:
   - `[DEBUG] Trying Matrix Media API v3`
   - `[DEBUG] Media API v3 response:`
   - `[DEBUG] ✅ Matrix Media API v3 worked!` (başarılı ise)
   - `[DEBUG] Media API v3 failed:` (başarısız ise)

**Örnek başarılı log:**
```
[DEBUG] Trying Matrix Media API v3 (Element Web format): https://matrix-synapse.up.railway.app/_matrix/media/v3/download/matrix-synapse.up.railway.app/JpPmAvKDuaZnUmOQyVaWRCGk?allow_redirect=true
[DEBUG] Media API v3 response: 200
[DEBUG] ✅ Matrix Media API v3 worked!
```

**Örnek başarısız log:**
```
[DEBUG] Trying Matrix Media API v3 (Element Web format): https://matrix-synapse.up.railway.app/_matrix/media/v3/download/matrix-synapse.up.railway.app/JpPmAvKDuaZnUmOQyVaWRCGk?allow_redirect=true
[DEBUG] Media API v3 response: 404
[DEBUG] Media API v3 response text: {"errcode":"M_NOT_FOUND","error":"Not found"}
```

---

### 3. Logları Bana Gönderin

Eğer resim hala görünmüyorsa, Railway loglarından şu bilgileri kopyalayıp bana gönderin:

1. **Media API v3 denemesi** ile ilgili tüm log satırları
2. **Hata mesajları** (varsa)
3. **Response status code**'ları
4. **Response text** (varsa)

---

### 4. Element Web Network Sekmesine Bakın (İleri Seviye)

Eğer hala çalışmazsa, Element Web'in nasıl eriştiğini görmek için:

1. **Element Web'de bir resim açın**
2. **F12** tuşuna basın (Developer Tools)
3. **Network** sekmesine gidin
4. **Filter** kısmına `download` yazın
5. **Resmi yeniden açın** (sayfayı yenileyin)
6. **Listede görünen request'e tıklayın**
7. **Headers** sekmesine gidin
8. **Request Headers** bölümündeki **Authorization** header'ını kontrol edin

**Örnek Authorization header:**
```
Authorization: Bearer syt_Y2FuLmNha2ly_VNR...
```

Bu token'ı bana gönderin (tam token'ı değil, sadece formatını).

---

## ✅ Başarılı Olursa

Eğer resim görünmeye başladıysa:
- ✅ **Sorun çözüldü!**
- Loglarda `✅ Matrix Media API v3 worked!` mesajını göreceksiniz

---

## ❌ Hala Çalışmıyorsa

Eğer resim hala görünmüyorsa:
1. **Railway loglarını** bana gönderin
2. **Element Web Network** bilgilerini paylaşın (yukarıdaki adım 4)
3. **Hangi resim ID'sini** denediğinizi söyleyin (örnek: `JpPmAvKDuaZnUmOQyVaWRCGk`)

---

## 🔍 Debug Bilgileri

Admin panelde resim yüklenemediğinde, browser console'da (F12 → Console) şu bilgileri görebilirsiniz:

```javascript
Resim yüklenemedi
URL: /api/media/download/matrix-synapse.up.railway.app/JpPmAvKDuaZnUmOQyVaWRCGk
```

Bu bilgiyi de bana gönderebilirsiniz.

