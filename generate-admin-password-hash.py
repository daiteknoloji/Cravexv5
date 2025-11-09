#!/usr/bin/env python3
"""
Generate bcrypt hash for admin password
"""
import bcrypt

password = "GüçlüBirŞifre123!"
salt = bcrypt.gensalt(rounds=12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

print("=" * 70)
print("ADMIN PASSWORD HASH")
print("=" * 70)
print(f"Password: {password}")
print(f"Hash: {password_hash}")
print("=" * 70)
print("\nSQL UPDATE komutu:")
print(f"UPDATE users SET password_hash = '{password_hash}' WHERE name = '@admin:matrix-synapse.up.railway.app';")
print("\nKontrol SQL:")
print("SELECT name, password_hash, admin, deactivated FROM users WHERE name = '@admin:matrix-synapse.up.railway.app';")
print("=" * 70)

