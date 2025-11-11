-- ============================================
-- ADMIN KULLANICISININ ŞİFRESİNİ GÜNCELLEME
-- ============================================
-- Bu sorgu mevcut admin kullanıcısının password hash'ini günceller
-- Şifre: GucluBirSifre123!
-- ============================================

-- Mevcut admin kullanıcısını kontrol et
SELECT name, admin, deactivated, locked FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';

-- Password hash'i güncelle
UPDATE users 
SET password_hash = '$2b$12$FGKyY303UV/fEYEvUHFkKORQsmNH4vjDArTqbfvv3f3eXiFmWnRS6',  -- GucluBirSifre123! için hash
    admin = 1,
    deactivated = 0,
    locked = false
WHERE name = '@admin:matrix-synapse.up.railway.app';

-- Kontrol sorgusu
SELECT name, admin, deactivated, locked FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';

-- ============================================
-- ELEMENT WEB'DE LOGIN:
-- ============================================
-- Kullanıcı adı: admin
-- Şifre: GucluBirSifre123!
-- ============================================

