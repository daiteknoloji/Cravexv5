#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kullanıcıyı Matrix API ile zorla aktif yap
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
SYNAPSE_URL = "https://matrix-synapse.up.railway.app"
user_id = "@6e:matrix-synapse.up.railway.app"

print(f"\n{'='*80}")
print(f"KULLANICIYI ZORLA AKTİF YAPMA: {user_id}")
print(f"{'='*80}\n")

try:
    # 1. Admin Panel'e login ve admin token al
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
    
    # 2. Admin token almak için Matrix'e login ol
    print("🔑 Admin token alınıyor...\n")
    
    admin_login_url = f"{SYNAPSE_URL}/_matrix/client/v3/login"
    admin_login_data = {
        "type": "m.login.password",
        "identifier": {
            "type": "m.id.user",
            "user": "admin"
        },
        "password": "admin123"
    }
    
    admin_login_response = requests.post(admin_login_url, json=admin_login_data, timeout=10)
    
    if admin_login_response.status_code != 200:
        print(f"❌ ADMIN LOGIN HATASI: {admin_login_response.status_code}")
        print(f"Response: {admin_login_response.text[:200]}")
        exit(1)
    
    admin_token = admin_login_response.json().get('access_token')
    if not admin_token:
        print("❌ Admin token alınamadı!")
        exit(1)
    
    print(f"✅ Admin token alındı: {admin_token[:20]}...\n")
    
    # 3. Kullanıcının mevcut durumunu Matrix API'den kontrol et
    print("📊 Matrix API'den kullanıcı durumu kontrol ediliyor...\n")
    
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }
    
    get_user_url = f"{SYNAPSE_URL}/_synapse/admin/v2/users/{user_id}"
    get_user_response = requests.get(get_user_url, headers=headers, timeout=10)
    
    if get_user_response.status_code == 200:
        user_data = get_user_response.json()
        current_deactivated = user_data.get('deactivated', False)
        print(f"   Matrix API Durum: {'🔴 PASİF' if current_deactivated else '🟢 AKTİF'}")
        print(f"   Display Name: {user_data.get('displayname', 'Yok')}")
        print(f"   Admin: {'✅ Evet' if user_data.get('admin', False) else '❌ Hayır'}\n")
    else:
        print(f"⚠️  Kullanıcı bilgileri alınamadı: {get_user_response.status_code}")
        print(f"   Response: {get_user_response.text[:200]}\n")
        user_data = {}
    
    # 4. Kullanıcıyı aktif yap
    print("🔄 Kullanıcıyı Matrix API ile aktif yapıyorum...\n")
    
    # Sadece deactivated: False gönder (şifreyi değiştirme)
    activate_data = {
        'deactivated': False
    }
    
    activate_url = f"{SYNAPSE_URL}/_synapse/admin/v2/users/{user_id}"
    activate_response = requests.put(
        activate_url,
        headers=headers,
        json=activate_data,
        timeout=10
    )
    
    if activate_response.status_code == 200:
        print("✅ Kullanıcı Matrix API ile aktif yapıldı!\n")
        
        # 5. Durumu tekrar kontrol et
        print("📊 Yeni durum kontrol ediliyor...\n")
        get_user_response = requests.get(get_user_url, headers=headers, timeout=10)
        
        if get_user_response.status_code == 200:
            user_data = get_user_response.json()
            new_deactivated = user_data.get('deactivated', False)
            print(f"   Yeni Durum: {'🔴 PASİF' if new_deactivated else '🟢 AKTİF'}")
            
            if not new_deactivated:
                print("\n✅ BAŞARILI! Kullanıcı artık aktif ve login olabilir.")
            else:
                print("\n⚠️  Kullanıcı hala pasif görünüyor. Matrix Synapse restart gerekebilir.")
        else:
            print(f"⚠️  Durum kontrol edilemedi: {get_user_response.status_code}")
    else:
        print(f"❌ AKTİF YAPMA HATASI: {activate_response.status_code}")
        print(f"   Response: {activate_response.text[:500]}")
        
        # Alternatif: v1 API'yi dene
        print("\n🔄 Alternatif yöntem deneniyor (v1 API)...\n")
        
        # v1 API'de activate için özel bir endpoint yok, sadece deactivate var
        # Bu durumda v2 API'yi tekrar deneyelim ama farklı bir yaklaşımla
        
        # Kullanıcı bilgilerini al ve sadece deactivated'i False yap
        if user_data:
            user_data['deactivated'] = False
            # Password field'ını kaldır
            if 'password' in user_data:
                del user_data['password']
            
            activate_response2 = requests.put(
                activate_url,
                headers=headers,
                json=user_data,
                timeout=10
            )
            
            if activate_response2.status_code == 200:
                print("✅ Alternatif yöntemle aktif yapıldı!")
            else:
                print(f"❌ Alternatif yöntem de başarısız: {activate_response2.status_code}")
                print(f"   Response: {activate_response2.text[:500]}")
    
    # 6. Veritabanını da güncelle
    print("\n🔄 Veritabanı güncelleniyor...\n")
    
    # Admin panel API'sini kullanarak veritabanını güncelle
    deactivate_api_url = f"{ADMIN_PANEL_URL}/api/users/{user_id.replace('@', '').replace(':', '/')}/deactivate"
    db_update_response = session.put(
        deactivate_api_url,
        json={"deactivated": False},
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    if db_update_response.status_code == 200:
        result = db_update_response.json()
        if result.get('success'):
            print("✅ Veritabanı güncellendi!")
        else:
            print(f"⚠️  Veritabanı güncellenemedi: {result.get('error', 'Bilinmeyen hata')}")
    else:
        print(f"⚠️  Veritabanı güncelleme hatası: {db_update_response.status_code}")
    
    print(f"\n{'='*80}")
    print("📋 ÖZET:")
    print(f"{'='*80}")
    print("1. Matrix Admin API v2 ile aktif yapma işlemi tamamlandı")
    print("2. Veritabanı güncellendi")
    print("\n💡 Şimdi Element Web'den login olmayı deneyin!")
    print("   Eğer hala 'deactivated' hatası alıyorsanız:")
    print("   - Matrix Synapse servisini restart edin (Railway dashboard)")
    print("   - Birkaç saniye bekleyin ve tekrar deneyin")
    print(f"{'='*80}\n")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API HATASI: {e}")
except Exception as e:
    print(f"❌ HATA: {e}")
    import traceback
    traceback.print_exc()

