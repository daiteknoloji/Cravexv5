#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Panel API'sini kullanarak kullanıcı durumunu kontrol et
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

print(f"\n{'='*80}")
print(f"KULLANICI DURUM KONTROLÜ: {user_id}")
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
        print(f"Response: {login_response.text[:200]}")
        exit(1)
    
    print("✅ Admin Panel'e giriş yapıldı\n")
    
    # 2. Kullanıcı listesini çek
    users_url = f"{ADMIN_PANEL_URL}/api/users"
    users_response = session.get(users_url, timeout=10)
    
    if users_response.status_code != 200:
        print(f"❌ KULLANICI LİSTESİ ALINAMADI: {users_response.status_code}")
        print(f"Response: {users_response.text[:200]}")
        exit(1)
    
    users_data = users_response.json()
    
    # Kullanıcıyı bul
    user = None
    for u in users_data.get('users', []):
        if u.get('user_id') == user_id:
            user = u
            break
    
    if not user:
        print(f"❌ KULLANICI BULUNAMADI: {user_id}")
        print("\nTüm kullanıcılar:")
        for u in users_data.get('users', [])[:10]:
            print(f"  - {u.get('user_id')}")
        exit(1)
    
    # 3. Kullanıcı bilgilerini göster
    print("✅ KULLANICI BULUNDU\n")
    print(f"📋 TEMEL BİLGİLER:")
    print(f"   User ID: {user.get('user_id')}")
    print(f"   Display Name: {user.get('displayname', 'Yok')}")
    print(f"   Admin: {'✅ Evet' if user.get('admin') else '❌ Hayır'}")
    print(f"   Pasif (Deactivated): {'🔴 EVET' if user.get('deactivated') else '🟢 HAYIR'}")
    print(f"   Oluşturulma: {user.get('created_at', 'N/A')}")
    print(f"   Son Görülme: {user.get('last_seen', 'N/A')}")
    
    # 4. Detaylı bilgi için user detail endpoint'i
    user_detail_url = f"{ADMIN_PANEL_URL}/api/users/{user_id.replace('@', '').replace(':', '/')}"
    detail_response = session.get(user_detail_url, timeout=10)
    
    if detail_response.status_code == 200:
        detail_data = detail_response.json()
        print(f"\n📊 DETAYLI BİLGİLER:")
        if 'user' in detail_data:
            detail = detail_data['user']
            print(f"   Shadow Banned: {'✅ Evet' if detail.get('shadow_banned') else '❌ Hayır'}")
            print(f"   Locked: {'✅ Evet' if detail.get('locked') else '❌ Hayır'}")
            print(f"   Avatar URL: {detail.get('avatar_url', 'Yok')}")
    
    # ÖZET
    print(f"\n{'='*80}")
    print("📊 ÖZET:")
    print(f"{'='*80}")
    print(f"   Durum: {'🔴 PASİF' if user.get('deactivated') else '🟢 AKTİF'}")
    print(f"   Admin: {'✅ Evet' if user.get('admin') else '❌ Hayır'}")
    print(f"{'='*80}\n")
    
    # Pasif/Aktif yapma önerisi
    if user.get('deactivated'):
        print("💡 KULLANICI ŞU ANDA PASİF")
        print("   Aktif yapmak için admin panelden 'Aktif Yap' butonuna tıklayın.")
    else:
        print("💡 KULLANICI ŞU ANDA AKTİF")
        print("   Pasif yapmak için admin panelden 'Pasif Yap' butonuna tıklayın.")
        print("   (Pasif yaparken yeni şifre belirlemeniz gerekecek)")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API HATASI: {e}")
except Exception as e:
    print(f"❌ HATA: {e}")
    import traceback
    traceback.print_exc()

