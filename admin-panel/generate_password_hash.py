#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matrix Synapse Password Hash Generator
======================================
Bu script Matrix Synapse için doğru formatta password hash oluşturur.
"""

import bcrypt
import sys
import os

# Windows terminal encoding sorunu için
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

def generate_password_hash(password):
    """Matrix Synapse için password hash oluştur"""
    # Matrix Synapse bcrypt kullanıyor, rounds=12
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = 'GucluBirSifre123!'
    
    print("=" * 60)
    print("Matrix Synapse Password Hash Generator")
    print("=" * 60)
    print(f"\nPassword: {password}")
    
    hash_value = generate_password_hash(password)
    print(f"\nGenerated Hash:")
    print(hash_value)
    print("\n" + "=" * 60)
    print("\nSQL sorgusunda kullanmak için:")
    print(f"password_hash = '{hash_value}'")
    print("=" * 60)

