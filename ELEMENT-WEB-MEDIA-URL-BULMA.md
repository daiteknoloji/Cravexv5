# Element Web Media URL Bulma Rehberi

## 🔍 Element Web'in Kullandığı Media URL'yi Bulma

### Yöntem 1: Browser Developer Tools (Network Tab)

1. **Element Web'i açın** ve bir resim gösterin
2. **F12** tuşuna basın (Developer Tools'u açın)
3. **Network** sekmesine gidin
4. **Filter** kısmına `media` veya `download` yazın
5. Resmi gösterdiğinizde network tab'ında bir request görünecek
6. Bu request'e tıklayın ve **Headers** sekmesine gidin
7. **Request URL** kısmındaki URL'yi kopyalayın

Örnek URL formatları:
- `https://matrix-synapse.up.railway.app/_matrix/client/v3/download/matrix-synapse.up.railway.app/MqnlVpJGrlhqFyWcITBVhcvH`
- `https://matrix-synapse.up.railway.app/_matrix/media/v1/download/MqnlVpJGrlhqFyWcITBVhcvH?allow_redirect=true`
- Başka bir format

### Yöntem 2: Browser Console (JavaScript)

Element Web'de bir resim açın ve browser console'da (F12 → Console) şunu çalıştırın:

```javascript
// Element Web'in Matrix Client instance'ını bul
const client = window.mxMatrixClient || window.mxClient;

if (client) {
    // MXC URL'yi HTTP URL'ye çevir
    const mxcUrl = 'mxc://matrix-synapse.up.railway.app/MqnlVpJGrlhqFyWcITBVhcvH';
    const httpUrl = client.mxcUrlToHttp(mxcUrl);
    console.log('Element Web Media URL:', httpUrl);
    
    // Veya direkt media API'yi kullan
    const mediaUrl = client.getMediaUrl(mxcUrl);
    console.log('Element Web Media URL (getMediaUrl):', mediaUrl);
} else {
    console.log('Matrix Client bulunamadı');
}
```

### Yöntem 3: Element Web Settings

1. Element Web'de **Settings** → **Help & About**
2. **Server** bilgisini kontrol edin
3. Bu URL'i kullanarak media URL formatını oluşturun

---

## 📋 Bulduğunuz URL'yi Paylaşın

Hangi yöntemi kullanırsanız kullanın, bulduğunuz URL formatını paylaşın. Örneğin:

```
https://matrix-synapse.up.railway.app/_matrix/client/v3/download/matrix-synapse.up.railway.app/MqnlVpJGrlhqFyWcITBVhcvH
```

Bu URL formatını admin panel'de kullanacağız.

---

## 🔧 Alternatif: Element Web'in Base URL'ini Kontrol

Eğer Element Web farklı bir Matrix server'a bağlanıyorsa:

1. Element Web'de **Settings** → **General** → **Advanced**
2. **Custom server** ayarını kontrol edin
3. Bu URL'i admin panel'de `SYNAPSE_URL` olarak kullanın

---

## 💡 Hızlı Test

Element Web'de bir resim açın ve browser console'da şunu çalıştırın:

```javascript
// Tüm network request'lerini filtrele
performance.getEntriesByType('resource')
    .filter(r => r.name.includes('download') || r.name.includes('media'))
    .forEach(r => console.log('Media URL:', r.name));
```

Bu komut tüm media request'lerini gösterecektir.

