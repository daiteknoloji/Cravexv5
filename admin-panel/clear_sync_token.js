/**
 * Element Web Sync Token Temizleme Script'i (GELİŞTİRİLMİŞ)
 * 
 * Bu script tüm sync token'ları ve ilgili verileri temizler:
 * - IndexedDB (matrix-js-sdk database)
 * - localStorage (sync token ve session bilgileri)
 * - MatrixClient internal state (eğer mevcutsa)
 * 
 * Kullanım:
 * 1. Element Web'i açın ve login olun
 * 2. Browser Developer Tools'u açın (F12)
 * 3. Console sekmesine bu script'i yapıştırın
 * 4. Enter'a basın
 * 5. Sayfa otomatik olarak yenilenecek ve fresh sync başlayacak
 */

(async function clearSyncTokenAndReload() {
    try {
        console.log('🔄 Kapsamlı sync token temizleme başlatılıyor...');
        
        // 1. IndexedDB'deki tüm matrix-js-sdk database'lerini sil
        console.log('📦 IndexedDB temizleniyor...');
        const databases = await indexedDB.databases();
        const matrixDatabases = databases.filter(db => 
            db.name && (
                db.name.startsWith('matrix-js-sdk') || 
                db.name.includes('matrix-sdk')
            )
        );
        
        console.log('📊 Bulunan Matrix database\'leri:', matrixDatabases.map(db => db.name));
        
        // Tüm Matrix database'lerini sil
        const deletePromises = matrixDatabases.map(db => {
            return new Promise((resolve, reject) => {
                const request = indexedDB.deleteDatabase(db.name);
                request.onsuccess = () => {
                    console.log(`✅ ${db.name} silindi`);
                    resolve();
                };
                request.onerror = () => {
                    console.warn(`⚠️ ${db.name} silinemedi:`, request.error);
                    resolve(); // Devam et, hata olsa bile
                };
                request.onblocked = () => {
                    console.warn(`⚠️ ${db.name} silme engellendi (başka sekme açık olabilir)`);
                    resolve(); // Devam et
                };
            });
        });
        
        await Promise.all(deletePromises);
        
        // 2. localStorage'daki sync token ve session bilgilerini temizle
        console.log('🗑️ localStorage temizleniyor...');
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && (
                key.includes('sync') || 
                key.includes('matrix') ||
                key.includes('mx_') ||
                key.startsWith('matrix')
            )) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
            console.log(`✅ localStorage'dan silindi: ${key}`);
        });
        
        // 3. SessionStorage'ı da temizle
        if (sessionStorage) {
            console.log('🗑️ sessionStorage temizleniyor...');
            sessionStorage.clear();
            console.log('✅ sessionStorage temizlendi');
        }
        
        // 4. MatrixClient'in internal state'ini temizlemek için window.mxMatrixClient'i kontrol et
        if (window.mxMatrixClient) {
            console.log('🔄 MatrixClient state temizleniyor...');
            try {
                const client = window.mxMatrixClient;
                if (client.stopClient) {
                    client.stopClient();
                    console.log('✅ MatrixClient durduruldu');
                }
            } catch (e) {
                console.warn('⚠️ MatrixClient durdurulamadı:', e);
            }
        }
        
        console.log('✅ Tüm sync token\'lar ve session bilgileri temizlendi!');
        console.log('🔄 Sayfa 3 saniye içinde yenilenecek...');
        console.log('💡 Sayfa yenilendikten sonra yeniden login olmanız gerekebilir.');
        
        setTimeout(() => {
            console.log('🔄 Sayfa yenileniyor...');
            // Hard reload - cache'i de temizle
            window.location.href = window.location.href.split('#')[0] + '#/login';
        }, 3000);
        
    } catch (error) {
        console.error('❌ Beklenmeyen hata:', error);
        alert('Hata oluştu: ' + error.message + '\n\nLütfen IndexedDB ve localStorage\'ı manuel olarak temizleyin.');
    }
})();

