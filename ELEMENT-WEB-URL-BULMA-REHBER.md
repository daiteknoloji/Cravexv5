# Element Web URL Bulma Rehberi - Adım Adım

## 🎯 Amaç
Element Web'in media dosyalarına erişmek için kullandığı gerçek URL formatını bulmak.

---

## 📋 ADIM 1: Element Web'de Resmi Açın

1. **Element Web'i açın** (örnek: `https://app.element.io` veya kendi Matrix sunucunuz)
2. **Bir sohbete gidin** (resim içeren bir mesaj olan)
3. **Resim içeren mesajı bulun**
4. **Resme tıklayın** (büyük resim açılacak)

---

## 📋 ADIM 2: Browser Developer Tools'u Açın

### Windows/Linux:
- **F12** tuşuna basın
- VEYA
- **Sağ tık** → **"İncele"** veya **"Inspect"**

### Mac:
- **Cmd + Option + I** tuşlarına basın
- VEYA
- **Sağ tık** → **"İncele"** veya **"Inspect"**

---

## 📋 ADIM 3: Network Sekmesine Geçin

1. Developer Tools açıldığında, **üstteki sekmelere** bakın:
   - Elements
   - Console
   - **Network** ← Buna tıklayın
   - Sources
   - vb.

2. **Network sekmesi** açılacak (boş olabilir, normal)

---

## 📋 ADIM 4: Filter Ekleyin

1. Network sekmesinin **üst kısmında** bir **"Filter"** kutusu var
2. Bu kutuya şunu yazın: **`download`**
3. VEYA şunu yazın: **`media`**

Bu, sadece media ile ilgili request'leri gösterecek.

---

## 📋 ADIM 5: Resmi Yeniden Açın

1. **Sayfayı yenileyin** (F5 veya Ctrl+R)
2. VEYA **resme tekrar tıklayın**
3. Network sekmesinde **yeni request'ler** görünecek

---

## 📋 ADIM 6: Request'i Bulun

1. Network sekmesindeki **liste**de şunlardan birini arayın:
   - `download`
   - `media`
   - `mxc`
   - Resim dosyası adı (örnek: `.png`, `.jpg`)

2. **Request'e tıklayın** (mavi renkte olacak)

---

## 📋 ADIM 7: URL'yi Kopyalayın

1. Request'e tıkladığınızda, **sağ tarafta** detaylar açılacak
2. **"Headers"** sekmesine tıklayın (varsayılan olarak açık olabilir)
3. **"Request URL"** veya **"General"** bölümünde URL'yi bulun
4. **URL'yi seçin** ve **Ctrl+C** ile kopyalayın

**Örnek URL formatları:**
```
https://matrix-synapse.up.railway.app/_matrix/media/v3/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD?allow_redirect=true
```

VEYA

```
https://matrix-synapse.up.railway.app/_matrix/client/v3/download/matrix-synapse.up.railway.app/HQtoyORnVrJmhoFLGhWQZZQD
```

---

## 📋 ADIM 8: URL'yi Bana Gönderin

Kopyaladığınız URL'yi bana gönderin. Ben admin panel'i o URL formatına göre güncelleyeceğim.

---

## 🖼️ Görsel Rehber

### Network Sekmesi Görünümü:
```
┌─────────────────────────────────────────────────┐
│ [Filter: download] [XHR] [JS] [CSS] [Img] ... │
├─────────────────────────────────────────────────┤
│ Name                    Status  Type    Size   │
├─────────────────────────────────────────────────┤
│ download/.../media_id   200     image   27KB   │ ← Buna tıkla
│ thumbnail/.../media_id   200     image   5KB   │
└─────────────────────────────────────────────────┘
```

### Request Detayları:
```
┌─────────────────────────────────────────────────┐
│ Headers | Preview | Response | Timing          │
├─────────────────────────────────────────────────┤
│ Request URL:                                    │
│ https://matrix-synapse.../download/.../media_id│ ← Bunu kopyala
│                                                 │
│ Request Headers:                                │
│ Authorization: Bearer syt_...                  │
│ ...                                             │
└─────────────────────────────────────────────────┘
```

---

## 🔍 Alternatif Yöntem: Resme Sağ Tıklama

Eğer Network sekmesi karmaşık geliyorsa:

1. **Element Web'de resme sağ tıklayın**
2. **"Resmi yeni sekmede aç"** veya **"Resim adresini kopyala"** seçeneğini seçin
3. Yeni sekmede açılırsa, **adres çubuğundaki URL'yi** kopyalayın
4. VEYA **"Resim adresini kopyala"** ile direkt kopyalayın

---

## ❓ Sorun Giderme

### Network sekmesinde hiçbir şey görünmüyor:
- **Sayfayı yenileyin** (F5)
- **Filter'ı temizleyin** ve tekrar yazın
- **Resme tekrar tıklayın**

### Request bulamıyorum:
- Filter'ı **boş bırakın** ve tüm request'leri görün
- **"Img"** sekmesine tıklayın (sadece resimleri gösterir)
- **"All"** sekmesine tıklayın (tüm request'leri gösterir)

### URL kopyalayamıyorum:
- **Sağ tık** → **"Copy"** → **"Copy URL"**
- VEYA URL'yi **manuel olarak** seçip kopyalayın

---

## 📝 Notlar

- **Element Web cache kullanıyor olabilir** - Eğer resim hemen yükleniyorsa, cache'den gösteriyor olabilir
- **Sayfayı yenileyin** - Cache'i bypass etmek için Ctrl+Shift+R (hard refresh)
- **Farklı resimler deneyin** - Her resim farklı URL formatı kullanıyor olabilir

---

## ✅ Başarı Kriteri

URL'yi bulduğunuzda şunları göreceksiniz:
- ✅ URL `https://` ile başlıyor
- ✅ URL'de `matrix-synapse` veya sunucu adınız var
- ✅ URL'de `download` veya `media` kelimesi var
- ✅ URL'de media ID var (örnek: `HQtoyORnVrJmhoFLGhWQZZQD`)

Bu URL'yi bana gönderin! 🎯

