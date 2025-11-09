#!/usr/bin/env python3
"""
Matrix Synapse Media API Test Script
====================================
Bu script Matrix Synapse'in media API'sini direkt test eder.
"""

import requests
import os
import sys

# Environment variables
SYNAPSE_URL = os.getenv('SYNAPSE_URL', 'https://matrix-synapse.up.railway.app')
HOMESERVER_DOMAIN = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Media bilgileri
MEDIA_ID = 'HQtoyORnVrJmhoFLGhWQZZQD'
SERVER_NAME = HOMESERVER_DOMAIN

def get_admin_token():
    """Admin token al"""
    print(f"[1/3] Admin token alınıyor...")
    try:
        login_url = f'{SYNAPSE_URL}/_matrix/client/v3/login'
        login_data = {
            'type': 'm.login.password',
            'identifier': {'type': 'm.id.user', 'user': ADMIN_USERNAME},
            'password': ADMIN_PASSWORD
        }
        
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"[OK] Token alindi: {token[:20]}...")
            return token
        else:
            print(f"[ERROR] Token alinamadi: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Token alma hatasi: {e}")
        return None

def test_media_url(url, token=None):
    """Media URL'ini test et"""
    headers = {
        'User-Agent': 'Cravex-Admin-Panel-Test/1.0',
        'Accept': '*/*'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        print(f"\n[TEST] Test ediliyor: {url}")
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"   Content-Length: {response.headers.get('Content-Length', 'N/A')}")
        
        if response.status_code == 200:
            print(f"   [OK] BASARILI! Dosya boyutu: {len(response.content)} bytes")
            return True
        else:
            print(f"   [ERROR] Basarisiz")
            if response.headers.get('Content-Type', '').startswith('application/json'):
                print(f"   Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   [ERROR] Hata: {e}")
        return False

def main():
    print("=" * 60)
    print("MATRIX SYNAPSE MEDIA API TEST")
    print("=" * 60)
    print(f"Synapse URL: {SYNAPSE_URL}")
    print(f"Server Name: {SERVER_NAME}")
    print(f"Media ID: {MEDIA_ID}")
    print("=" * 60)
    
    # Token al
    token = get_admin_token()
    if not token:
        print("\n[WARN] Token alinamadi, authentication olmadan test ediliyor...")
    
    print(f"\n[2/3] Media URL'leri test ediliyor...")
    
    # Test edilecek URL formatları
    test_urls = [
        # Media API v3 (Element Web formatı)
        f'{SYNAPSE_URL}/_matrix/media/v3/download/{SERVER_NAME}/{MEDIA_ID}?allow_redirect=true',
        
        # Client API v3
        f'{SYNAPSE_URL}/_matrix/client/v3/download/{SERVER_NAME}/{MEDIA_ID}',
        
        # Media API r0 (eski format)
        f'{SYNAPSE_URL}/_matrix/media/r0/download/{SERVER_NAME}/{MEDIA_ID}',
        
        # Media API v1
        f'{SYNAPSE_URL}/_matrix/media/v1/download/{SERVER_NAME}/{MEDIA_ID}',
        
        # Media API r0 (server_name olmadan)
        f'{SYNAPSE_URL}/_matrix/media/r0/download/{MEDIA_ID}',
        
        # Client API v3 (server_name olmadan)
        f'{SYNAPSE_URL}/_matrix/client/v3/download/{MEDIA_ID}',
    ]
    
    success_count = 0
    for url in test_urls:
        if test_media_url(url, token):
            success_count += 1
    
    print(f"\n[3/3] Sonuç:")
    print(f"   Toplam test: {len(test_urls)}")
    print(f"   Başarılı: {success_count}")
    print(f"   Başarısız: {len(test_urls) - success_count}")
    
    if success_count == 0:
        print("\n[WARN] Hicbir URL formati calismadi!")
        print("   Olası nedenler:")
        print("   1. Media dosyasi Matrix Synapse'de yok (silinmis)")
        print("   2. Element Web cache'den gosteriyor")
        print("   3. Farkli bir URL formati kullaniliyor")
        print("\n   Cozum: Element Web'in Network sekmesinden gercek URL'yi bulun")
    else:
        print(f"\n[OK] {success_count} URL formati calisti!")
        print("   Admin panel'i bu URL formatina gore guncelleyebiliriz.")

if __name__ == '__main__':
    main()

