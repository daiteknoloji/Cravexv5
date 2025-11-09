#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kullanıcıyı pasif/aktif yap
"""
import requests
import json
import sys
import io

# Windows encoding sorununu çöz
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Admin Panel URL
ADMIN_PANEL_URL = "https://considerate-adaptation-production.up.railway.app"
user_id = "@6e:matrix-synapse.up.railway.app"

# Kullanıcıdan şifre al (pasif yapmak için)
import getpass

print(f"\n{'='*80}")
print(f"KULLANICI DURUM DEĞİŞTİRME: {user_id}")
print(f"{'='*80}\n")

try:
    # 1. Login
    login_url = f"{ADMIN_PANEL_URL}/login"
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    session = requests.Session()
    login_response = session.post(login_url, data=login_data, timeout=10)
    
    if login_response.status_code != 200:
        print(f"❌ LOGIN HATASI: {login_response.status_code}")
        exit(1)
    
    print("✅ Admin Panel'e giriş yapıldı\n")
    
    # 2. Mevcut durumu kontrol et
    users_url = f"{ADMIN_PANEL_URL}/api/users"
    users_response = session.get(users_url, timeout=10)
    users_data = users_response.json()
    
    user = None
    for u in users_data.get('users', []):
        if u.get('user_id') == user_id:
            user = u
            break
    
    if not user:
        print(f"❌ KULLANICI BULUNAMADI: {user_id}")
        exit(1)
    
    current_status = "PASİF" if user.get('deactivated') else "AKTİF"
    print(f"📊 MEVCUT DURUM: {current_status}\n")
    
    # 3. Durum değiştirme
    if user.get('deactivated'):
        # Aktif yap
        print("🔄 KULLANICIYI AKTİF YAPIYORUM...\n")
        action = "aktif"
        deactivate_url = f"{ADMIN_PANEL_URL}/api/users/{user_id.replace('@', '').replace(':', '/')}/deactivate"
        response = session.put(
            deactivate_url,
            json={"deactivated": False},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
    else:
        # Pasif yap - şifre gerekli
        print("🔄 KULLANICIYI PASİF YAPIYORUM...\n")
        print("⚠️  Pasif yapmak için yeni şifre belirlemeniz gerekiyor!")
        print("   (Kullanıcı aktif edildiğinde bu şifre ile login olabilecek)\n")
        
        new_password = input("Yeni şifre girin (min 8 karakter): ")
        if len(new_password) < 8:
            print("❌ Şifre en az 8 karakter olmalı!")
            exit(1)
        
        confirm_password = input("Şifreyi tekrar girin: ")
        if new_password != confirm_password:
            print("❌ Şifreler eşleşmiyor!")
            exit(1)
        
        action = "pasif"
        deactivate_url = f"{ADMIN_PANEL_URL}/api/users/{user_id.replace('@', '').replace(':', '/')}/deactivate"
        response = session.put(
            deactivate_url,
            json={
                "deactivated": True,
                "new_password": new_password
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
    
    # 4. Sonucu göster
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"✅ KULLANICI BAŞARIYLA {action.upper()} YAPILDI!")
            print(f"   Mesaj: {result.get('message', 'N/A')}\n")
            
            # Yeni durumu kontrol et
            users_response = session.get(users_url, timeout=10)
            users_data = users_response.json()
            
            for u in users_data.get('users', []):
                if u.get('user_id') == user_id:
                    new_status = "PASİF" if u.get('deactivated') else "AKTİF"
                    print(f"📊 YENİ DURUM: {new_status}")
                    break
        else:
            print(f"❌ İŞLEM BAŞARISIZ: {result.get('error', 'Bilinmeyen hata')}")
    else:
        print(f"❌ API HATASI: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API HATASI: {e}")
except KeyboardInterrupt:
    print("\n\n⚠️  İşlem iptal edildi!")
except Exception as e:
    print(f"❌ HATA: {e}")
    import traceback
    traceback.print_exc()

