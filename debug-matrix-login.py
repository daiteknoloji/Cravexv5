#!/usr/bin/env python3
"""
Debug Matrix Synapse login issue
Checks password hash format and compares with Matrix Synapse expectations
"""
import os
import psycopg2
import bcrypt
import requests
import json

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/synapse')
SYNAPSE_URL = os.getenv('SYNAPSE_URL', 'https://matrix-synapse.up.railway.app')
HOMESERVER_DOMAIN = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')

def check_user_in_db(username):
    """Check user details in database"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Get user details
    cur.execute("""
        SELECT 
            name, 
            password_hash, 
            deactivated, 
            creation_ts,
            admin,
            is_guest
        FROM users
        WHERE name = %s
    """, (username,))
    
    result = cur.fetchone()
    if not result:
        print(f"❌ User {username} not found in database")
        cur.close()
        conn.close()
        return None
    
    name, password_hash, deactivated, creation_ts, admin, is_guest = result
    
    print(f"\n{'='*70}")
    print(f"DATABASE CHECK: {name}")
    print(f"{'='*70}")
    print(f"Password Hash: {password_hash}")
    print(f"Hash Length: {len(password_hash) if password_hash else 'NULL'}")
    print(f"Hash Type: {type(password_hash)}")
    print(f"Is String: {isinstance(password_hash, str)}")
    print(f"Starts with $2b$12$: {password_hash.startswith('$2b$12$') if password_hash else False}")
    print(f"Deactivated: {deactivated}")
    print(f"Admin: {admin}")
    print(f"Is Guest: {is_guest}")
    print(f"Creation TS: {creation_ts}")
    
    # Check if hash is valid bcrypt format
    if password_hash:
        if password_hash.startswith('$2b$12$'):
            print(f"✅ Hash format is correct (bcrypt $2b$12$)")
        else:
            print(f"❌ Hash format is incorrect (should start with $2b$12$)")
            print(f"   Current format: {password_hash[:20]}...")
    
    cur.close()
    conn.close()
    
    return {
        'name': name,
        'password_hash': password_hash,
        'deactivated': deactivated,
        'creation_ts': creation_ts
    }

def test_password_with_hash(password, password_hash):
    """Test password against hash"""
    print(f"\n{'='*70}")
    print(f"PASSWORD VERIFICATION TEST")
    print(f"{'='*70}")
    
    try:
        # Encode password_hash to bytes if it's a string
        hash_bytes = password_hash.encode('utf-8') if isinstance(password_hash, str) else password_hash
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hash_bytes)
        print(f"Password: {password}")
        print(f"Hash: {password_hash[:30]}...")
        print(f"Verification: {'✅ PASSED' if is_valid else '❌ FAILED'}")
        return is_valid
    except Exception as e:
        print(f"❌ Password verification error: {e}")
        return False

def test_matrix_api_login(username, password):
    """Test login via Matrix API"""
    print(f"\n{'='*70}")
    print(f"MATRIX API LOGIN TEST")
    print(f"{'='*70}")
    
    # Extract username part (without @ and domain)
    username_part = username.split(':')[0].replace('@', '')
    
    login_url = f"{SYNAPSE_URL}/_matrix/client/v3/login"
    login_data = {
        "type": "m.login.password",
        "identifier": {
            "type": "m.id.user",
            "user": username_part
        },
        "password": password
    }
    
    print(f"Login URL: {login_url}")
    print(f"Username: {username_part}")
    print(f"Full User ID: {username}")
    
    try:
        response = requests.post(login_url, json=login_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login request error: {e}")
        return False

def check_user_directory(username):
    """Check if user exists in user_directory"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT user_id, display_name, avatar_url
        FROM user_directory
        WHERE user_id = %s
    """, (username,))
    
    result = cur.fetchone()
    if result:
        print(f"\n✅ User found in user_directory: {result}")
    else:
        print(f"\n❌ User NOT found in user_directory!")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python debug-matrix-login.py <username> <password>")
        print("Example: python debug-matrix-login.py @test3:matrix-synapse.up.railway.app 12344321")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    # Check database
    user_data = check_user_in_db(username)
    if not user_data:
        sys.exit(1)
    
    # Test password verification
    if user_data['password_hash']:
        test_password_with_hash(password, user_data['password_hash'])
    
    # Check user_directory
    check_user_directory(username)
    
    # Test Matrix API login
    test_matrix_api_login(username, password)

