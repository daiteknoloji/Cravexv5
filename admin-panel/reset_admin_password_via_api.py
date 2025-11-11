#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matrix Synapse Admin Password Reset Script
==========================================
Bu script Matrix Synapse Admin API kullanarak admin kullanıcısının şifresini reset eder.
Registration shared secret kullanarak admin kullanıcısı oluşturur veya şifresini reset eder.
"""

import requests
import hmac
import hashlib
import sys
import os

def create_admin_user(synapse_url, username, password, registration_secret):
    """Registration shared secret kullanarak admin kullanıcısı oluştur"""
    
    # Step 1: Get nonce
    nonce_url = f'{synapse_url}/_synapse/admin/v1/register'
    try:
        nonce_response = requests.get(nonce_url, timeout=10)
        if nonce_response.status_code != 200:
            print(f"[ERROR] Failed to get nonce: {nonce_response.status_code}")
            print(f"[ERROR] Response: {nonce_response.text[:200]}")
            return False
        
        nonce_data = nonce_response.json()
        nonce = nonce_data.get('nonce')
        
        if not nonce:
            print("[ERROR] No nonce received from Synapse")
            return False
        
        print(f"[INFO] Nonce received: {nonce}")
        
        # Step 2: Calculate HMAC signature
        # Format: nonce + NULL + username + NULL + password + NULL + admin
        message = f"{nonce}\x00{username}\x00{password}\x00admin"
        mac = hmac.new(
            registration_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()
        
        print(f"[DEBUG] Calculated MAC: {mac}")
        
        # Step 3: Register admin user
        register_body = {
            'nonce': nonce,
            'username': username,
            'password': password,
            'admin': True,
            'mac': mac
        }
        
        register_response = requests.post(nonce_url, json=register_body, timeout=10)
        
        if register_response.status_code == 200:
            print(f"[SUCCESS] Admin user created successfully!")
            print(f"[INFO] User ID: {register_response.json().get('user_id', 'N/A')}")
            return True
        else:
            print(f"[ERROR] Registration failed: {register_response.status_code}")
            print(f"[ERROR] Response: {register_response.text[:500]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error: {str(e)}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Matrix Synapse Admin User Creator")
    print("=" * 60)
    print()
    
    # Configuration
    synapse_url = os.getenv('SYNAPSE_URL', 'https://matrix-synapse.up.railway.app')
    username = 'admin'
    password = 'GucluBirSifre123!'
    registration_secret = os.getenv('REGISTRATION_SHARED_SECRET', 'GizliKayitAnahtari123456789')
    
    if len(sys.argv) > 1:
        registration_secret = sys.argv[1]
    
    if len(sys.argv) > 2:
        password = sys.argv[2]
    
    print(f"Synapse URL: {synapse_url}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Registration Secret: {registration_secret[:10]}...")
    print()
    
    success = create_admin_user(synapse_url, username, password, registration_secret)
    
    if success:
        print()
        print("=" * 60)
        print("SUCCESS! Admin user created/reset.")
        print("=" * 60)
        print()
        print("Login bilgileri:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print()
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("FAILED! Could not create/reset admin user.")
        print("=" * 60)
        print()
        sys.exit(1)

