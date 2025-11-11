-- ============================================
-- SQL İLE ADMIN KULLANICISI OLUŞTURMA (Password Hash ile)
-- ============================================
-- Bu sorgu admin kullanıcısını direkt veritabanında oluşturur
-- Şifre: GüçlüBirŞifre123!
-- ============================================
-- ÖNCE: generate_password_hash.py script'ini çalıştırın ve hash'i alın
-- python generate_password_hash.py "GüçlüBirŞifre123!"
-- ============================================

-- Önce admin kullanıcısının var olup olmadığını kontrol et
SELECT name, admin, deactivated FROM users WHERE name LIKE '@admin:%';

-- Admin kullanıcısını oluştur
-- NOT: password_hash'i generate_password_hash.py script'i ile oluşturun
-- Örnek hash (GüçlüBirŞifre123! için):
-- $2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
INSERT INTO users (name, password_hash, creation_ts, admin, deactivated, locked, user_type)
VALUES (
    '@admin:matrix-synapse.up.railway.app',
    '$2b$12$YOUR_GENERATED_HASH_HERE',  -- generate_password_hash.py ile oluşturun!
    EXTRACT(EPOCH FROM NOW()) * 1000,  -- milliseconds
    1,  -- admin = 1 (admin kullanıcısı)
    0,  -- deactivated = 0 (aktif)
    0,  -- locked = 0 (kilitli değil)
    NULL  -- user_type = NULL (normal kullanıcı)
)
ON CONFLICT (name) DO UPDATE SET
    admin = 1,
    deactivated = 0,
    locked = 0,
    password_hash = '$2b$12$YOUR_GENERATED_HASH_HERE';  -- Hash'i güncelle

-- Kontrol sorgusu
SELECT name, admin, deactivated, locked, creation_ts FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';

-- ============================================
-- KULLANIM:
-- ============================================
-- 1. generate_password_hash.py script'ini çalıştırın:
--    python generate_password_hash.py "GüçlüBirŞifre123!"
--
-- 2. Oluşturulan hash'i kopyalayın
--
-- 3. Yukarıdaki sorguda '$2b$12$YOUR_GENERATED_HASH_HERE' yerine hash'i yapıştırın
--
-- 4. Sorguyu Railway PostgreSQL'de çalıştırın
--
-- 5. Element Web'de admin kullanıcısıyla login olun:
--    Kullanıcı: admin
--    Şifre: GüçlüBirŞifre123!
-- ============================================

