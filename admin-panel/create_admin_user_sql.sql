-- ============================================
-- SQL İLE ADMIN KULLANICISI OLUŞTURMA
-- ============================================
-- Bu sorgu admin kullanıcısını direkt veritabanında oluşturur
-- Şifre: GüçlüBirŞifre123!
-- ============================================

-- Önce admin kullanıcısının var olup olmadığını kontrol et
SELECT name, admin, deactivated FROM users WHERE name LIKE '@admin:%';

-- Admin kullanıcısını oluştur (eğer yoksa)
-- NOT: password_hash geçici bir değer, sonra Matrix Admin API ile reset edilecek
-- VEYA: generate_password_hash.py script'ini kullanarak doğru hash'i oluşturun
INSERT INTO users (name, password_hash, creation_ts, admin, deactivated, locked, user_type)
VALUES (
    '@admin:matrix-synapse.up.railway.app',
    '$2b$12$PLACEHOLDER_PASSWORD_HASH_WILL_BE_SET_VIA_MATRIX_API',  -- Geçici hash
    EXTRACT(EPOCH FROM NOW()) * 1000,  -- milliseconds
    1,  -- admin = 1 (admin kullanıcısı)
    0,  -- deactivated = 0 (aktif)
    0,  -- locked = 0 (kilitli değil)
    NULL  -- user_type = NULL (normal kullanıcı)
)
ON CONFLICT (name) DO UPDATE SET
    admin = 1,
    deactivated = 0,
    locked = 0;

-- Kontrol sorgusu
SELECT name, admin, deactivated, locked, creation_ts FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';

-- ============================================
-- SONRAKI ADIMLAR:
-- ============================================
-- 1. generate_password_hash.py script'ini çalıştırın (şifre hash'i oluşturmak için)
-- 2. Oluşturulan hash'i yukarıdaki sorguda kullanın
-- 3. Element Web'de admin kullanıcısıyla login olun
-- ============================================
