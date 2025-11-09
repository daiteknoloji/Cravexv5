#!/usr/bin/env python3
"""
Kullanıcı şifresini düzeltme scripti
Kullanım: python fix-user-password.py @2r:matrix-synapse.up.railway.app 12344321
"""

import sys
import os
import psycopg2
import bcrypt

# PostgreSQL bağlantısı - Railway ortam değişkenlerinden
DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'database': os.getenv('PGDATABASE', 'synapse'),
    'user': os.getenv('PGUSER', 'synapse_user'),
    'password': os.getenv('PGPASSWORD', 'SuperGucluSifre2024!'),
    'port': int(os.getenv('PGPORT', '5432'))
}

def fix_user_password(user_id, password):
    """Kullanıcı şifresini düzelt"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Kullanıcıyı kontrol et
        cur.execute("SELECT name, password_hash, deactivated FROM users WHERE name = %s", (user_id,))
        user_row = cur.fetchone()
        
        if not user_row:
            print(f"[HATA] Kullanıcı bulunamadı: {user_id}")
            return False
        
        print(f"[INFO] Kullanıcı bulundu: {user_row[0]}")
        print(f"[INFO] Mevcut password_hash: {user_row[1][:30] if user_row[1] else 'NULL'}...")
        print(f"[INFO] Deactivated: {user_row[2]}")
        
        # Yeni şifre hash'i oluştur
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        print(f"[INFO] Yeni password_hash: {password_hash[:30]}...")
        
        # Şifreyi güncelle
        cur.execute("UPDATE users SET password_hash = %s WHERE name = %s", (password_hash, user_id))
        conn.commit()
        
        # Doğrula
        cur.execute("SELECT password_hash FROM users WHERE name = %s", (user_id,))
        verify_row = cur.fetchone()
        
        if verify_row and verify_row[0]:
            # Şifre hash'i test et
            test_check = bcrypt.checkpw(password.encode('utf-8'), verify_row[0].encode('utf-8'))
            if test_check:
                print(f"[BAŞARILI] Şifre hash'i doğru şekilde güncellendi ve doğrulandı!")
                print(f"[INFO] Kullanıcı artık '{password}' şifresi ile login olabilir.")
            else:
                print(f"[HATA] Şifre hash'i güncellendi ama doğrulama başarısız!")
                return False
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"[HATA] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Kullanım: python fix-user-password.py <user_id> <password>")
        print("Örnek: python fix-user-password.py @2r:matrix-synapse.up.railway.app 12344321")
        sys.exit(1)
    
    user_id = sys.argv[1]
    password = sys.argv[2]
    
    print(f"[INFO] Kullanıcı şifresi düzeltiliyor: {user_id}")
    print(f"[INFO] Yeni şifre: {password}")
    print()
    
    if fix_user_password(user_id, password):
        print()
        print("[BAŞARILI] İşlem tamamlandı!")
    else:
        print()
        print("[HATA] İşlem başarısız!")
        sys.exit(1)

