-- ============================================
-- SQL İLE ADMIN KULLANICISI OLUŞTURMA (Hazır Hash ile)
-- ============================================
-- Bu sorgu admin kullanıcısını direkt veritabanında oluşturur
-- Şifre: GucluBirSifre123!
-- ============================================

-- Önce admin kullanıcısının var olup olmadığını kontrol et
SELECT name, admin, deactivated FROM users WHERE name LIKE '@admin:%';

-- Admin kullanıcısını oluştur (password hash ile)
INSERT INTO users (name, password_hash, creation_ts, admin, deactivated, locked, user_type)
VALUES (
    '@admin:matrix-synapse.up.railway.app',
    '$2b$12$FGKyY303UV/fEYEvUHFkKORQsmNH4vjDArTqbfvv3f3eXiFmWnRS6',  -- GucluBirSifre123! için hash
    EXTRACT(EPOCH FROM NOW()) * 1000,  -- milliseconds
    1,  -- admin = 1 (admin kullanıcısı)
    0,  -- deactivated = 0 (aktif)
    false,  -- locked = false (kilitli değil) - BOOLEAN tipi için false kullan
    NULL  -- user_type = NULL (normal kullanıcı)
)
ON CONFLICT (name) DO UPDATE SET
    admin = 1,
    deactivated = 0,
    locked = false,  -- BOOLEAN tipi için false kullan
    password_hash = '$2b$12$FGKyY303UV/fEYEvUHFkKORQsmNH4vjDArTqbfvv3f3eXiFmWnRS6';  -- Hash'i güncelle

-- Kontrol sorgusu
SELECT name, admin, deactivated, locked, creation_ts FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';

-- ============================================
-- KULLANIM:
-- ============================================
-- 1. Bu sorguyu Railway PostgreSQL'de çalıştırın
-- 2. Element Web'de admin kullanıcısıyla login olun:
--    Kullanıcı: admin
--    Şifre: GucluBirSifre123!
-- 3. Login olduktan sonra token veritabanına kaydedilir
-- 4. Admin panel'den kullanıcı oluşturabilirsiniz
-- ============================================

