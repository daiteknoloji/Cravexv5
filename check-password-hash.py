#!/usr/bin/env python3
"""
Check password hash format in database for Matrix Synapse compatibility
"""
import os
import psycopg2
import bcrypt

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/synapse')

def check_user_password_hash(username):
    """Check password hash format for a specific user"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Get user password hash
    cur.execute("""
        SELECT name, password_hash, deactivated, creation_ts
        FROM users
        WHERE name = %s
    """, (username,))
    
    result = cur.fetchone()
    if not result:
        print(f"❌ User {username} not found in database")
        return
    
    name, password_hash, deactivated, creation_ts = result
    
    print(f"\n{'='*60}")
    print(f"User: {name}")
    print(f"{'='*60}")
    print(f"Password Hash: {password_hash}")
    print(f"Hash Length: {len(password_hash) if password_hash else 'NULL'}")
    print(f"Hash Type: {type(password_hash)}")
    print(f"Is String: {isinstance(password_hash, str)}")
    print(f"Starts with $2b$12$: {password_hash.startswith('$2b$12$') if password_hash else False}")
    print(f"Deactivated: {deactivated}")
    print(f"Creation TS: {creation_ts}")
    
    # Check if hash is valid bcrypt format
    if password_hash:
        if password_hash.startswith('$2b$12$'):
            print(f"✅ Hash format is correct (bcrypt $2b$12$)")
            
            # Try to verify with a test password
            test_password = input(f"\nEnter password to test (or press Enter to skip): ").strip()
            if test_password:
                try:
                    # Encode password_hash to bytes if it's a string
                    hash_bytes = password_hash.encode('utf-8') if isinstance(password_hash, str) else password_hash
                    is_valid = bcrypt.checkpw(test_password.encode('utf-8'), hash_bytes)
                    print(f"✅ Password verification: {'PASSED' if is_valid else 'FAILED'}")
                except Exception as e:
                    print(f"❌ Password verification error: {e}")
        else:
            print(f"❌ Hash format is incorrect (should start with $2b$12$)")
            print(f"   Current format: {password_hash[:20]}...")
    else:
        print(f"❌ Password hash is NULL")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else '@test1:matrix-synapse.up.railway.app'
    check_user_password_hash(username)

