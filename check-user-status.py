#!/usr/bin/env python3
"""
Kullanıcı durumunu veritabanından kontrol et
"""
import psycopg2
import os
from datetime import datetime

# Railway PostgreSQL bağlantı bilgileri
DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'database': os.getenv('PGDATABASE', 'synapse'),
    'user': os.getenv('PGUSER', 'synapse_user'),
    'password': os.getenv('PGPASSWORD', 'SuperGucluSifre2024!'),
    'port': int(os.getenv('PGPORT', '5432'))
}

user_id = '@6e:matrix-synapse.up.railway.app'

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print(f"\n{'='*80}")
    print(f"KULLANICI DURUM KONTROLÜ: {user_id}")
    print(f"{'='*80}\n")
    
    # 1. Users tablosundan temel bilgiler
    cur.execute("""
        SELECT 
            name,
            password_hash,
            creation_ts,
            admin,
            deactivated,
            shadow_banned,
            locked,
            displayname,
            avatar_url,
            is_guest,
            consent_version,
            consent_server_notice_sent,
            consent_ts,
            appservice_id,
            locked_ts
        FROM users 
        WHERE name = %s
    """, (user_id,))
    
    user_data = cur.fetchone()
    
    if not user_data:
        print(f"❌ KULLANICI BULUNAMADI: {user_id}")
        print("\nKullanıcı veritabanında kayıtlı değil!")
    else:
        print("✅ KULLANICI BULUNDU\n")
        print(f"📋 TEMEL BİLGİLER:")
        print(f"   User ID: {user_data[0]}")
        print(f"   Şifre Hash: {user_data[1][:50]}..." if user_data[1] else "   Şifre Hash: NULL")
        print(f"   Oluşturulma: {datetime.fromtimestamp(user_data[2]/1000).strftime('%Y-%m-%d %H:%M:%S') if user_data[2] else 'N/A'}")
        print(f"   Admin: {'✅ Evet' if user_data[3] else '❌ Hayır'}")
        print(f"   Pasif (Deactivated): {'🔴 EVET' if user_data[4] else '🟢 HAYIR'}")
        print(f"   Shadow Banned: {'✅ Evet' if user_data[5] else '❌ Hayır'}")
        print(f"   Kilitli (Locked): {'✅ Evet' if user_data[6] else '❌ Hayır'}")
        print(f"   Display Name: {user_data[7] or 'Yok'}")
        print(f"   Avatar URL: {user_data[8] or 'Yok'}")
        print(f"   Misafir (Guest): {'✅ Evet' if user_data[9] else '❌ Hayır'}")
        print(f"   Consent Version: {user_data[10] or 'N/A'}")
        print(f"   Consent Server Notice Sent: {'✅ Evet' if user_data[11] else '❌ Hayır'}")
        print(f"   Consent TS: {datetime.fromtimestamp(user_data[12]/1000).strftime('%Y-%m-%d %H:%M:%S') if user_data[12] else 'N/A'}")
        print(f"   Appservice ID: {user_data[13] or 'N/A'}")
        print(f"   Locked TS: {datetime.fromtimestamp(user_data[14]/1000).strftime('%Y-%m-%d %H:%M:%S') if user_data[14] else 'N/A'}")
        
        # 2. Access tokens kontrolü
        cur.execute("SELECT COUNT(*) FROM access_tokens WHERE user_id = %s", (user_id,))
        token_count = cur.fetchone()[0]
        print(f"\n🔑 ACCESS TOKENS: {token_count} adet")
        
        if token_count > 0:
            cur.execute("""
                SELECT token, device_id, last_used 
                FROM access_tokens 
                WHERE user_id = %s 
                ORDER BY last_used DESC 
                LIMIT 5
            """, (user_id,))
            tokens = cur.fetchall()
            print("   Son kullanılan token'lar:")
            for i, (token, device_id, last_used) in enumerate(tokens, 1):
                token_preview = token[:20] + "..." if len(token) > 20 else token
                last_used_str = datetime.fromtimestamp(last_used/1000).strftime('%Y-%m-%d %H:%M:%S') if last_used else 'N/A'
                print(f"   {i}. Token: {token_preview} | Device: {device_id or 'N/A'} | Son Kullanım: {last_used_str}")
        
        # 3. Devices kontrolü
        cur.execute("SELECT COUNT(*) FROM devices WHERE user_id = %s", (user_id,))
        device_count = cur.fetchone()[0]
        print(f"\n📱 DEVICES: {device_count} adet")
        
        if device_count > 0:
            cur.execute("""
                SELECT device_id, display_name, last_seen_ts 
                FROM devices 
                WHERE user_id = %s 
                ORDER BY last_seen_ts DESC 
                LIMIT 5
            """, (user_id,))
            devices = cur.fetchall()
            print("   Cihazlar:")
            for i, (device_id, display_name, last_seen) in enumerate(devices, 1):
                last_seen_str = datetime.fromtimestamp(last_seen/1000).strftime('%Y-%m-%d %H:%M:%S') if last_seen else 'N/A'
                print(f"   {i}. Device ID: {device_id} | Name: {display_name or 'N/A'} | Son Görülme: {last_seen_str}")
        
        # 4. Room memberships kontrolü
        cur.execute("SELECT COUNT(*) FROM room_memberships WHERE user_id = %s", (user_id,))
        room_count = cur.fetchone()[0]
        print(f"\n🏠 ROOM MEMBERSHIPS: {room_count} adet")
        
        # 5. User directory kontrolü
        cur.execute("SELECT COUNT(*) FROM user_directory WHERE user_id = %s", (user_id,))
        dir_count = cur.fetchone()[0]
        print(f"📂 USER DIRECTORY: {dir_count} adet kayıt")
        
        # 6. Profiles kontrolü
        cur.execute("SELECT displayname, avatar_url FROM profiles WHERE user_id = %s", (user_id,))
        profile = cur.fetchone()
        if profile:
            print(f"👤 PROFILE:")
            print(f"   Display Name: {profile[0] or 'Yok'}")
            print(f"   Avatar URL: {profile[1] or 'Yok'}")
        else:
            print(f"👤 PROFILE: Yok")
        
        # ÖZET
        print(f"\n{'='*80}")
        print("📊 ÖZET:")
        print(f"{'='*80}")
        print(f"   Durum: {'🔴 PASİF' if user_data[4] else '🟢 AKTİF'}")
        print(f"   Admin: {'✅ Evet' if user_data[3] else '❌ Hayır'}")
        print(f"   Aktif Token: {token_count} adet")
        print(f"   Cihaz: {device_count} adet")
        print(f"   Oda Üyeliği: {room_count} adet")
        print(f"{'='*80}\n")
    
    cur.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"❌ VERİTABANI HATASI: {e}")
except Exception as e:
    print(f"❌ HATA: {e}")
    import traceback
    traceback.print_exc()

