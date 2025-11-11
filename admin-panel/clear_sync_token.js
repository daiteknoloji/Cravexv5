/**
 * Element Web Sync Token Temizleme Script'i
 * 
 * Kullanım:
 * 1. Element Web'i açın ve login olun
 * 2. Browser Developer Tools'u açın (F12)
 * 3. Console sekmesine bu script'i yapıştırın
 * 4. Enter'a basın
 * 5. Sayfa otomatik olarak yenilenecek
 */

(async function clearSyncTokenAndReload() {
    try {
        console.log('🔄 Sync token temizleme başlatılıyor...');
        
        // Tüm IndexedDB database'lerini listele
        const databases = await indexedDB.databases();
        console.log('📊 Mevcut IndexedDB database\'leri:', databases.map(db => db.name));
        
        // matrix-js-sdk database'ini sil
        const dbName = 'matrix-js-sdk';
        return new Promise((resolve, reject) => {
            const request = indexedDB.deleteDatabase(dbName);
            
            request.onsuccess = () => {
                console.log('✅ Sync token başarıyla temizlendi!');
                console.log('🔄 Sayfa 2 saniye içinde yenilenecek...');
                
                setTimeout(() => {
                    console.log('🔄 Sayfa yenileniyor...');
                    location.reload();
                }, 2000);
                
                resolve();
            };
            
            request.onerror = () => {
                console.error('❌ Hata:', request.error);
                alert('Hata oluştu: ' + request.error?.message || 'Bilinmeyen hata');
                reject(request.error);
            };
            
            request.onblocked = () => {
                console.warn('⚠️ Database silme engellendi.');
                console.warn('💡 Lütfen tüm Element Web sekmelerini kapatıp tekrar deneyin.');
                alert('Database silme engellendi. Lütfen tüm Element Web sekmelerini kapatıp tekrar deneyin.');
            };
        });
    } catch (error) {
        console.error('❌ Beklenmeyen hata:', error);
        alert('Hata oluştu: ' + error.message + '\n\nLütfen IndexedDB\'yi manuel olarak temizleyin.');
    }
})();

