# Element Web Sync Sorunu Çözümü

## Sorun
Odalar admin panelde görünüyor ama Element Web chat ekranında görünmüyor. Console'da `404: No row found` hatası alınıyor.

## Neden
Element Web'in IndexedDB'sinde saklanan sync token geçersiz hale gelmiş. Büyük veri silme işlemlerinden sonra Synapse'in sync state'i değişti ama Element Web eski token'ı kullanmaya devam ediyor.

## Çözüm Yöntemleri

### Yöntem 1: Browser Console'dan Sync Token'ı Temizleme (HIZLI - ÖNERİLEN)

1. Element Web'i açın ve login olun
2. Browser Developer Tools'u açın (F12)
3. Console sekmesine gidin
4. Aşağıdaki kodu yapıştırıp Enter'a basın:

```javascript
// IndexedDB'deki sync token'ı temizle ve fresh sync başlat
(async function clearSyncTokenAndReload() {
    try {
        // Tüm IndexedDB database'lerini listele
        const databases = await indexedDB.databases();
        console.log('Mevcut IndexedDB database\'leri:', databases.map(db => db.name));
        
        // matrix-js-sdk database'ini sil
        const dbName = 'matrix-js-sdk';
        return new Promise((resolve, reject) => {
            const request = indexedDB.deleteDatabase(dbName);
            request.onsuccess = () => {
                console.log('✅ Sync token temizlendi! Sayfa yenileniyor...');
                setTimeout(() => {
                    location.reload();
                }, 1000);
                resolve();
            };
            request.onerror = () => {
                console.error('❌ Hata:', request.error);
                reject(request.error);
            };
            request.onblocked = () => {
                console.warn('⚠️ Database silme engellendi. Lütfen tüm Element Web sekmelerini kapatıp tekrar deneyin.');
            };
        });
    } catch (error) {
        console.error('❌ Beklenmeyen hata:', error);
        alert('Hata oluştu. Lütfen IndexedDB\'yi manuel olarak temizleyin (Yöntem 2).');
    }
})();
```

5. Sayfa otomatik olarak yenilenecek ve fresh sync başlayacak
6. Odalar artık görünmelidir

### Yöntem 2: IndexedDB'yi Manuel Temizleme (GÜVENLİ)

1. Browser Developer Tools'u açın (F12)
2. **Application** (Chrome) veya **Storage** (Firefox) sekmesine gidin
3. Sol menüden **IndexedDB** → **matrix-js-sdk** seçin
4. Sağ tıklayıp **Delete database** seçin
5. **Local Storage** → Element Web domain'i → Tüm key'leri silin
6. Browser'ı kapatıp yeniden açın
7. Element Web'e yeniden login olun

### Yöntem 3: Logout/Login (BASIT)

1. Element Web'de logout yapın
2. Browser cache'ini temizleyin (Ctrl+Shift+Delete)
3. Element Web'e yeniden login olun

**NOT:** Bu yöntem bazen yeterli olmayabilir çünkü IndexedDB temizlenmeyebilir.

### Yöntem 4: Incognito/Private Mode (TEST İÇİN)

1. Browser'ı incognito/private mode'da açın
2. Element Web'e login olun
3. Odalar görünüyorsa, normal modda IndexedDB'yi temizleyin

## Kontrol

Çözüm uygulandıktan sonra:
1. Yeni bir oda oluşturun
2. Odanın Element Web'de göründüğünü kontrol edin
3. Console'da `404: No row found` hatasının kaybolduğunu kontrol edin

## Teknik Detaylar

- Element Web sync token'ı IndexedDB'de `matrix-js-sdk` database'inde saklar
- Sync token, Synapse'den gelen son sync response'un `next_batch` değeridir
- Büyük veri silme işlemlerinden sonra bu token geçersiz hale gelir
- Fresh sync için token'ın silinmesi veya `null` yapılması gerekir

## Sorun Devam Ederse

1. Synapse servisini Railway'de restart edin
2. `fix_synapse_sync_state.sql` script'ini çalıştırın
3. Tüm kullanıcılar için IndexedDB'yi temizleyin

