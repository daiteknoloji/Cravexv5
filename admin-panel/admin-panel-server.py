#!/usr/bin/env python3
"""
Cravex Admin Panel - Enterprise Edition
========================================
Port: 9000
URL: http://localhost:9000
Login: admin / admin123
"""

from flask import Flask, render_template_string, jsonify, request, send_file, session, redirect, url_for, Response
import psycopg2
from datetime import datetime
import json
import csv
import io
from functools import wraps
import requests

app = Flask(__name__)
app.secret_key = 'cravex-admin-secret-key-2024'

# PostgreSQL bağlantısı - Railway ortam değişkenlerinden
import os

DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'database': os.getenv('PGDATABASE', 'synapse'),
    'user': os.getenv('PGUSER', 'synapse_user'),
    'password': os.getenv('PGPASSWORD', 'SuperGucluSifre2024!'),
    'port': int(os.getenv('PGPORT', '5432'))
}

# Admin kullanıcı bilgileri
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Homeserver domain (Railway or localhost)
HOMESERVER_DOMAIN = os.getenv('HOMESERVER_DOMAIN', 'localhost')
ADMIN_USER_ID = f'@admin:{HOMESERVER_DOMAIN}'

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Media Cache Functions
def init_media_cache_table():
    """Media cache tablosunu oluştur"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS media_cache (
                id SERIAL PRIMARY KEY,
                media_id VARCHAR(255) NOT NULL UNIQUE,
                server_name VARCHAR(255) NOT NULL,
                mxc_url TEXT NOT NULL,
                media_data BYTEA NOT NULL,
                content_type VARCHAR(255),
                file_size BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                sender_user_id VARCHAR(255),
                event_id VARCHAR(255)
            )
        """)
        
        # Index'leri oluştur
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_media_cache_media_id 
            ON media_cache(media_id)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_media_cache_server_name 
            ON media_cache(server_name)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_media_cache_last_accessed 
            ON media_cache(last_accessed)
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("[INFO] Media cache table initialized")
    except Exception as e:
        print(f"[ERROR] Failed to create media_cache table: {e}")

def get_media_from_cache(media_id):
    """Media dosyasını cache'den oku"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT media_data, content_type, file_size, sender_user_id, event_id
            FROM media_cache
            WHERE media_id = %s
        """, (media_id,))
        
        row = cur.fetchone()
        
        if row:
            # Access count ve last_accessed güncelle
            cur.execute("""
                UPDATE media_cache
                SET access_count = access_count + 1,
                    last_accessed = CURRENT_TIMESTAMP
                WHERE media_id = %s
            """, (media_id,))
            conn.commit()
            
            cur.close()
            conn.close()
            
            return {
                'media_data': row[0],  # BYTEA
                'content_type': row[1],
                'file_size': row[2],
                'sender_user_id': row[3],
                'event_id': row[4],
                'cached': True
            }
        
        cur.close()
        conn.close()
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get media from cache: {e}")
        return None

def save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type=None, sender_user_id=None, event_id=None):
    """Media dosyasını cache'e kaydet (tüm dosyalar için - limit kaldırıldı)"""
    MAX_CACHE_SIZE_MB = 100  # 100MB'a kadar dosyalar cache'lenir (limit artırıldı)
    file_size = len(media_data) if isinstance(media_data, bytes) else len(media_data.encode())
    
    # Çok büyük dosyaları cache'leme (100MB üzeri)
    if file_size > MAX_CACHE_SIZE_MB * 1024 * 1024:
        print(f"[INFO] Media too large to cache: {media_id} ({file_size / 1024 / 1024:.2f} MB)")
        return False
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO media_cache 
            (media_id, server_name, mxc_url, media_data, content_type, file_size, sender_user_id, event_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (media_id) 
            DO UPDATE SET
                media_data = EXCLUDED.media_data,
                content_type = EXCLUDED.content_type,
                file_size = EXCLUDED.file_size,
                last_accessed = CURRENT_TIMESTAMP,
                access_count = media_cache.access_count + 1
        """, (media_id, server_name, mxc_url, media_data, content_type, file_size, sender_user_id, event_id))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"[INFO] Media cached: {media_id} ({file_size / 1024:.2f} KB)")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to cache media: {e}")
        return False

# Initialize media cache table on startup
init_media_cache_table()

def auto_cache_media_from_message(media_url, sender, event_id, msgtype=None, thumbnail_url=None):
    """
    Mesajdan medya URL'sini alıp otomatik olarak cache'e kaydet
    
    Args:
        media_url: MXC URL (mxc://server.com/media_id)
        sender: Gönderen kullanıcı ID'si
        event_id: Event ID
        msgtype: Mesaj tipi (m.image, m.file, m.audio, m.video, vb.)
        thumbnail_url: Thumbnail MXC URL (opsiyonel)
    
    Returns:
        bool: Başarılı ise True
    """
    if not media_url or not media_url.startswith('mxc://'):
        return False
    
    try:
        # Parse MXC URL: mxc://server.com/media_id
        mxc_path = media_url.replace('mxc://', '')
        if '/' not in mxc_path:
            return False
        
        server_name, media_id = mxc_path.split('/', 1)
        
        # Cache'de var mı kontrol et
        cached = get_media_from_cache(media_id)
        if cached:
            print(f"[INFO] Media already cached: {media_id}")
            return True
        
        # Matrix Synapse'den indir
        print(f"[INFO] Auto-caching media from message: {media_id} (sender: {sender})")
        
        synapse_url = os.getenv('SYNAPSE_URL', f'https://{server_name}')
        homeserver_domain = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')
        
        # Sender'ın token'ını al
        sender_token = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (sender,)
            )
            token_row = cur.fetchone()
            sender_token = token_row[0] if token_row else None
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[WARN] Could not get sender token for auto-cache: {e}")
        
        # Admin token fallback
        if not sender_token:
            try:
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                admin_password = os.getenv('ADMIN_PASSWORD')
                if admin_password:
                    import requests
                    login_response = requests.post(
                        f'{synapse_url}/_matrix/client/v3/login',
                        json={
                            'type': 'm.login.password',
                            'identifier': {'type': 'm.id.user', 'user': admin_username},
                            'password': admin_password
                        },
                        timeout=5
                    )
                    if login_response.status_code == 200:
                        sender_token = login_response.json().get('access_token')
            except Exception as e:
                print(f"[WARN] Admin auto-login failed for auto-cache: {e}")
        
        # Matrix Synapse'den medya indir
        headers = {
            'User-Agent': 'Cravex-Admin-Panel/1.0',
            'Accept': '*/*'
        }
        if sender_token:
            headers['Authorization'] = f'Bearer {sender_token}'
        
        # Önce Client API v1 dene (Element Web format)
        media_downloaded = False
        media_data = None
        content_type = None
        
        if sender_token:
            client_api_v1_url = f'{synapse_url}/_matrix/client/v1/media/download/{server_name}/{media_id}?allow_redirect=true'
            try:
                import requests
                response = requests.get(client_api_v1_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                if response.status_code == 200:
                    media_data = response.content
                    content_type = response.headers.get('Content-Type', 'application/octet-stream')
                    media_downloaded = True
                    print(f"[INFO] ✅ Auto-cached media via Client API v1: {media_id}")
            except Exception as e:
                print(f"[WARN] Client API v1 failed for auto-cache: {e}")
        
        # Media API v3 dene (Element Web format, no auth)
        if not media_downloaded:
            media_v3_url = f'{synapse_url}/_matrix/media/v3/download/{server_name}/{media_id}?allow_redirect=true'
            try:
                import requests
                media_v3_headers = {'User-Agent': 'Cravex-Admin-Panel/1.0', 'Accept': '*/*'}
                response = requests.get(media_v3_url, stream=True, timeout=30, allow_redirects=True, headers=media_v3_headers)
                if response.status_code == 200:
                    media_data = response.content
                    content_type = response.headers.get('Content-Type', 'application/octet-stream')
                    media_downloaded = True
                    print(f"[INFO] ✅ Auto-cached media via Media API v3: {media_id}")
            except Exception as e:
                print(f"[WARN] Media API v3 failed for auto-cache: {e}")
        
        # Fallback: Media API r0
        if not media_downloaded:
            media_r0_url = f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}'
            try:
                import requests
                response = requests.get(media_r0_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                if response.status_code == 200:
                    media_data = response.content
                    content_type = response.headers.get('Content-Type', 'application/octet-stream')
                    media_downloaded = True
                    print(f"[INFO] ✅ Auto-cached media via Media API r0: {media_id}")
            except Exception as e:
                print(f"[WARN] Media API r0 failed for auto-cache: {e}")
        
        # Cache'e kaydet
        if media_downloaded and media_data:
            success = save_media_to_cache(media_id, server_name, media_url, media_data, content_type, sender, event_id)
            if success:
                print(f"[INFO] ✅ Media auto-cached successfully: {media_id}")
                return True
            else:
                print(f"[WARN] Failed to save media to cache: {media_id}")
                return False
        else:
            print(f"[WARN] Could not download media for auto-cache: {media_id}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Auto-cache media failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login Sayfası HTML
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cravex Admin Panel - Giriş</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f1419;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: #1a1f2e;
            padding: 50px 60px;
            border-radius: 12px;
            border: 1px solid #2a3441;
            width: 100%;
            max-width: 420px;
        }
        .logo {
            text-align: center;
            margin-bottom: 40px;
        }
        .logo h1 {
            color: #ffffff;
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        .logo p {
            color: #8b92a0;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 24px;
        }
        .form-group label {
            display: block;
            color: #c4c9d4;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 8px;
        }
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #2a3441;
            border-radius: 6px;
            font-size: 15px;
            transition: all 0.2s;
            background: #0f1419;
            color: #ffffff;
        }
        .form-group input:focus {
            outline: none;
            border-color: #4a90e2;
            background: #1a1f2e;
        }
        .login-btn {
            width: 100%;
            padding: 14px;
            background: #4a90e2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .login-btn:hover {
            background: #3a7bc8;
        }
        .error {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 14px;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #64748b;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1><i class="fas fa-shield-alt"></i> Cravex Admin</h1>
            <p>Admin Panel</p>
        </div>
        
        {% if error %}
        <div class="error"><i class="fas fa-exclamation-circle"></i> {{ error }}</div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username" required autofocus placeholder="admin">
            </div>
            
            <div class="form-group">
                <label>Şifre</label>
                <input type="password" name="password" required placeholder="••••••••">
            </div>
            
            <button type="submit" class="login-btn">Giriş Yap</button>
        </form>
        
        <div class="footer">
            © 2024 Cravex Communication
        </div>
    </div>
</body>
</html>
'''

# Ana Dashboard HTML (Minimal Tasarım + Pagination)
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cravex Admin Panel</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f1419;
            color: #e4e6eb;
        }
        
        /* Header */
        .header {
            background: #1a1f2e;
            border-bottom: 1px solid #2a3441;
            padding: 0 32px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-left { display: flex; align-items: center; gap: 16px; }
        .header h1 { 
            font-size: 20px; 
            font-weight: 600; 
            color: #ffffff;
            letter-spacing: -0.3px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header h1 i {
            font-size: 48px;
            color: #4a90e2;
        }
        .header-right { display: flex; align-items: center; gap: 16px; }
        .user-info {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 6px 14px;
            background: rgba(255,255,255,0.05);
            border-radius: 6px;
            border: 1px solid #2a3441;
        }
        .user-avatar {
            width: 28px;
            height: 28px;
            background: #4a90e2;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 12px;
        }
        .user-name { font-size: 13px; color: #c4c9d4; }
        .logout-btn {
            padding: 6px 14px;
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .logout-btn:hover { background: rgba(239, 68, 68, 0.15); }
        
        /* Container */
        .container { max-width: 1600px; margin: 0 auto; padding: 32px; }
        
        /* Stats Cards */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        .stat-card {
            background: #1a1f2e;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #2a3441;
        }
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .stat-icon {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            background: rgba(255,255,255,0.05);
            color: #8b92a0;
        }
        .stat-label { 
            font-size: 12px; 
            color: #8b92a0; 
            font-weight: 500;
            margin-bottom: 8px;
        }
        .stat-value { 
            font-size: 28px; 
            font-weight: 600; 
            color: #ffffff;
        }
        
        /* Filters */
        .filters-card {
            background: #1a1f2e;
            padding: 24px;
            border-radius: 8px;
            border: 1px solid #2a3441;
            margin-bottom: 20px;
        }
        .filters-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .filters-header h2 { 
            font-size: 16px; 
            font-weight: 600;
            color: #ffffff;
        }
        .filter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }
        .filter-group label {
            display: block;
            color: #8b92a0;
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 6px;
        }
        .filter-group input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #2a3441;
            border-radius: 6px;
            font-size: 13px;
            background: #0f1419;
            color: #ffffff;
            transition: all 0.2s;
        }
        .filter-group input:focus {
            outline: none;
            border-color: #4a90e2;
        }
        .filter-group input::placeholder {
            color: #64748b;
        }
        
        /* Buttons */
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        button {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn-primary { 
            background: #4a90e2; 
            color: white;
        }
        .btn-primary:hover { background: #3a7bc8; }
        .btn-secondary { 
            background: rgba(255,255,255,0.05);
            color: #c4c9d4;
            border: 1px solid #2a3441;
        }
        .btn-secondary:hover { background: rgba(255,255,255,0.08); }
        button:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }
        
        /* Messages Table */
        .messages-card {
            background: #1a1f2e;
            border-radius: 8px;
            border: 1px solid #2a3441;
            overflow: hidden;
        }
        .messages-header {
            padding: 20px 24px;
            border-bottom: 1px solid #2a3441;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .messages-header h2 { 
            font-size: 16px; 
            font-weight: 600;
            color: #ffffff;
        }
        .messages-body { padding: 0; }
        
        /* Pagination */
        .pagination {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .pagination-info {
            font-size: 13px;
            color: #8b92a0;
            padding: 0 12px;
        }
        .pagination-info strong {
            color: #ffffff;
        }
        .page-btn {
            padding: 6px 12px;
            background: rgba(255,255,255,0.05);
            color: #c4c9d4;
            border: 1px solid #2a3441;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .page-btn:hover:not(:disabled) {
            background: rgba(255,255,255,0.08);
        }
        .page-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        table { width: 100%; border-collapse: collapse; }
        thead { 
            background: rgba(255,255,255,0.02);
            border-bottom: 1px solid #2a3441;
        }
        th { 
            padding: 12px 20px; 
            text-align: left; 
            font-size: 11px;
            font-weight: 600;
            color: #8b92a0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        td { 
            padding: 14px 20px; 
            border-bottom: 1px solid #2a3441;
            font-size: 13px;
            color: #c4c9d4;
        }
        tr:hover { background: rgba(255,255,255,0.02); }
        .sender { 
            color: #4a90e2; 
            font-weight: 500;
            font-family: 'Courier New', monospace;
        }
        .timestamp { 
            color: #8b92a0; 
            font-size: 12px;
        }
        .room-name { 
            color: #8b92a0;
        }
        .recipient {
            color: #10b981;
            font-weight: 500;
            font-family: 'Courier New', monospace;
        }
        .recipient-group {
            color: #10b981;
            font-weight: 500;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            position: relative;
            text-decoration: underline dotted;
        }
        .recipient-group:hover {
            color: #059669;
        }
        
        /* Tooltip */
        .tooltip {
            position: absolute;
            background: #1a1f2e;
            border: 1px solid #4a90e2;
            border-radius: 8px;
            padding: 12px 16px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            min-width: 200px;
            max-width: 400px;
            display: none;
            pointer-events: none;
        }
        .tooltip.show {
            display: block;
        }
        .tooltip-title {
            font-size: 11px;
            color: #8b92a0;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .tooltip-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .tooltip-list li {
            padding: 4px 0;
            color: #e4e6eb;
            font-size: 13px;
            font-family: 'Courier New', monospace;
        }
        .tooltip-list li:before {
            content: "• ";
            color: #4a90e2;
            margin-right: 6px;
        }
        .message-text {
            color: #e4e6eb;
            max-width: 500px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .loading {
            text-align: center;
            padding: 60px 40px;
            color: #64748b;
            font-size: 14px;
        }
        .empty-state {
            text-align: center;
            padding: 60px 40px;
        }
        .empty-state-icon {
            font-size: 48px;
            margin-bottom: 12px;
            opacity: 0.2;
        }
        .empty-state-text {
            font-size: 14px;
            color: #8b92a0;
        }
        .result-count {
            font-size: 13px;
            color: #8b92a0;
            margin-bottom: 16px;
            padding: 0 24px;
        }
        .result-count strong {
            color: #ffffff;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <div class="header-left">
            <h1><i class="fas fa-shield-alt"></i> Cravex Admin Panel</h1>
        </div>
        <div class="header-right">
            <div class="user-info">
                <div class="user-avatar">A</div>
                <span class="user-name">Administrator</span>
            </div>
            <form action="/logout" method="POST" style="margin: 0;">
                <button type="submit" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Çıkış</button>
            </form>
        </div>
    </div>
    
    <!-- Main Content -->
    <div class="container">
        <!-- Stats -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">TOPLAM MESAJ</div>
                <div class="stat-value" id="totalMessages">0</div>
                <div class="stat-icon"><i class="fas fa-comments"></i></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">TOPLAM ODA</div>
                <div class="stat-value" id="totalRooms">0</div>
                <div class="stat-icon"><i class="fas fa-door-open"></i></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">AKTİF KULLANICI</div>
                <div class="stat-value" id="totalUsers">0</div>
                <div class="stat-icon"><i class="fas fa-users"></i></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">ŞİFRESİZ</div>
                <div class="stat-value">100%</div>
                <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
            </div>
        </div>
        
        <!-- Filters -->
        <div class="filters-card">
            <div class="filters-header">
                <h2><i class="fas fa-filter"></i> Arama Filtreleri</h2>
            </div>
            
            <div class="filter-grid">
                <div class="filter-group">
                    <label>Oda ID</label>
                    <input type="text" id="filterRoomId" placeholder="!abc:localhost">
                </div>
                <div class="filter-group">
                    <label>Gönderen (Kullanıcı Adı)</label>
                    <input type="text" id="filterSender" placeholder="@kullanici:localhost">
                </div>
                <div class="filter-group">
                    <label>Mesaj İçeriğinde Ara</label>
                    <input type="text" id="searchQuery" placeholder="Kelime ara...">
                </div>
            </div>
            
            <div class="btn-group">
                <button class="btn-primary" onclick="searchMessages()">
                    <i class="fas fa-search"></i> Ara
                </button>
                <button class="btn-secondary" onclick="exportData('json')">
                    <i class="fas fa-download"></i> JSON
                </button>
                <button class="btn-secondary" onclick="exportData('csv')">
                    <i class="fas fa-file-csv"></i> CSV
                </button>
                <button class="btn-secondary" onclick="clearFilters()">
                    <i class="fas fa-redo"></i> Temizle
                </button>
            </div>
        </div>
        
        <!-- Messages -->
        <div class="messages-card">
            <div class="messages-header">
                <h2><i class="fas fa-list"></i> Mesajlar</h2>
                <div class="pagination" id="paginationTop" style="display: none;">
                    <button class="page-btn" onclick="previousPage()" id="prevBtnTop">
                        <i class="fas fa-chevron-left"></i> Önceki
                    </button>
                    <div class="pagination-info">
                        Sayfa <strong id="currentPageTop">1</strong> / <strong id="totalPagesTop">1</strong>
                    </div>
                    <button class="page-btn" onclick="nextPage()" id="nextBtnTop">
                        İleri <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
            <div class="messages-body">
                <div id="messagesContent">
                    <div class="empty-state">
                        <div class="empty-state-icon"><i class="fas fa-inbox"></i></div>
                        <div class="empty-state-text">Mesajları görüntülemek için filtreleri kullanın ve "Ara" butonuna tıklayın</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentPage = 1;
        let totalPages = 1;
        let totalMessages = 0;
        const pageSize = 50;
        
        // Sayfa yüklenince stats'ı yükle
        loadStats();
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('totalMessages').textContent = stats.total_messages.toLocaleString();
                document.getElementById('totalRooms').textContent = stats.total_rooms.toLocaleString();
                document.getElementById('totalUsers').textContent = stats.total_users.toLocaleString();
            } catch (error) {
                console.error('Stats yüklenirken hata:', error);
            }
        }
        
        function searchMessages() {
            currentPage = 1;
            loadMessages();
        }
        
        async function loadMessages() {
            const content = document.getElementById('messagesContent');
            content.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Mesajlar yükleniyor...</div>';
            
            const params = new URLSearchParams({
                room_id: document.getElementById('filterRoomId').value,
                sender: document.getElementById('filterSender').value,
                search: document.getElementById('searchQuery').value,
                page: currentPage,
                page_size: pageSize
            });
            
            try {
                const response = await fetch('/api/messages?' + params);
                const data = await response.json();
                
                if (data.error) {
                    content.innerHTML = '<div class="loading"><i class="fas fa-exclamation-circle"></i> Hata: ' + data.error + '</div>';
                    return;
                }
                
                totalMessages = data.total;
                totalPages = Math.ceil(totalMessages / pageSize);
                
                updatePagination();
                
                if (data.messages.length === 0) {
                    content.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon"><i class="fas fa-search"></i></div>
                            <div class="empty-state-text">Arama kriterlerinize uygun mesaj bulunamadı</div>
                        </div>
                    `;
                    return;
                }
                
                const start = (currentPage - 1) * pageSize + 1;
                const end = Math.min(start + data.messages.length - 1, totalMessages);
                
                let html = `
                    <div class="result-count">
                        Toplam <strong>${totalMessages.toLocaleString()}</strong> mesajdan 
                        <strong>${start.toLocaleString()}</strong> - <strong>${end.toLocaleString()}</strong> arası gösteriliyor
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 130px;">TARİH/SAAT</th>
                                <th style="width: 200px;">GÖNDEREN</th>
                                <th style="width: 150px;">GİTTİĞİ ODA</th>
                                <th style="width: 200px;">ALICI</th>
                                <th>MESAJ</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                data.messages.forEach(msg => {
                    let recipientCell = '';
                    if (msg.recipient_list && msg.recipient_list.length > 0) {
                        // Grup mesajı - tooltip ile göster
                        const recipientListJSON = JSON.stringify(msg.recipient_list).replace(/"/g, '&quot;');
                        recipientCell = `<span class="recipient-group" data-recipients='${recipientListJSON}'>${msg.recipient || 'Grup'}</span>`;
                    } else {
                        // Tekil alıcı
                        recipientCell = `<span class="recipient">${msg.recipient || 'Grup'}</span>`;
                    }
                    
                    html += `
                        <tr>
                            <td class="timestamp">${msg.timestamp}</td>
                            <td class="sender">${msg.sender}</td>
                            <td class="room-name">${msg.room_name || msg.room_id}</td>
                            <td>${recipientCell}</td>
                            <td class="message-text" title="${msg.message || ''}">${msg.message || '<em>Boş mesaj</em>'}</td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                content.innerHTML = html;
                
            } catch (error) {
                content.innerHTML = '<div class="loading"><i class="fas fa-times-circle"></i> Bağlantı hatası: ' + error.message + '</div>';
            }
        }
        
        function updatePagination() {
            const paginationTop = document.getElementById('paginationTop');
            
            if (totalPages > 1) {
                paginationTop.style.display = 'flex';
                
                // Update page numbers
                document.getElementById('currentPageTop').textContent = currentPage;
                document.getElementById('totalPagesTop').textContent = totalPages;
                
                // Update button states
                document.getElementById('prevBtnTop').disabled = currentPage === 1;
                document.getElementById('nextBtnTop').disabled = currentPage === totalPages;
            } else {
                paginationTop.style.display = 'none';
            }
        }
        
        function nextPage() {
            if (currentPage < totalPages) {
                currentPage++;
                loadMessages();
                window.scrollTo(0, 0);
            }
        }
        
        function previousPage() {
            if (currentPage > 1) {
                currentPage--;
                loadMessages();
                window.scrollTo(0, 0);
            }
        }
        
        async function exportData(format) {
            const params = new URLSearchParams({
                room_id: document.getElementById('filterRoomId').value,
                sender: document.getElementById('filterSender').value,
                search: document.getElementById('searchQuery').value,
                format: format
            });
            
            window.location.href = '/api/export?' + params;
        }
        
        function clearFilters() {
            document.getElementById('filterRoomId').value = '';
            document.getElementById('filterSender').value = '';
            document.getElementById('searchQuery').value = '';
            
            currentPage = 1;
            totalPages = 1;
            
            document.getElementById('messagesContent').innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon"><i class="fas fa-inbox"></i></div>
                    <div class="empty-state-text">Mesajları görüntülemek için filtreleri kullanın ve "Ara" butonuna tıklayın</div>
                </div>
            `;
            
            document.getElementById('paginationTop').style.display = 'none';
        }
        
        // Enter tuşuyla arama
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    searchMessages();
                }
            });
        });
        
        // Tooltip functionality
        let tooltip = null;
        
        function createTooltip() {
            if (!tooltip) {
                tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                document.body.appendChild(tooltip);
            }
            return tooltip;
        }
        
        function showTooltip(element, recipients) {
            const tooltip = createTooltip();
            
            let html = '<div class="tooltip-title">Grup Üyeleri</div>';
            html += '<ul class="tooltip-list">';
            recipients.forEach(recipient => {
                html += `<li>${recipient}</li>`;
            });
            html += '</ul>';
            
            tooltip.innerHTML = html;
            tooltip.classList.add('show');
            
            // Position tooltip
            const rect = element.getBoundingClientRect();
            tooltip.style.position = 'fixed';
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.bottom + 5) + 'px';
        }
        
        function hideTooltip() {
            if (tooltip) {
                tooltip.classList.remove('show');
            }
        }
        
        // Event delegation for dynamically added elements
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('recipient-group')) {
                try {
                    const recipients = JSON.parse(e.target.getAttribute('data-recipients'));
                    showTooltip(e.target, recipients);
                } catch (error) {
                    console.error('Error parsing recipients:', error);
                }
            }
        });
        
        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('recipient-group')) {
                hideTooltip();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error='Kullanıcı adı veya şifre hatalı!')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Serve the modern UI
    try:
        with open('admin-panel-ui-modern.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Fallback to old template
        return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (logo, etc.)"""
    import os
    static_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(static_dir, filename)
    print(f"[DEBUG] Static file request: {filename}")
    print(f"[DEBUG] Looking for: {file_path}")
    print(f"[DEBUG] Exists: {os.path.exists(file_path)}")
    if os.path.exists(file_path):
        return send_file(file_path)
    return f"File not found: {file_path}", 404

@app.route('/api/stats')
@login_required
def get_stats():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM events WHERE type = 'm.room.message'")
        total_messages = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM rooms")
        total_rooms = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT sender) FROM events WHERE type = 'm.room.message'")
        total_users = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'total_messages': total_messages,
            'total_rooms': total_rooms,
            'total_users': total_users
        })
    except Exception as e:
        print(f"[HATA] /api/stats - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages')
@login_required
def get_messages():
    try:
        room_id = request.args.get('room_id', '').strip()
        sender = request.args.get('sender', '').strip()
        receiver = request.args.get('receiver', '').strip()
        search = request.args.get('search', '').strip()
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 50))
        
        offset = (page - 1) * page_size
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        conditions = ["e.type = 'm.room.message'"]
        
        if room_id:
            # Search both in room_id and room_name
            conditions.append(f"""
                (e.room_id ILIKE {cur.mogrify('%s', (f'%{room_id}%',)).decode('utf-8')}
                 OR EXISTS (
                    SELECT 1 FROM event_json ej_name
                    WHERE ej_name.room_id = e.room_id
                      AND ej_name.json::json->>'type' = 'm.room.name'
                      AND ej_name.json::json->'content'->>'name' ILIKE {cur.mogrify('%s', (f'%{room_id}%',)).decode('utf-8')}
                 ))
            """)
        if sender:
            conditions.append(cur.mogrify("e.sender ILIKE %s", (f'%{sender}%',)).decode('utf-8'))
        if receiver:
            # Filter by recipient (member in room)
            conditions.append(f"""
                EXISTS (
                    SELECT 1 FROM room_memberships rm
                    WHERE rm.room_id = e.room_id
                      AND rm.user_id ILIKE {cur.mogrify('%s', (f'%{receiver}%',)).decode('utf-8')}
                      AND rm.user_id != e.sender
                      AND rm.membership = 'join'
                )
            """)
        if search:
            conditions.append(cur.mogrify("ej.json::json->'content'->>'body' ILIKE %s", (f'%{search}%',)).decode('utf-8'))
        if start_date:
            # Convert datetime-local to timestamp (milliseconds)
            from datetime import datetime
            start_ts = int(datetime.fromisoformat(start_date).timestamp() * 1000)
            conditions.append(cur.mogrify("e.origin_server_ts >= %s", (start_ts,)).decode('utf-8'))
        if end_date:
            from datetime import datetime
            end_ts = int(datetime.fromisoformat(end_date).timestamp() * 1000)
            conditions.append(cur.mogrify("e.origin_server_ts <= %s", (end_ts,)).decode('utf-8'))
        
        where_clause = " AND ".join(conditions)
        
        # Toplam mesaj sayısını al
        count_query = f"""
            SELECT COUNT(*)
            FROM events e
            JOIN event_json ej ON e.event_id = ej.event_id
            WHERE {where_clause}
        """
        cur.execute(count_query)
        total = cur.fetchone()[0]
        
        # Sayfalı mesajları al (silinen mesajlar dahil)
        query = f"""
            SELECT 
                to_timestamp(e.origin_server_ts/1000) as timestamp,
                e.sender,
                e.room_id,
                (SELECT ej2.json::json->'content'->>'name' 
                 FROM event_json ej2
                 WHERE ej2.room_id = e.room_id 
                   AND ej2.json::json->>'type' = 'm.room.name'
                 ORDER BY (ej2.json::json->>'origin_server_ts')::bigint DESC
                 LIMIT 1) as room_name,
                ej.json::json->'content'->>'body' as message,
                ej.json::json->'content'->>'msgtype' as msgtype,
                ej.json::json->'content'->>'url' as media_url,
                ej.json::json->'content'->'info'->>'mimetype' as mimetype,
                ej.json::json->'content'->'info'->>'size' as file_size,
                ej.json::json->'content'->'info'->>'w' as image_width,
                ej.json::json->'content'->'info'->>'h' as image_height,
                ej.json::json->'content'->'info'->>'thumbnail_url' as thumbnail_url,
                (SELECT STRING_AGG(DISTINCT rm.user_id, ', ')
                 FROM room_memberships rm
                 WHERE rm.room_id = e.room_id
                   AND rm.user_id != e.sender
                   AND rm.membership = 'join') as recipients,
                -- Check if deleted
                (SELECT er.sender 
                 FROM redactions r
                 JOIN events er ON r.event_id = er.event_id
                 WHERE r.redacts = e.event_id 
                 LIMIT 1) as redacted_by,
                e.event_id
            FROM events e
            JOIN event_json ej ON e.event_id = ej.event_id
            WHERE {where_clause}
            ORDER BY e.origin_server_ts DESC
            LIMIT {page_size} OFFSET {offset};
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        messages = []
        for row in rows:
            # Row structure: timestamp(0), sender(1), room_id(2), room_name(3), message(4), 
            # msgtype(5), media_url(6), mimetype(7), file_size(8), image_width(9), image_height(10), 
            # thumbnail_url(11), recipients(12), redacted_by(13), event_id(14)
            recipients = row[12] if len(row) > 12 and row[12] else ''
            is_deleted = row[13] is not None if len(row) > 13 else False  # redacted_by exists
            room_name = row[3]
            room_id = row[2]
            sender = row[1]
            
            # Extract media/file information
            msgtype = row[5] if len(row) > 5 else None
            media_url = row[6] if len(row) > 6 else None
            mimetype = row[7] if len(row) > 7 else None
            file_size = row[8] if len(row) > 8 else None
            image_width = row[9] if len(row) > 9 else None
            image_height = row[10] if len(row) > 10 else None
            thumbnail_url = row[11] if len(row) > 11 else None
            
            # Eğer tek alıcı varsa direkt göster, birden fazlaysa sayı göster
            if recipients:
                recipient_list = recipients.split(', ')
                if len(recipient_list) == 1:
                    recipient_display = recipient_list[0]
                    recipient_full_list = None
                else:
                    recipient_display = f'Grup ({len(recipient_list)} kişi)'
                    recipient_full_list = recipient_list
            else:
                recipient_display = 'Grup'
                recipient_full_list = None
            
            # DM room naming logic
            if not room_name:
                # Get all members in the room
                cur.execute("""
                    SELECT user_id 
                    FROM room_memberships 
                    WHERE room_id = %s AND membership = 'join'
                    ORDER BY user_id
                """, (room_id,))
                members = [m[0] for m in cur.fetchall()]
                
                if len(members) == 2:
                    # It's a DM - show member names
                    member_names = []
                    for member_id in members:
                        cur.execute("SELECT displayname FROM profiles WHERE user_id = %s LIMIT 1", (member_id,))
                        display_row = cur.fetchone()
                        display_name = display_row[0] if display_row and display_row[0] else member_id
                        member_names.append(display_name)
                    
                    room_name = f'DM: {member_names[0]} ↔ {member_names[1]}'
                elif len(members) > 2:
                    room_name = f'Grup Chat ({len(members)} kişi)'
                else:
                    room_name = 'İsimsiz oda'
            
            # Convert MXC URL to HTTP URL if needed
            # MXC format: mxc://server.com/media_id
            # HTTP format: https://server.com/_matrix/media/r0/download/server.com/media_id
            media_http_url = None
            thumbnail_http_url = None
            homeserver_domain = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')
            synapse_url = os.getenv('SYNAPSE_URL', f'https://{homeserver_domain}')
            
            def mxc_to_http(mxc_url, use_thumbnail=False):
                """Convert MXC URL to HTTP URL (via proxy)"""
                if not mxc_url or not mxc_url.startswith('mxc://'):
                    return None
                
                # Parse mxc://server.com/media_id
                mxc_path = mxc_url.replace('mxc://', '')
                if '/' not in mxc_path:
                    return None
                
                server_name, media_id = mxc_path.split('/', 1)
                
                # Use proxy endpoint to avoid CORS and authentication issues
                if use_thumbnail:
                    # Thumbnail endpoint with size parameters (via proxy)
                    return f'/api/media/thumbnail/{server_name}/{media_id}?width=800&height=600&method=scale'
                else:
                    # Download endpoint (via proxy)
                    return f'/api/media/download/{server_name}/{media_id}'
            
            if media_url:
                media_http_url = mxc_to_http(media_url, use_thumbnail=False)
            
            if thumbnail_url:
                thumbnail_http_url = mxc_to_http(thumbnail_url, use_thumbnail=True)
            elif media_url:
                # If no thumbnail_url but we have media_url, use thumbnail endpoint for images
                if msgtype == 'm.image':
                    thumbnail_http_url = mxc_to_http(media_url, use_thumbnail=True)
            
            # Debug: Log MXC URL information
            if media_url:
                print(f"[DEBUG] Message {row[14]}: MXC URL = {media_url}, Parsed HTTP URL = {media_http_url}")
            
            # Otomatik medya cache'leme: Mesajları okurken medya dosyalarını otomatik olarak cache'e kaydet
            if media_url and sender and row[14]:  # media_url, sender, event_id varsa
                try:
                    # Background'da cache'le (blocking olmaması için)
                    auto_cache_media_from_message(media_url, sender, row[14], msgtype, thumbnail_url)
                except Exception as cache_err:
                    print(f"[WARN] Auto-cache failed for message {row[14]}: {cache_err}")
            
            # Get sender's access token for media access (if available)
            sender_token = None
            if sender and media_url:
                try:
                    conn_token = get_db_connection()
                    cur_token = conn_token.cursor()
                    cur_token.execute(
                        "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                        (sender,)
                    )
                    token_row = cur_token.fetchone()
                    sender_token = token_row[0] if token_row else None
                    cur_token.close()
                    conn_token.close()
                    if sender_token:
                        print(f"[DEBUG] Found token for sender {sender}: {sender_token[:20]}...")
                except Exception as token_err:
                    print(f"[DEBUG] Could not get sender token: {token_err}")
            
            messages.append({
                'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S') if row[0] else '',
                'sender': sender,
                'room_id': room_id,
                'room_name': room_name,
                'message': row[4],
                'msgtype': msgtype,
                'media_url': media_url,  # Original MXC URL
                'media_http_url': media_http_url,  # Parsed proxy URL
                'thumbnail_url': thumbnail_url,  # Original MXC thumbnail URL
                'thumbnail_http_url': thumbnail_http_url,  # Parsed proxy thumbnail URL
                'mimetype': mimetype,
                'file_size': int(file_size) if file_size else None,
                'image_width': int(image_width) if image_width else None,
                'image_height': int(image_height) if image_height else None,
                'recipient': recipient_display,
                'recipient_list': recipient_full_list,
                'is_deleted': is_deleted,
                'deleted_by': row[13] if is_deleted else None,
                'event_id': row[14],
                'sender_token_available': sender_token is not None,  # For debugging
                # Debug info
                'debug': {
                    'mxc_url': media_url,
                    'parsed_server_name': media_url.split('/')[2] if media_url and '/' in media_url.replace('mxc://', '') else None,
                    'parsed_media_id': media_url.split('/')[-1] if media_url and '/' in media_url.replace('mxc://', '') else None
                } if media_url else None
            })
        
        cur.close()
        conn.close()
        
        return jsonify({
            'messages': messages,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    except Exception as e:
        print(f"[HATA] /api/messages - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ============================================
# ROOM MANAGEMENT API ENDPOINTS
# ============================================

@app.route('/api/rooms')
@login_required
def get_rooms():
    """Get all rooms with stats"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT 
                r.room_id,
                (SELECT ej.json::json->'content'->>'name' 
                 FROM event_json ej
                 WHERE ej.room_id = r.room_id 
                   AND ej.json::json->>'type' = 'm.room.name'
                 ORDER BY (ej.json::json->>'origin_server_ts')::bigint DESC
                 LIMIT 1) as room_name,
                r.creator,
                r.is_public,
                (SELECT COUNT(*) FROM room_memberships 
                 WHERE room_id = r.room_id AND membership = 'join') as member_count,
                (SELECT COUNT(*) FROM events 
                 WHERE room_id = r.room_id AND type = 'm.room.message') as message_count,
                -- Get members for DM detection
                (SELECT STRING_AGG(user_id, '|||')
                 FROM room_memberships
                 WHERE room_id = r.room_id AND membership = 'join'
                 LIMIT 10) as members_list
            FROM rooms r
            ORDER BY member_count DESC;
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        rooms = []
        for row in rows:
            room_name = row[1]
            members_list = row[6]
            member_count = row[4] or 0
            
            # If no name and 2 members, it's a DM - show member names
            if not room_name and member_count == 2 and members_list:
                members = members_list.split('|||')
                # Get displaynames for members
                member_names = []
                for member in members[:2]:
                    cur.execute("SELECT displayname FROM profiles WHERE user_id = %s LIMIT 1", (member,))
                    display_row = cur.fetchone()
                    display_name = display_row[0] if display_row and display_row[0] else member
                    member_names.append(display_name)
                
                if len(member_names) == 2:
                    room_name = f'DM: {member_names[0]} ↔ {member_names[1]}'
                else:
                    room_name = 'DM (2 kişi)'
            elif not room_name and member_count > 2:
                room_name = f'Grup Chat ({member_count} kişi)'
            elif not room_name:
                room_name = 'İsimsiz Oda'
            
            rooms.append({
                'room_id': row[0],
                'name': room_name,
                'creator': row[2],
                'is_public': row[3],
                'member_count': member_count,
                'message_count': row[5] or 0,
                'is_dm': (not row[1] and member_count == 2)  # DM indicator
            })
        
        cur.close()
        conn.close()
        
        return jsonify({'rooms': rooms, 'total': len(rooms)})
        
    except Exception as e:
        print(f"[HATA] /api/rooms - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<room_id>/members')
@login_required
def get_room_members(room_id):
    """Get members of a specific room"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT DISTINCT
                rm.user_id,
                rm.membership,
                (SELECT displayname FROM profiles 
                 WHERE user_id = rm.user_id LIMIT 1) as displayname
            FROM room_memberships rm
            WHERE rm.room_id = %s AND rm.membership = 'join'
            ORDER BY rm.user_id;
        """
        
        cur.execute(query, (room_id,))
        rows = cur.fetchall()
        
        members = []
        for row in rows:
            members.append({
                'user_id': row[0],
                'membership': row[1],
                'displayname': row[2]
            })
        
        cur.close()
        conn.close()
        
        return jsonify({'members': members, 'total': len(members)})
        
    except Exception as e:
        print(f"[HATA] /api/rooms/{room_id}/members - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<room_id>/messages')
@login_required
def get_room_messages(room_id):
    """Get messages from a specific room"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 50))
        offset = (page - 1) * page_size
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Count total messages
        count_query = """
            SELECT COUNT(*)
            FROM events e
            WHERE e.room_id = %s AND e.type = 'm.room.message'
        """
        cur.execute(count_query, (room_id,))
        total = cur.fetchone()[0]
        
        # Get paginated messages with redaction info and media
        query = """
            SELECT 
                to_timestamp(e.origin_server_ts/1000) as timestamp,
                e.sender,
                ej.json::json->'content'->>'body' as message,
                ej.json::json->'content'->>'msgtype' as msgtype,
                ej.json::json->'content'->>'url' as media_url,
                ej.json::json->'content'->'info'->>'mimetype' as mimetype,
                ej.json::json->'content'->'info'->>'size' as file_size,
                ej.json::json->'content'->'info'->>'w' as image_width,
                ej.json::json->'content'->'info'->>'h' as image_height,
                ej.json::json->'content'->'info'->>'thumbnail_url' as thumbnail_url,
                e.event_id,
                -- Check if message was deleted using redactions table
                (SELECT er.sender 
                 FROM redactions r
                 JOIN events er ON r.event_id = er.event_id
                 WHERE r.redacts = e.event_id 
                 LIMIT 1) as redacted_by,
                (SELECT to_timestamp(er.origin_server_ts/1000)
                 FROM redactions r
                 JOIN events er ON r.event_id = er.event_id
                 WHERE r.redacts = e.event_id 
                 LIMIT 1) as redacted_at
            FROM events e
            JOIN event_json ej ON e.event_id = ej.event_id
            WHERE e.room_id = %s AND e.type = 'm.room.message'
            ORDER BY e.origin_server_ts DESC
            LIMIT %s OFFSET %s;
        """
        
        cur.execute(query, (room_id, page_size, offset))
        rows = cur.fetchall()
        
        messages = []
        for row in rows:
            is_deleted = row[11] is not None  # redacted_by exists
            
            # Extract media/file information
            msgtype = row[3] if len(row) > 3 else None
            media_url = row[4] if len(row) > 4 else None
            mimetype = row[5] if len(row) > 5 else None
            file_size = row[6] if len(row) > 6 else None
            image_width = row[7] if len(row) > 7 else None
            image_height = row[8] if len(row) > 8 else None
            thumbnail_url = row[9] if len(row) > 9 else None
            
            # Convert MXC URL to HTTP URL if needed
            # MXC format: mxc://server.com/media_id
            # HTTP format: https://server.com/_matrix/media/r0/download/server.com/media_id
            media_http_url = None
            thumbnail_http_url = None
            homeserver_domain = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')
            synapse_url = os.getenv('SYNAPSE_URL', f'https://{homeserver_domain}')
            
            def mxc_to_http(mxc_url, use_thumbnail=False):
                """Convert MXC URL to HTTP URL (via proxy)"""
                if not mxc_url or not mxc_url.startswith('mxc://'):
                    return None
                
                # Parse mxc://server.com/media_id
                mxc_path = mxc_url.replace('mxc://', '')
                if '/' not in mxc_path:
                    return None
                
                server_name, media_id = mxc_path.split('/', 1)
                
                # Use proxy endpoint to avoid CORS and authentication issues
                if use_thumbnail:
                    # Thumbnail endpoint with size parameters (via proxy)
                    return f'/api/media/thumbnail/{server_name}/{media_id}?width=800&height=600&method=scale'
                else:
                    # Download endpoint (via proxy)
                    return f'/api/media/download/{server_name}/{media_id}'
            
            if media_url:
                media_http_url = mxc_to_http(media_url, use_thumbnail=False)
            
            if thumbnail_url:
                thumbnail_http_url = mxc_to_http(thumbnail_url, use_thumbnail=True)
            elif media_url:
                # If no thumbnail_url but we have media_url, use thumbnail endpoint for images
                if msgtype == 'm.image':
                    thumbnail_http_url = mxc_to_http(media_url, use_thumbnail=True)
            
            # Otomatik medya cache'leme: Mesajları okurken medya dosyalarını otomatik olarak cache'e kaydet
            if media_url and row[1] and row[10]:  # media_url, sender, event_id varsa
                try:
                    # Background'da cache'le (blocking olmaması için)
                    auto_cache_media_from_message(media_url, row[1], row[10], msgtype, thumbnail_url)
                except Exception as cache_err:
                    print(f"[WARN] Auto-cache failed for message {row[10]}: {cache_err}")
            
            messages.append({
                'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S') if row[0] else '',
                'sender': row[1],
                'message': row[2] or '',
                'msgtype': msgtype or 'm.text',
                'media_url': media_url,
                'media_http_url': media_http_url,
                'thumbnail_url': thumbnail_url,
                'thumbnail_http_url': thumbnail_http_url,
                'mimetype': mimetype,
                'file_size': int(file_size) if file_size else None,
                'image_width': int(image_width) if image_width else None,
                'image_height': int(image_height) if image_height else None,
                'event_id': row[10],
                'is_deleted': is_deleted,
                'deleted_by': row[11] if is_deleted else None,
                'deleted_at': row[12].strftime('%Y-%m-%d %H:%M:%S') if row[12] else None
            })
        
        cur.close()
        conn.close()
        
        return jsonify({
            'messages': messages,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
        
    except Exception as e:
        print(f"[HATA] /api/rooms/{room_id}/messages - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<room_id>/members', methods=['POST'])
@login_required
def add_room_member(room_id):
    """Add a member to a room (DATABASE + Matrix API for sync)"""
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if already member
        cur.execute(
            "SELECT COUNT(*) FROM room_memberships WHERE room_id = %s AND user_id = %s AND membership = 'join'",
            (room_id, user_id)
        )
        exists = cur.fetchone()[0]
        
        if exists > 0:
            cur.close()
            conn.close()
            return jsonify({'message': 'User already in room', 'success': True})
        
        # Get admin token for Matrix API call
        cur.execute(
            "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
            (ADMIN_USER_ID,)
        )
        token_row = cur.fetchone()
        admin_token = token_row[0] if token_row else None
        
        # Check if admin is already in room (before closing connection)
        cur.execute(
            "SELECT COUNT(*) FROM room_memberships WHERE room_id = %s AND user_id = %s AND membership = 'join'",
            (room_id, ADMIN_USER_ID)
        )
        admin_in_room = cur.fetchone()[0] > 0
        
        cur.close()
        conn.close()
        
        # Get Synapse URL (for both auto-login and API calls)
        import requests
        synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
        
        # If no token, try auto-login
        if not admin_token:
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_password = os.getenv('ADMIN_PASSWORD')
            
            if admin_password:
                print(f"[INFO] No admin token, attempting auto-login...")
                try:
                    login_response = requests.post(
                        f'{synapse_url}/_matrix/client/v3/login',
                        json={
                            'type': 'm.login.password',
                            'identifier': {'type': 'm.id.user', 'user': admin_username},
                            'password': admin_password
                        },
                        timeout=10
                    )
                    if login_response.status_code == 200:
                        admin_token = login_response.json().get('access_token')
                        print(f"[INFO] Auto-login successful for member add!")
                except Exception as e:
                    print(f"[WARN] Auto-login failed: {e}")
        
        if not admin_token:
            return jsonify({'error': 'Admin not logged in. Please set ADMIN_PASSWORD environment variable.', 'success': False}), 401
        
        # Update headers with new token (in case auto-login happened)
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        if not admin_in_room:
            try:
                print(f"Admin not in room, adding admin first...")
                admin_join_url = f'{synapse_url}/_synapse/admin/v1/join/{room_id}'
                admin_response = requests.post(admin_join_url, headers=headers, json={'user_id': ADMIN_USER_ID}, timeout=5)
                print(f"Admin join result: {admin_response.status_code}")
                
                if admin_response.status_code != 200:
                    print(f"Admin join failed: {admin_response.text}")
                    # Continue anyway, maybe user can be added
            except Exception as admin_err:
                print(f"Admin join attempt failed: {admin_err}")
                # Continue anyway
        
        # Step 2: Try Admin API join first
        try:
            admin_join_url = f'{synapse_url}/_synapse/admin/v1/join/{room_id}'
            print(f"[INFO] Trying Admin API force-join for {user_id}...")
            admin_api_response = requests.post(admin_join_url, headers=headers, json={'user_id': user_id}, timeout=5)
            print(f"[INFO] Admin API result: {admin_api_response.status_code} - {admin_api_response.text[:200]}")
            
            if admin_api_response.status_code == 200:
                # Success! User joined via Admin API - this sends notification
                return jsonify({
                    'message': f'✅ {user_id} odaya eklendi! Element Web\'de bildirim alacak.',
                    'success': True,
                    'method': 'admin_api'
                })
            
            # If Admin API failed, try sending invite first (so user gets notification)
            print(f"[WARN] Admin API failed ({admin_api_response.status_code}), trying invite...")
            invite_url = f'{synapse_url}/_matrix/client/v3/rooms/{room_id}/invite'
            invite_response = requests.post(invite_url, headers=headers, json={'user_id': user_id}, timeout=5)
            print(f"[INFO] Invite result: {invite_response.status_code} - {invite_response.text[:200]}")
            
            # If invite sent successfully, try to auto-join user with their token
            if invite_response.status_code == 200:
                print(f"[INFO] Invite sent successfully, trying to auto-join user with their token...")
                join_url = f'{synapse_url}/_matrix/client/v3/rooms/{room_id}/join'
                
                # Get user's access token to join as them (auto-accept invite)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                    (user_id,)
                )
                user_token_row = cur.fetchone()
                user_token = user_token_row[0] if user_token_row else None
                
                if user_token:
                    # Join as the user (auto-accept invite, they will get notification)
                    user_headers = {
                        'Authorization': f'Bearer {user_token}',
                        'Content-Type': 'application/json'
                    }
                    print(f"[INFO] Joining as user via Client API v3...")
                    user_join_response = requests.post(join_url, headers=user_headers, json={}, timeout=5)
                    print(f"[INFO] User join result: {user_join_response.status_code} - {user_join_response.text[:200]}")
                    
                    if user_join_response.status_code == 200:
                        # Success! User auto-joined, they got notification
                        cur.close()
                        conn.close()
                        return jsonify({
                            'success': True,
                            'message': f'✅ {user_id} odaya eklendi! Element Web\'de bildirim alacak.',
                            'method': 'invite_autojoin'
                        })
                    elif user_join_response.status_code == 403:
                        # User might already be in room, check database
                        cur.execute(
                            "SELECT COUNT(*) FROM room_memberships WHERE room_id = %s AND user_id = %s AND membership = 'join'",
                            (room_id, user_id)
                        )
                        already_member = cur.fetchone()[0] > 0
                        cur.close()
                        conn.close()
                        
                        if already_member:
                            return jsonify({
                                'success': True,
                                'message': f'✅ {user_id} zaten odada!',
                                'method': 'already_member'
                            })
                
                cur.close()
                conn.close()
                
                # Invite sent but couldn't auto-join - add to database anyway
                # User will see invite notification and can accept manually
                conn = get_db_connection()
                cur = conn.cursor()
                import time
                event_id = f"$admin_force_add_{int(time.time()*1000)}"
                cur.execute("""
                    INSERT INTO room_memberships (event_id, user_id, sender, room_id, membership)
                    VALUES (%s, %s, %s, %s, 'join')
                    ON CONFLICT DO NOTHING
                """, (event_id, user_id, ADMIN_USER_ID, room_id))
                conn.commit()
                cur.close()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'message': f'✅ {user_id} odaya eklendi! Davet gönderildi, Element Web\'de bildirim alacak.',
                    'method': 'invite_database'
                })
            
            # Invite failed or not sent - add to database anyway
            conn = get_db_connection()
            cur = conn.cursor()
            import time
            event_id = f"$admin_force_add_{int(time.time()*1000)}"
            cur.execute("""
                INSERT INTO room_memberships (event_id, user_id, sender, room_id, membership)
                VALUES (%s, %s, %s, %s, 'join')
                ON CONFLICT DO NOTHING
            """, (event_id, user_id, ADMIN_USER_ID, room_id))
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'✅ {user_id} odaya eklendi. Element Web\'de refresh yapması gerekebilir.',
                'method': 'database'
            })
                
        except Exception as api_error:
            print(f"[ERROR] Matrix API error: {api_error}")
            import traceback
            traceback.print_exc()
            
            # Try database fallback even if API call failed
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                
                import time
                event_id = f"$admin_force_add_{int(time.time()*1000)}"
                
                cur.execute("""
                    INSERT INTO room_memberships (event_id, user_id, sender, room_id, membership)
                    VALUES (%s, %s, %s, %s, 'join')
                    ON CONFLICT DO NOTHING
                """, (event_id, user_id, ADMIN_USER_ID, room_id))
                
                conn.commit()
                cur.close()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'message': f'✅ {user_id} odaya eklendi (database fallback). Element Web\'de refresh yapması gerekebilir.',
                    'method': 'database_fallback'
                })
            except Exception as db_err:
                print(f"[ERROR] Database fallback also failed: {db_err}")
                return jsonify({
                    'error': f'Üye eklenemedi: {str(api_error)}',
                    'success': False
                }), 500
        
    except Exception as e:
        print(f"[HATA] POST /api/rooms/{room_id}/members - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms/<room_id>/members/<user_id>', methods=['DELETE'])
@login_required
def remove_room_member(room_id, user_id):
    """Remove a member from a room (DIRECT DATABASE)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check current membership status
        cur.execute("""
            SELECT membership, event_id 
            FROM room_memberships 
            WHERE room_id = %s AND user_id = %s
        """, (room_id, user_id))
        
        result = cur.fetchone()
        
        if not result:
            cur.close()
            conn.close()
            return jsonify({'message': 'Member not found in room', 'success': False}), 404
        
        current_membership = result[0]
        
        # If already left, no need to update
        if current_membership == 'leave':
            cur.close()
            conn.close()
            return jsonify({'message': 'Member already removed', 'success': True})
        
        # Generate unique event_id using uuid
        import uuid
        event_id = f"$admin_remove_{uuid.uuid4().hex}"
        
        # Update membership to 'leave'
        cur.execute("""
            UPDATE room_memberships 
            SET membership = 'leave', event_id = %s
            WHERE room_id = %s AND user_id = %s AND membership != 'leave'
        """, (event_id, room_id, user_id))
        
        conn.commit()
        
        affected = cur.rowcount
        cur.close()
        conn.close()
        
        if affected > 0:
            return jsonify({'message': 'Member removed successfully', 'success': True})
        else:
            return jsonify({'message': 'Member already removed', 'success': True})
        
    except Exception as e:
        print(f"[HATA] DELETE /api/rooms/{room_id}/members/{user_id} - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users')
@login_required
def get_users():
    """Get all users with extended info (excluding deleted users)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if shadow_banned, locked, and deleted columns exist
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('shadow_banned', 'locked', 'deleted')
        """)
        existing_cols = [row[0] for row in cur.fetchall()]
        has_shadow_banned = 'shadow_banned' in existing_cols
        has_locked = 'locked' in existing_cols
        has_deleted = 'deleted' in existing_cols
        
        # Add deleted column if it doesn't exist
        if not has_deleted:
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted smallint DEFAULT 0")
                conn.commit()
                print("[INFO] Added 'deleted' column to users table")
                has_deleted = True
            except Exception as col_error:
                print(f"[WARN] Could not add deleted column: {col_error}")
                conn.rollback()
        
        shadow_col = 'u.shadow_banned' if has_shadow_banned else 'false as shadow_banned'
        locked_col = 'u.locked' if has_locked else 'false as locked'
        deleted_col = 'u.deleted' if has_deleted else '0 as deleted'
        
        query = f"""
            SELECT 
                u.name,
                u.admin,
                u.deactivated,
                u.creation_ts,
                (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
                (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
                 WHERE user_id = u.name AND membership = 'join') as room_count,
                (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as token_count,
                {shadow_col},
                {locked_col},
                {deleted_col}
            FROM users u
            WHERE ({deleted_col} = 0 OR {deleted_col} IS NULL)
            ORDER BY u.admin DESC, u.deactivated ASC, u.name;
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        users = []
        for row in rows:
            # Handle timestamp (can be in milliseconds or seconds)
            created_str = ''
            if row[3]:
                try:
                    # Try milliseconds first (Synapse format)
                    if row[3] > 10000000000:  # Milliseconds
                        created_str = datetime.fromtimestamp(row[3] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    else:  # Seconds
                        created_str = datetime.fromtimestamp(row[3]).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as ts_err:
                    created_str = str(row[3])
            
            users.append({
                'user_id': row[0],
                'admin': bool(row[1]),
                'deactivated': bool(row[2]),
                'created': created_str,
                'displayname': row[4],
                'room_count': row[5] or 0,
                'active_sessions': row[6] or 0,
                'shadow_banned': bool(row[7]) if row[7] is not None else False,
                'locked': bool(row[8]) if row[8] is not None else False,
                'deleted': bool(row[9]) if len(row) > 9 and row[9] is not None else False
            })
        
        cur.close()
        conn.close()
        
        return jsonify({'users': users, 'total': len(users)})
        
    except Exception as e:
        print(f"[HATA] /api/users - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'details': traceback.format_exc()}), 500

@app.route('/api/users/deleted')
@login_required
def get_deleted_users():
    """Get all deleted users"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if deleted column exists, if not add it
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'deleted'
        """)
        has_deleted_col = cur.fetchone() is not None
        
        if not has_deleted_col:
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted smallint DEFAULT 0")
                conn.commit()
                print("[INFO] Added 'deleted' column to users table")
                has_deleted_col = True
            except Exception as col_error:
                print(f"[WARN] Could not add deleted column: {col_error}")
                conn.rollback()
        
        # Check other columns
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('shadow_banned', 'locked')
        """)
        existing_cols = [row[0] for row in cur.fetchall()]
        has_shadow_banned = 'shadow_banned' in existing_cols
        has_locked = 'locked' in existing_cols
        
        shadow_col = 'u.shadow_banned' if has_shadow_banned else 'false as shadow_banned'
        locked_col = 'u.locked' if has_locked else 'false as locked'
        deleted_col = 'u.deleted' if has_deleted_col else '0 as deleted'
        
        query = f"""
            SELECT 
                u.name,
                u.admin,
                u.deactivated,
                u.creation_ts,
                (SELECT displayname FROM profiles WHERE user_id = u.name LIMIT 1) as displayname,
                (SELECT COUNT(DISTINCT room_id) FROM room_memberships 
                 WHERE user_id = u.name AND membership = 'join') as room_count,
                (SELECT COUNT(*) FROM access_tokens WHERE user_id = u.name) as token_count,
                {shadow_col},
                {locked_col},
                {deleted_col}
            FROM users u
            WHERE {deleted_col} = 1
            ORDER BY u.creation_ts DESC;
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        users = []
        for row in rows:
            # Handle timestamp
            created_str = ''
            if row[3]:
                try:
                    if row[3] > 10000000000:  # Milliseconds
                        created_str = datetime.fromtimestamp(row[3] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    else:  # Seconds
                        created_str = datetime.fromtimestamp(row[3]).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as ts_err:
                    created_str = str(row[3])
            
            users.append({
                'user_id': row[0],
                'admin': bool(row[1]),
                'deactivated': bool(row[2]),
                'created': created_str,
                'displayname': row[4],
                'room_count': row[5] or 0,
                'active_sessions': row[6] or 0,
                'shadow_banned': bool(row[7]) if row[7] is not None else False,
                'locked': bool(row[8]) if row[8] is not None else False,
                'deleted': True
            })
        
        cur.close()
        conn.close()
        
        return jsonify({'users': users, 'total': len(users)})
        
    except Exception as e:
        print(f"[HATA] /api/users/deleted - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'details': traceback.format_exc()}), 500

@app.route('/api/users/<user_id>/details')
@login_required
def get_user_details(user_id):
    """Get detailed user info"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # User basic info
        cur.execute("""
            SELECT name, admin, creation_ts, deactivated, shadow_banned, locked
            FROM users WHERE name = %s
        """, (user_id,))
        user_row = cur.fetchone()
        
        if not user_row:
            return jsonify({'error': 'User not found'}), 404
        
        # User's rooms
        cur.execute("""
            SELECT 
                r.room_id,
                (SELECT ej.json::json->'content'->>'name' 
                 FROM event_json ej
                 WHERE ej.room_id = r.room_id 
                   AND ej.json::json->>'type' = 'm.room.name'
                 LIMIT 1) as room_name,
                (SELECT COUNT(*) FROM room_memberships 
                 WHERE room_id = r.room_id AND membership = 'join') as member_count
            FROM room_memberships rm
            JOIN rooms r ON rm.room_id = r.room_id
            WHERE rm.user_id = %s AND rm.membership = 'join'
            ORDER BY member_count DESC
            LIMIT 20;
        """, (user_id,))
        rooms = cur.fetchall()
        
        # User's devices/sessions
        cur.execute("""
            SELECT device_id, last_seen, ip, user_agent
            FROM devices
            WHERE user_id = %s
            ORDER BY last_seen DESC NULLS LAST
            LIMIT 10;
        """, (user_id,))
        devices = cur.fetchall()
        
        # Last activity
        cur.execute("""
            SELECT MAX(last_seen) FROM devices WHERE user_id = %s
        """, (user_id,))
        last_seen_row = cur.fetchone()
        last_seen = last_seen_row[0] if last_seen_row and last_seen_row[0] else None
        
        cur.close()
        conn.close()
        
        # Parse creation_ts (can be milliseconds or seconds)
        created_str = ''
        if user_row[2]:
            try:
                creation_ts = user_row[2]
                if creation_ts > 10000000000:  # Milliseconds
                    created_str = datetime.fromtimestamp(creation_ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
                else:  # Seconds
                    created_str = datetime.fromtimestamp(creation_ts).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as ts_err:
                created_str = str(user_row[2])
        
        # Parse last_seen (always milliseconds in devices table)
        last_seen_str = 'Hiç görülmedi'
        if last_seen:
            try:
                last_seen_str = datetime.fromtimestamp(last_seen / 1000).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as ls_err:
                last_seen_str = str(last_seen)
        
        # Parse device last_seen timestamps
        device_list = []
        for d in devices:
            device_last_seen = 'Bilinmiyor'
            if d[1]:
                try:
                    device_last_seen = datetime.fromtimestamp(d[1] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as dev_err:
                    device_last_seen = str(d[1])
            
            device_list.append({
                'device_id': d[0],
                'last_seen': device_last_seen,
                'ip': d[2],
                'user_agent': d[3]
            })
        
        return jsonify({
            'user_id': user_row[0],
            'admin': bool(user_row[1]),
            'created': created_str,
            'deactivated': bool(user_row[3]),
            'shadow_banned': bool(user_row[4]) if user_row[4] is not None else False,
            'locked': bool(user_row[5]) if user_row[5] is not None else False,
            'last_seen': last_seen_str,
            'rooms': [{'room_id': r[0], 'name': r[1] or 'İsimsiz Oda', 'member_count': r[2]} for r in rooms],
            'devices': device_list
        })
        
    except Exception as e:
        print(f"[HATA] /api/users/{user_id}/details - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/admin', methods=['PUT'])
@login_required
def toggle_user_admin(user_id):
    """Toggle user admin status"""
    try:
        make_admin = request.json.get('admin', False)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE users SET admin = %s WHERE name = %s
        """, (1 if make_admin else 0, user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'User {"is now" if make_admin else "is no longer"} an admin',
            'admin': make_admin
        })
        
    except Exception as e:
        print(f"[HATA] PUT /api/users/{user_id}/admin - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/deactivate', methods=['PUT'])
@login_required
def toggle_user_deactivate(user_id):
    """Toggle user deactivated status (activate/deactivate)"""
    try:
        deactivate = request.json.get('deactivated', False)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE users SET deactivated = %s WHERE name = %s
        """, (1 if deactivate else 0, user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Kullanıcı {"pasif yapıldı" if deactivate else "aktif yapıldı"}',
            'deactivated': bool(deactivate)
        })
        
    except Exception as e:
        print(f"[HATA] PUT /api/users/{user_id}/deactivate - {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete user - First logout via Matrix API, then delete from database"""
    try:
        import requests
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT name, deactivated FROM users WHERE name = %s", (user_id,))
        user_row = cur.fetchone()
        if not user_row:
            cur.close()
            conn.close()
            return jsonify({'error': 'Kullanıcı bulunamadı', 'success': False}), 404
        
        print(f"[INFO] Deleting user: {user_id} (currently deactivated: {user_row[1]})")
        
        # STEP 1: First, logout user via Matrix Admin API (this will immediately logout active sessions)
        matrix_api_success = False
        try:
            # Get admin token
            cur.execute(
                "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (ADMIN_USER_ID,)
            )
            token_row = cur.fetchone()
            admin_token = token_row[0] if token_row else None
            
            # If no token, try auto-login
            if not admin_token:
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                admin_password = os.getenv('ADMIN_PASSWORD')
                synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
                
                if admin_password:
                    try:
                        login_response = requests.post(
                            f'{synapse_url}/_matrix/client/v3/login',
                            json={
                                'type': 'm.login.password',
                                'identifier': {'type': 'm.id.user', 'user': admin_username},
                                'password': admin_password
                            },
                            timeout=10
                        )
                        
                        if login_response.status_code == 200:
                            admin_token = login_response.json().get('access_token')
                            print(f"[INFO] Auto-login successful for user deletion")
                    except Exception as login_error:
                        print(f"[WARN] Auto-login failed: {login_error}")
            
            # Use Matrix Admin API to deactivate (this logs out user immediately)
            if admin_token:
                synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
                headers = {
                    'Authorization': f'Bearer {admin_token}',
                    'Content-Type': 'application/json'
                }
                
                # Deactivate via Synapse Admin API (this will logout all sessions)
                api_url = f'{synapse_url}/_synapse/admin/v1/deactivate/{user_id}'
                try:
                    response = requests.post(
                        api_url, 
                        headers=headers, 
                        json={'erase': False},  # Don't erase, just deactivate and logout
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        print(f"[INFO] User deactivated via Matrix API (logged out): {user_id}")
                        matrix_api_success = True
                    else:
                        print(f"[WARN] Matrix API deactivate failed: {response.status_code} - {response.text[:200]}")
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    print(f"[WARN] Matrix API timeout/connection error: {e}")
                except Exception as api_error:
                    print(f"[WARN] Matrix API error: {api_error}")
        except Exception as matrix_error:
            print(f"[WARN] Matrix API setup error: {matrix_error}")
        
        # STEP 2: Delete from database (even if Matrix API failed, we still delete from DB)
        # Delete access tokens (logout all sessions from DB)
        cur.execute("""
            DELETE FROM access_tokens WHERE user_id = %s
        """, (user_id,))
        tokens_deleted = cur.rowcount
        
        # Delete devices
        cur.execute("""
            DELETE FROM devices WHERE user_id = %s
        """, (user_id,))
        devices_deleted = cur.rowcount
        
        # Delete room memberships
        cur.execute("""
            DELETE FROM room_memberships WHERE user_id = %s
        """, (user_id,))
        memberships_deleted = cur.rowcount
        
        # Delete user directory entries
        cur.execute("""
            DELETE FROM user_directory WHERE user_id = %s
        """, (user_id,))
        directory_deleted = cur.rowcount
        
        # Delete profiles
        cur.execute("""
            DELETE FROM profiles WHERE user_id = %s
        """, (user_id,))
        profiles_deleted = cur.rowcount
        
        # Check if deleted column exists, if not add it
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'deleted'
        """)
        has_deleted_col = cur.fetchone() is not None
        
        if not has_deleted_col:
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted smallint DEFAULT 0")
                conn.commit()
                print("[INFO] Added 'deleted' column to users table")
            except Exception as col_error:
                print(f"[WARN] Could not add deleted column: {col_error}")
                conn.rollback()
        
        # Mark user as deleted instead of actually deleting (so we can show deleted users)
        cur.execute("""
            UPDATE users 
            SET deleted = 1, deactivated = 1 
            WHERE name = %s
        """, (user_id,))
        user_marked_deleted = cur.rowcount
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"[INFO] User marked as deleted: {user_id} - user: {user_marked_deleted}, tokens: {tokens_deleted}, devices: {devices_deleted}, memberships: {memberships_deleted}, matrix_api: {matrix_api_success}")
        
        msg = f'Kullanıcı başarıyla silindi: {user_id}'
        if matrix_api_success:
            msg += ' - Aktif oturumlar kapatıldı (Matrix API)'
        else:
            msg += ' - Sistemden kaldırıldı (Matrix API kullanılamadı)'
        
        return jsonify({
            'success': True,
            'message': msg,
            'user_deleted': user_marked_deleted > 0,
            'tokens_deleted': tokens_deleted,
            'devices_deleted': devices_deleted,
            'memberships_deleted': memberships_deleted,
            'matrix_api_logout': matrix_api_success
        })
        
    except Exception as e:
        print(f"[HATA] DELETE /api/users/{user_id} - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/users/<user_id>/password', methods=['PUT'])
@login_required
def change_user_password(user_id):
    """Change user password"""
    try:
        new_password = request.json.get('new_password', '').strip()
        
        if not new_password:
            return jsonify({'error': 'Yeni şifre gerekli', 'success': False}), 400
        
        if len(new_password) < 8:
            return jsonify({'error': 'Şifre en az 8 karakter olmalıdır', 'success': False}), 400
        
        # Try Matrix Admin API first
        try:
            import requests
            import bcrypt
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Get admin token
            cur.execute(
                "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (ADMIN_USER_ID,)
            )
            token_row = cur.fetchone()
            admin_token = token_row[0] if token_row else None
            
            # If no token, try auto-login
            if not admin_token:
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                admin_password = os.getenv('ADMIN_PASSWORD')
                synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
                
                if admin_password:
                    print(f"[INFO] No admin token, attempting auto-login for password change...")
                    try:
                        login_response = requests.post(
                            f'{synapse_url}/_matrix/client/v3/login',
                            json={
                                'type': 'm.login.password',
                                'identifier': {'type': 'm.id.user', 'user': admin_username},
                                'password': admin_password
                            },
                            timeout=10
                        )
                        
                        if login_response.status_code == 200:
                            admin_token = login_response.json().get('access_token')
                            print(f"[INFO] Auto-login successful!")
                    except Exception as login_error:
                        print(f"[WARN] Auto-login failed: {login_error}")
            
            cur.close()
            conn.close()
            
            # If we have a token, use Matrix Admin API
            if admin_token:
                synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
                headers = {
                    'Authorization': f'Bearer {admin_token}',
                    'Content-Type': 'application/json'
                }
                
                # Reset password via Synapse Admin API
                api_url = f'{synapse_url}/_synapse/admin/v1/reset_password/{user_id}'
                response = requests.post(api_url, headers=headers, json={'new_password': new_password, 'logout_devices': False}, timeout=10)
                
                if response.status_code == 200:
                    return jsonify({
                        'success': True,
                        'message': f'Şifre başarıyla değiştirildi (Matrix API)',
                        'method': 'matrix_api'
                    })
                else:
                    print(f"[ERROR] Matrix API password change failed: {response.status_code} - {response.text[:200]}")
                    return jsonify({
                        'error': f'Matrix API password change failed: {response.status_code} - {response.text[:200]}',
                        'success': False
                    }), 500
            
            # REMOVED: Database fallback - Matrix Admin API is now REQUIRED
            # Matrix Synapse cannot read password_hash directly from database
            # We MUST use Matrix Admin API for password changes
            print(f"[ERROR] Admin token not found and auto-login failed!")
            return jsonify({
                'error': 'Matrix Admin API requires admin token. Please ensure ADMIN_PASSWORD is set correctly.',
                'success': False
            }), 500
            
        except Exception as api_error:
            print(f"[ERROR] Password change error: {api_error}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': f'Matrix API error: {str(api_error)}',
                'success': False
            }), 500
        
    except Exception as e:
        print(f"[HATA] PUT /api/users/{user_id}/password - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/users', methods=['POST'])
@login_required
def create_user():
    """Create a new user (DATABASE ONLY - for Railway)"""
    try:
        username = request.json.get('username', '').strip()
        password = request.json.get('password', '').strip()
        displayname = request.json.get('displayname', '').strip()
        make_admin = request.json.get('admin', False)
        
        if not username or not password:
            return jsonify({'error': 'Username and password required', 'success': False}), 400
        
        # Construct user ID with proper domain (Railway or localhost)
        homeserver_domain = os.getenv('HOMESERVER_DOMAIN', 'localhost')
        user_id = f'@{username}:{homeserver_domain}'
        
        # Try Matrix Admin API first (if running locally with Synapse)
        try:
            import requests
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute(
                "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (ADMIN_USER_ID,)
            )
            token_row = cur.fetchone()
            admin_token = token_row[0] if token_row else None
            
            print(f"[DEBUG] Token query for {ADMIN_USER_ID}: token_row={token_row}, admin_token={'FOUND' if admin_token else 'NONE'}")
            
            cur.close()
            conn.close()
            
            # If no token, try to auto-login admin to get one
            if not admin_token:
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                admin_password = os.getenv('ADMIN_PASSWORD')
                synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
                
                if admin_password:
                    print(f"[INFO] No admin token found, attempting auto-login for {ADMIN_USER_ID}...")
                    try:
                        login_response = requests.post(
                            f'{synapse_url}/_matrix/client/v3/login',
                            json={
                                'type': 'm.login.password',
                                'identifier': {
                                    'type': 'm.id.user',
                                    'user': admin_username
                                },
                                'password': admin_password
                            },
                            timeout=10
                        )
                        
                        if login_response.status_code == 200:
                            admin_token = login_response.json().get('access_token')
                            print(f"[INFO] Auto-login successful! Token obtained: {admin_token[:20]}...")
                        else:
                            print(f"[WARN] Auto-login failed: {login_response.status_code} - {login_response.text[:100]}")
                    except Exception as login_error:
                        print(f"[WARN] Auto-login error: {login_error}")
            
            if admin_token:
                # Matrix API available - use it
                import requests
                
                print(f"[DEBUG] Admin token found: {admin_token[:20]}...")
                
                headers = {
                    'Authorization': f'Bearer {admin_token}',
                    'Content-Type': 'application/json'
                }
                
                user_data = {
                    'password': password,
                    'displayname': displayname if displayname else username,
                    'admin': make_admin
                }
                
                # Use Synapse URL (localhost for local, Railway URL for production)
                synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
                api_url = f'{synapse_url}/_synapse/admin/v2/users/{user_id}'
                
                print(f"[DEBUG] Calling Synapse API: {api_url}")
                print(f"[DEBUG] User data: {user_data}")
                response = requests.put(api_url, headers=headers, json=user_data, timeout=10)
                print(f"[DEBUG] Synapse API response: {response.status_code} - {response.text[:200]}")
                
                if response.status_code == 200 or response.status_code == 201:
                    # Verify user was created correctly
                    print(f"[INFO] User created via Matrix API. Verifying password...")
                    # Test login to verify password works
                    login_success = False
                    try:
                        test_login = requests.post(
                            f'{synapse_url}/_matrix/client/v3/login',
                            json={
                                'type': 'm.login.password',
                                'identifier': {'type': 'm.id.user', 'user': username},
                                'password': password
                            },
                            timeout=5
                        )
                        if test_login.status_code == 200:
                            print(f"[INFO] Password verification successful!")
                            login_success = True
                        else:
                            print(f"[WARN] Password verification failed: {test_login.status_code} - {test_login.text[:100]}")
                            print(f"[WARN] Matrix API created user but password doesn't work. This is a problem!")
                    except Exception as verify_error:
                        print(f"[WARN] Could not verify password: {verify_error}")
                    
                    if not login_success:
                        print(f"[ERROR] Matrix API created user but password verification failed!")
                        print(f"[ERROR] Resetting password via Matrix Admin API...")
                        # Reset password via Matrix Admin API to ensure it works
                        try:
                            reset_response = requests.post(
                                f'{synapse_url}/_synapse/admin/v1/reset_password/{user_id}',
                                headers=headers,
                                json={'new_password': password, 'logout_devices': False},
                                timeout=10
                            )
                            if reset_response.status_code == 200:
                                print(f"[INFO] Password reset via Matrix Admin API successful!")
                                # Verify again
                                test_login2 = requests.post(
                                    f'{synapse_url}/_matrix/client/v3/login',
                                    json={
                                        'type': 'm.login.password',
                                        'identifier': {'type': 'm.id.user', 'user': username},
                                        'password': password
                                    },
                                    timeout=5
                                )
                                if test_login2.status_code == 200:
                                    print(f"[INFO] Password verification after reset successful!")
                                    return jsonify({
                                        'success': True,
                                        'user_id': user_id,
                                        'message': 'User created successfully via Matrix API (password reset)!',
                                        'method': 'matrix_api_reset'
                                    })
                                else:
                                    print(f"[WARN] Password still doesn't work after reset: {test_login2.status_code}")
                                    # Continue to database fallback
                            else:
                                print(f"[WARN] Password reset failed: {reset_response.status_code} - {reset_response.text[:100]}")
                                # Continue to database fallback
                        except Exception as reset_error:
                            print(f"[WARN] Password reset error: {reset_error}")
                            # Continue to database fallback
                    else:
                        return jsonify({
                            'success': True,
                            'user_id': user_id,
                            'message': 'User created successfully via Matrix API!',
                            'method': 'matrix_api'
                        })
                else:
                    print(f"[ERROR] Synapse API failed with {response.status_code}")
                    print(f"[ERROR] Error details: {response.text[:200]}")
                    return jsonify({
                        'error': f'Matrix API failed: {response.status_code} - {response.text[:200]}',
                        'success': False
                    }), 500
            else:
                print(f"[ERROR] Admin token not found and auto-login failed!")
                return jsonify({
                    'error': 'Matrix Admin API requires admin token. Please ensure ADMIN_PASSWORD is set correctly.',
                    'success': False
                }), 500
        except Exception as api_error:
            print(f"[ERROR] Matrix API error: {api_error}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': f'Matrix API error: {str(api_error)}',
                'success': False
            }), 500
        
        # REMOVED: Database fallback - Matrix Admin API is now REQUIRED
        # Matrix Synapse cannot read password_hash directly from database
        # We MUST use Matrix Admin API for user creation and password management
        # This ensures password hash is stored in the correct format that Matrix Synapse can read
        
    except Exception as e:
        print(f"[HATA] POST /api/users - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/rooms', methods=['POST'])
@login_required  
def create_room():
    """Create a new room using Matrix Client API (proper event stream)"""
    try:
        room_name = request.json.get('name', 'Yeni Oda')
        is_public = request.json.get('is_public', True)
        
        # Get admin token
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
            (ADMIN_USER_ID,)
        )
        token_row = cur.fetchone()
        admin_token = token_row[0] if token_row else None
        
        cur.close()
        conn.close()
        
        # Get Synapse URL (for both auto-login and API calls)
        import requests
        synapse_url = os.getenv('SYNAPSE_URL', 'http://localhost:8008')
        
        # If no token, try auto-login
        if not admin_token:
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_password = os.getenv('ADMIN_PASSWORD')
            
            if admin_password:
                print(f"[INFO] No admin token for room creation, attempting auto-login...")
                try:
                    login_response = requests.post(
                        f'{synapse_url}/_matrix/client/v3/login',
                        json={
                            'type': 'm.login.password',
                            'identifier': {'type': 'm.id.user', 'user': admin_username},
                            'password': admin_password
                        },
                        timeout=10
                    )
                    if login_response.status_code == 200:
                        admin_token = login_response.json().get('access_token')
                        print(f"[INFO] Auto-login successful for room creation!")
                except Exception as e:
                    print(f"[WARN] Auto-login failed: {e}")
        
        if not admin_token:
            return jsonify({
                'error': 'Admin not logged in. Please set ADMIN_PASSWORD environment variable.',
                'success': False
            }), 401
        
        # Use Matrix Client API to create room (proper way!)
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        create_room_body = {
            'name': room_name,
            'visibility': 'public' if is_public else 'private',
            'preset': 'public_chat' if is_public else 'private_chat',
            'room_version': '10'
        }
        
        api_url = f'{synapse_url}/_matrix/client/v3/createRoom'
        
        response = requests.post(api_url, headers=headers, json=create_room_body, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            room_id = result.get('room_id', '')
            
            return jsonify({
                'success': True,
                'room_id': room_id,
                'name': room_name,
                'message': 'Room created successfully via Matrix API!'
            })
        else:
            return jsonify({
                'error': f'Matrix API error: {response.status_code}',
                'success': False,
                'details': response.text
            }), response.status_code
        
    except Exception as e:
        print(f"[HATA] POST /api/rooms - {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
@login_required
def export_data():
    room_id = request.args.get('room_id', '').strip()
    sender = request.args.get('sender', '').strip()
    search = request.args.get('search', '').strip()
    format_type = request.args.get('format', 'json')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        conditions = ["e.type = 'm.room.message'"]
        
        if room_id:
            conditions.append(cur.mogrify("e.room_id = %s", (room_id,)).decode('utf-8'))
        if sender:
            conditions.append(cur.mogrify("e.sender ILIKE %s", (f'%{sender}%',)).decode('utf-8'))
        if search:
            conditions.append(cur.mogrify("ej.json::json->'content'->>'body' ILIKE %s", (f'%{search}%',)).decode('utf-8'))
        
        where_clause = " AND ".join(conditions)
        
        query = f"""
            SELECT 
                to_timestamp(e.origin_server_ts/1000) as timestamp,
                e.sender,
                e.room_id,
                (SELECT ej2.json::json->'content'->>'name' 
                 FROM events e2 
                 JOIN event_json ej2 ON e2.event_id = ej2.event_id 
                 WHERE e2.room_id = e.room_id 
                   AND e2.type = 'm.room.name' 
                 ORDER BY e2.origin_server_ts DESC 
                 LIMIT 1) as room_name,
                ej.json::json->'content'->>'body' as message,
                (SELECT STRING_AGG(DISTINCT rm.user_id, ', ')
                 FROM room_memberships rm
                 WHERE rm.room_id = e.room_id
                   AND rm.user_id != e.sender
                   AND rm.membership = 'join') as recipients
            FROM events e
            JOIN event_json ej ON e.event_id = ej.event_id
            WHERE {where_clause}
            ORDER BY e.origin_server_ts ASC;
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        messages = []
        for row in rows:
            recipients = row[5] if row[5] else 'Grup'
            # Eğer tek alıcı varsa direkt göster, birden fazlaysa sayı göster
            if recipients and recipients != 'Grup':
                recipient_list = recipients.split(', ')
                if len(recipient_list) == 1:
                    recipient_display = recipient_list[0]
                else:
                    recipient_display = f'Grup ({len(recipient_list)} kişi)'
            else:
                recipient_display = 'Grup'
            
            messages.append({
                'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S') if row[0] else '',
                'sender': row[1],
                'room_id': row[2],
                'room_name': row[3] or 'İsimsiz oda',
                'message': row[4],
                'recipient': recipient_display
            })
        
        cur.close()
        conn.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'json':
            output = io.BytesIO()
            output.write(json.dumps(messages, indent=2, ensure_ascii=False).encode('utf-8'))
            output.seek(0)
            return send_file(
                output,
                mimetype='application/json',
                as_attachment=True,
                download_name=f'cravex_messages_{timestamp}.json'
            )
        
        elif format_type == 'csv':
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=['timestamp', 'sender', 'room_name', 'recipient', 'message'])
            writer.writeheader()
            writer.writerows(messages)
            
            mem = io.BytesIO()
            mem.write(output.getvalue().encode('utf-8-sig'))
            mem.seek(0)
            
            return send_file(
                mem,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'cravex_messages_{timestamp}.csv'
            )
        
        return jsonify({'error': 'Invalid format'}), 400
        
    except Exception as e:
        print(f"[HATA] /api/export - {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/test/<server_name>/<path:media_id>')
@login_required
def test_media_access(server_name, media_id):
    """Test media access - returns debug information"""
    try:
        synapse_url = os.getenv('SYNAPSE_URL', f'https://{server_name}')
        homeserver_domain = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')
        
        test_urls = [
            f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}',
            f'{synapse_url}/_matrix/media/r0/download/{homeserver_domain}/{media_id}',
            f'{synapse_url}/_matrix/media/r0/download/{media_id}',
        ]
        
        results = []
        for url in test_urls:
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                results.append({
                    'url': url,
                    'status': response.status_code,
                    'headers': dict(response.headers)
                })
            except Exception as e:
                results.append({
                    'url': url,
                    'status': 'ERROR',
                    'error': str(e)
                })
        
        return jsonify({
            'server_name': server_name,
            'media_id': media_id,
            'homeserver_domain': homeserver_domain,
            'synapse_url': synapse_url,
            'test_results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/download/<server_name>/<path:media_id>')
@login_required
def proxy_media_download(server_name, media_id):
    """Proxy media download requests to Matrix Synapse"""
    try:
        synapse_url = os.getenv('SYNAPSE_URL', f'https://{server_name}')
        homeserver_domain = os.getenv('HOMESERVER_DOMAIN', 'matrix-synapse.up.railway.app')
        
        # Matrix media URL format: /_matrix/media/r0/download/{server_name}/{media_id}
        # But if server_name == homeserver_domain, we can try without server_name
        media_url = f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}'
        
        print(f"[DEBUG] ===== Media Download Request =====")
        print(f"[DEBUG] Server name from URL: {server_name}")
        print(f"[DEBUG] Media ID: {media_id}")
        print(f"[DEBUG] Synapse URL: {synapse_url}")
        print(f"[DEBUG] Homeserver domain: {homeserver_domain}")
        print(f"[DEBUG] Primary URL: {media_url}")
        
        # Try to get sender's token from the media event
        # First, find which event contains this media_id
        sender_token = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Find the event that contains this media_id
            # Search in event_json table (JSON data is stored separately in Matrix Synapse)
            cur.execute("""
                SELECT e.sender 
                FROM events e
                JOIN event_json ej ON e.event_id = ej.event_id
                WHERE jsonb_typeof(ej.json::jsonb) = 'object' 
                AND (
                    (ej.json::jsonb)->'content'->>'url' LIKE %s 
                    OR (ej.json::jsonb)->'content'->'info'->>'thumbnail_url' LIKE %s
                )
                ORDER BY e.stream_ordering DESC 
                LIMIT 1
            """, (f'%{media_id}%', f'%{media_id}%'))
            
            sender_row = cur.fetchone()
            if sender_row:
                sender = sender_row[0]
                print(f"[DEBUG] Found sender for media {media_id}: {sender}")
                
                # Get sender's token
                cur.execute(
                    "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                    (sender,)
                )
                token_row = cur.fetchone()
                if token_row:
                    sender_token = token_row[0]
                    print(f"[DEBUG] Found token for sender {sender}: {sender_token[:20]}...")
            
            # Fallback: Try admin token
            if not sender_token:
                cur.execute(
                    "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                    (ADMIN_USER_ID,)
                )
                token_row = cur.fetchone()
                sender_token = token_row[0] if token_row else None
                if sender_token:
                    print(f"[DEBUG] Using admin token as fallback")
            
            # Fallback 2: Try any active user token
            if not sender_token:
                cur.execute(
                    "SELECT token, user_id FROM access_tokens WHERE id IN (SELECT MAX(id) FROM access_tokens GROUP BY user_id) ORDER BY id DESC LIMIT 1"
                )
                any_token_row = cur.fetchone()
                if any_token_row:
                    sender_token = any_token_row[0]
                    print(f"[DEBUG] Using token from user {any_token_row[1]} for media access")
            
            cur.close()
            conn.close()
        except Exception as token_error:
            print(f"[WARN] Could not get sender token: {token_error}")
            sender_token = None
        
        # Forward request to Matrix Synapse with headers
        headers = {
            'User-Agent': 'Cravex-Admin-Panel/1.0',
            'Accept': '*/*'
        }
        if sender_token:
            headers['Authorization'] = f'Bearer {sender_token}'
            print(f"[DEBUG] Using sender token for authentication: {sender_token[:20]}...")
        else:
            print(f"[WARN] No token found - trying without authentication")
        
        # 1. Önce cache'den kontrol et
        cached_media = get_media_from_cache(media_id)
        if cached_media:
            print(f"[INFO] ✅ Media served from cache: {media_id} ({cached_media['file_size'] / 1024:.2f} KB)")
            return Response(
                cached_media['media_data'],
                mimetype=cached_media['content_type'] or 'application/octet-stream',
                headers={
                    'Content-Disposition': f'inline; filename="{media_id}"',
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*',
                    'X-Cache': 'HIT'
                }
            )
        
        print(f"[INFO] ⏳ Media not in cache, fetching from Matrix: {media_id}")
        
        # Try Matrix Client API v1 endpoint first (Element Web uses this format with auth)
        client_api_v1_url = None
        client_api_v1_tried = False
        if sender_token:
            # Matrix Client API v1 endpoint (Element Web format: /_matrix/client/v1/media/download/)
            # Format: /_matrix/client/v1/media/download/{server_name}/{media_id}?allow_redirect=true
            client_api_v1_url = f'{synapse_url}/_matrix/client/v1/media/download/{server_name}/{media_id}?allow_redirect=true'
            print(f"[DEBUG] Trying Matrix Client API v1 (Element Web format): {client_api_v1_url}")
            try:
                client_v1_response = requests.get(client_api_v1_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                print(f"[DEBUG] Client API v1 response: {client_v1_response.status_code}")
                if client_v1_response.status_code == 200:
                    print(f"[DEBUG] ✅ Matrix Client API v1 worked!")
                    content_type = client_v1_response.headers.get('Content-Type', 'application/octet-stream')
                    media_data = client_v1_response.content
                    file_size = len(media_data)
                    
                    # Cache'e kaydet
                    mxc_url = f'mxc://{server_name}/{media_id}'
                    save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type, None, None)
                    
                    def generate():
                        yield media_data
                    
                    return Response(
                        generate(),
                        mimetype=content_type,
                        headers={
                            'Content-Disposition': f'inline; filename="{media_id}"',
                            'Cache-Control': 'public, max-age=3600',
                            'Access-Control-Allow-Origin': '*',
                            'X-Cache': 'MISS',
                            'X-Source': 'Client-API-v1'
                        }
                    )
                else:
                    print(f"[DEBUG] Client API v1 failed: {client_v1_response.status_code}")
                    if hasattr(client_v1_response, 'text'):
                        print(f"[DEBUG] Client API v1 response text: {client_v1_response.text[:200]}")
            except Exception as e:
                print(f"[WARN] Client API v1 error: {e}")
                import traceback
                traceback.print_exc()
        
        # Try Matrix Media API v3 endpoint (Element Web also tries this without auth)
        media_v3_url = None
        media_v3_tried = False
        # Try without auth first (as Element Web does)
        media_v3_url = f'{synapse_url}/_matrix/media/v3/download/{server_name}/{media_id}?allow_redirect=true'
        print(f"[DEBUG] Trying Matrix Media API v3 (Element Web format, no auth): {media_v3_url}")
        try:
            media_v3_headers = {
                'User-Agent': 'Cravex-Admin-Panel/1.0',
                'Accept': '*/*'
            }
            media_v3_response = requests.get(media_v3_url, stream=True, timeout=30, allow_redirects=True, headers=media_v3_headers)
            print(f"[DEBUG] Media API v3 response: {media_v3_response.status_code}")
            if media_v3_response.status_code == 200:
                print(f"[DEBUG] ✅ Matrix Media API v3 worked!")
                content_type = media_v3_response.headers.get('Content-Type', 'application/octet-stream')
                media_data = media_v3_response.content
                file_size = len(media_data)
                
                # Cache'e kaydet
                mxc_url = f'mxc://{server_name}/{media_id}'
                save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type, None, None)
                
                def generate():
                    yield media_data
                
                return Response(
                    generate(),
                    mimetype=content_type,
                    headers={
                        'Content-Disposition': f'inline; filename="{media_id}"',
                        'Cache-Control': 'public, max-age=3600',
                        'Access-Control-Allow-Origin': '*',
                        'X-Cache': 'MISS',
                        'X-Source': 'Media-API-v3'
                    }
                )
            else:
                print(f"[DEBUG] Media API v3 failed: {media_v3_response.status_code}")
                if hasattr(media_v3_response, 'text'):
                    print(f"[DEBUG] Media API v3 response text: {media_v3_response.text[:200]}")
        except Exception as e:
            print(f"[WARN] Media API v3 error: {e}")
            import traceback
            traceback.print_exc()
        
        # Try Matrix Client API v3 endpoint (fallback)
        client_api_url = None
        client_api_tried = False
        if sender_token:
            # Matrix Client API v3 endpoint (requires auth)
            client_api_url = f'{synapse_url}/_matrix/client/v3/download/{server_name}/{media_id}'
            print(f"[DEBUG] Trying Matrix Client API v3: {client_api_url}")
            try:
                client_response = requests.get(client_api_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                if client_response.status_code == 200:
                    print(f"[DEBUG] ✅ Matrix Client API v3 worked!")
                    content_type = client_response.headers.get('Content-Type', 'application/octet-stream')
                    media_data = client_response.content
                    file_size = len(media_data)
                    
                    # Cache'e kaydet
                    mxc_url = f'mxc://{server_name}/{media_id}'
                    save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type, None, None)
                    
                    def generate():
                        yield media_data
                    
                    return Response(
                        generate(),
                        mimetype=content_type,
                        headers={
                            'Content-Disposition': f'inline; filename="{media_id}"',
                            'Cache-Control': 'public, max-age=3600',
                            'Access-Control-Allow-Origin': '*',
                            'X-Cache': 'MISS',
                            'X-Source': 'Client-API-v3'
                        }
                    )
                else:
                    print(f"[DEBUG] Matrix Client API v3 failed: {client_response.status_code}")
                    if hasattr(client_response, 'text'):
                        print(f"[DEBUG] Client API v3 response text: {client_response.text[:200]}")
            except Exception as e:
                print(f"[WARN] Matrix Client API v3 error: {e}")
                import traceback
                traceback.print_exc()
        
        # Fallback to media API
        print(f"[DEBUG] Request headers: {headers}")
        response = requests.get(media_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            # Get content type from response
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            print(f"[DEBUG] Media download successful: {content_type}")
            
            # Media data'yı memory'de topla (cache için)
            media_data = response.content
            file_size = len(media_data)
            
            # Cache'e kaydet (küçük dosyalar için)
            mxc_url = f'mxc://{server_name}/{media_id}'
            save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type, None, None)
            
            # Stream the response
            def generate():
                yield media_data
            
            return Response(
                generate(),
                mimetype=content_type,
                headers={
                    'Content-Disposition': f'inline; filename="{media_id}"',
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*',
                    'X-Cache': 'MISS'
                }
            )
        else:
            error_text = response.text[:500] if hasattr(response, 'text') else str(response.content[:500])
            print(f"[WARN] Media download failed: {response.status_code}")
            print(f"[WARN] Response headers: {dict(response.headers)}")
            print(f"[WARN] Response text: {error_text}")
            print(f"[WARN] Request URL: {media_url}")
            
            # Try alternative URL formats
            if response.status_code == 404 or response.status_code >= 500:
                print(f"[DEBUG] Primary URL failed with {response.status_code}, trying alternatives...")
                
                # Try 0: Matrix Media API v3 (Element Web format - if not tried yet)
                if sender_token and not media_v3_tried:
                    media_v3_url = f'{synapse_url}/_matrix/media/v3/download/{server_name}/{media_id}?allow_redirect=true'
                    print(f"[DEBUG] Trying Matrix Media API v3 (Element Web format): {media_v3_url}")
                    try:
                        media_v3_response = requests.get(media_v3_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                        if media_v3_response.status_code == 200:
                            print(f"[DEBUG] ✅ Matrix Media API v3 worked!")
                            content_type = media_v3_response.headers.get('Content-Type', 'application/octet-stream')
                            media_data = media_v3_response.content
                            file_size = len(media_data)
                            
                            mxc_url = f'mxc://{server_name}/{media_id}'
                            save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type, None, None)
                            
                            def generate():
                                yield media_data
                            
                            return Response(
                                generate(),
                                mimetype=content_type,
                                headers={
                                    'Content-Disposition': f'inline; filename="{media_id}"',
                                    'Cache-Control': 'public, max-age=3600',
                                    'Access-Control-Allow-Origin': '*',
                                    'X-Cache': 'MISS',
                                    'X-Source': 'Media-API-v3-Fallback'
                                }
                            )
                    except Exception as e:
                        print(f"[WARN] Media API v3 fallback error: {e}")
                
                # Try 1: Matrix Client API v3 (if not tried yet)
                if sender_token and not client_api_tried:
                    client_api_url = f'{synapse_url}/_matrix/client/v3/download/{server_name}/{media_id}'
                    print(f"[DEBUG] Trying Matrix Client API v3: {client_api_url}")
                    try:
                        client_response = requests.get(client_api_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                        if client_response.status_code == 200:
                            print(f"[DEBUG] ✅ Matrix Client API v3 worked!")
                            content_type = client_response.headers.get('Content-Type', 'application/octet-stream')
                            media_data = client_response.content
                            file_size = len(media_data)
                            
                            mxc_url = f'mxc://{server_name}/{media_id}'
                            save_media_to_cache(media_id, server_name, mxc_url, media_data, content_type, None, None)
                            
                            def generate():
                                yield media_data
                            
                            return Response(
                                generate(),
                                mimetype=content_type,
                                headers={
                                    'Content-Disposition': f'inline; filename="{media_id}"',
                                    'Cache-Control': 'public, max-age=3600',
                                    'Access-Control-Allow-Origin': '*',
                                    'X-Cache': 'MISS',
                                    'X-Source': 'Client-API-v3-Fallback'
                                }
                            )
                    except Exception as e:
                        print(f"[WARN] Matrix Client API v3 fallback error: {e}")
                
                # Try 1: Use homeserver_domain instead of server_name
                if server_name != homeserver_domain:
                    alt_url1 = f'{synapse_url}/_matrix/media/r0/download/{homeserver_domain}/{media_id}'
                    print(f"[DEBUG] Trying alternative URL 1 (homeserver_domain): {alt_url1}")
                    alt_response1 = requests.get(alt_url1, stream=True, timeout=30, allow_redirects=True, headers=headers)
                    if alt_response1.status_code == 200:
                        print(f"[DEBUG] ✅ Alternative URL 1 worked!")
                        content_type = alt_response1.headers.get('Content-Type', 'application/octet-stream')
                        def generate():
                            for chunk in alt_response1.iter_content(chunk_size=8192):
                                if chunk:
                                    yield chunk
                        return Response(
                            generate(),
                            mimetype=content_type,
                            headers={
                                'Content-Disposition': f'inline; filename="{media_id}"',
                                'Cache-Control': 'public, max-age=3600',
                                'Access-Control-Allow-Origin': '*'
                            }
                        )
                    else:
                        print(f"[DEBUG] Alternative URL 1 failed: {alt_response1.status_code}")
                
                # Try 2: Without server_name in path (some Synapse configs)
                alt_url2 = f'{synapse_url}/_matrix/media/r0/download/{media_id}'
                print(f"[DEBUG] Trying alternative URL 2 (no server_name): {alt_url2}")
                alt_response2 = requests.get(alt_url2, stream=True, timeout=30, allow_redirects=True, headers=headers)
                if alt_response2.status_code == 200:
                    print(f"[DEBUG] ✅ Alternative URL 2 worked!")
                    content_type = alt_response2.headers.get('Content-Type', 'application/octet-stream')
                    def generate():
                        for chunk in alt_response2.iter_content(chunk_size=8192):
                            if chunk:
                                yield chunk
                    return Response(
                        generate(),
                        mimetype=content_type,
                        headers={
                            'Content-Disposition': f'inline; filename="{media_id}"',
                            'Cache-Control': 'public, max-age=3600',
                            'Access-Control-Allow-Origin': '*'
                        }
                    )
                else:
                    print(f"[DEBUG] Alternative URL 2 failed: {alt_response2.status_code}")
                    print(f"[DEBUG] Response: {alt_response2.text[:200]}")
                
                # Try 3: Matrix Client API endpoint (v3) - requires authentication
                if sender_token:
                    alt_url3 = f'{synapse_url}/_matrix/client/v3/download/{server_name}/{media_id}'
                    print(f"[DEBUG] Trying alternative URL 3 (client v3 with auth): {alt_url3}")
                    alt_response3 = requests.get(alt_url3, stream=True, timeout=30, allow_redirects=True, headers=headers)
                    if alt_response3.status_code == 200:
                        print(f"[DEBUG] ✅ Alternative URL 3 worked!")
                        content_type = alt_response3.headers.get('Content-Type', 'application/octet-stream')
                        def generate():
                            for chunk in alt_response3.iter_content(chunk_size=8192):
                                if chunk:
                                    yield chunk
                        return Response(
                            generate(),
                            mimetype=content_type,
                            headers={
                                'Content-Disposition': f'inline; filename="{media_id}"',
                                'Cache-Control': 'public, max-age=3600',
                                'Access-Control-Allow-Origin': '*'
                            }
                        )
                    else:
                        print(f"[DEBUG] Alternative URL 3 failed: {alt_response3.status_code}")
                        print(f"[DEBUG] Response: {alt_response3.text[:200]}")
                
                # Try 4: Matrix Client API endpoint without server_name (v3)
                if sender_token:
                    alt_url4 = f'{synapse_url}/_matrix/client/v3/download/{media_id}'
                    print(f"[DEBUG] Trying alternative URL 4 (client v3, no server_name): {alt_url4}")
                    alt_response4 = requests.get(alt_url4, stream=True, timeout=30, allow_redirects=True, headers=headers)
                    if alt_response4.status_code == 200:
                        print(f"[DEBUG] ✅ Alternative URL 4 worked!")
                        content_type = alt_response4.headers.get('Content-Type', 'application/octet-stream')
                        def generate():
                            for chunk in alt_response4.iter_content(chunk_size=8192):
                                if chunk:
                                    yield chunk
                        return Response(
                            generate(),
                            mimetype=content_type,
                            headers={
                                'Content-Disposition': f'inline; filename="{media_id}"',
                                'Cache-Control': 'public, max-age=3600',
                                'Access-Control-Allow-Origin': '*'
                            }
                        )
                    else:
                        print(f"[DEBUG] Alternative URL 4 failed: {alt_response4.status_code}")
                
                # Try 5: Media v1 endpoint (some Synapse configs)
                alt_url5 = f'{synapse_url}/_matrix/media/v1/download/{server_name}/{media_id}'
                print(f"[DEBUG] Trying alternative URL 5 (media v1): {alt_url5}")
                alt_response5 = requests.get(alt_url5, stream=True, timeout=30, allow_redirects=True, headers=headers)
                if alt_response5.status_code == 200:
                    print(f"[DEBUG] ✅ Alternative URL 5 worked!")
                    content_type = alt_response5.headers.get('Content-Type', 'application/octet-stream')
                    def generate():
                        for chunk in alt_response5.iter_content(chunk_size=8192):
                            if chunk:
                                yield chunk
                    return Response(
                        generate(),
                        mimetype=content_type,
                        headers={
                            'Content-Disposition': f'inline; filename="{media_id}"',
                            'Cache-Control': 'public, max-age=3600',
                            'Access-Control-Allow-Origin': '*'
                        }
                    )
                else:
                    print(f"[DEBUG] Alternative URL 5 failed: {alt_response5.status_code}")
                
                # Try 3: Check if media is on a different server (federated)
                if server_name != homeserver_domain:
                    federated_url = f'https://{server_name}/_matrix/media/r0/download/{server_name}/{media_id}'
                    print(f"[DEBUG] Trying federated URL: {federated_url}")
                    fed_response = requests.get(federated_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                    if fed_response.status_code == 200:
                        print(f"[DEBUG] ✅ Federated URL worked!")
                        content_type = fed_response.headers.get('Content-Type', 'application/octet-stream')
                        def generate():
                            for chunk in fed_response.iter_content(chunk_size=8192):
                                if chunk:
                                    yield chunk
                        return Response(
                            generate(),
                            mimetype=content_type,
                            headers={
                                'Content-Disposition': f'inline; filename="{media_id}"',
                                'Cache-Control': 'public, max-age=3600',
                                'Access-Control-Allow-Origin': '*'
                            }
                        )
                    else:
                        print(f"[DEBUG] Federated URL failed: {fed_response.status_code}")
                
                print(f"[DEBUG] ❌ All alternative URLs failed. Media not found.")
            
            return jsonify({
                'errcode': 'M_NOT_FOUND',
                'error': f'Media not found: {response.status_code}',
                'details': error_text,
                'requested_url': media_url,
                'server_name': server_name,
                'media_id': media_id,
                'homeserver_domain': homeserver_domain,
                'synapse_url': synapse_url,
                'debug_info': {
                    'tried_urls': [
                        media_url,
                        f'{synapse_url}/_matrix/media/r0/download/{homeserver_domain}/{media_id}' if server_name != homeserver_domain else None,
                        f'{synapse_url}/_matrix/media/r0/download/{media_id}',
                        f'https://{server_name}/_matrix/media/r0/download/{server_name}/{media_id}' if server_name != homeserver_domain else None
                    ]
                }
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"[HATA] Media proxy error: {str(e)}")
        return jsonify({
            'errcode': 'M_UNKNOWN',
            'error': f'Media proxy error: {str(e)}'
        }), 500
    except Exception as e:
        print(f"[HATA] Media proxy error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'errcode': 'M_UNKNOWN',
            'error': str(e)
        }), 500

@app.route('/api/media/thumbnail/<server_name>/<path:media_id>')
@login_required
def proxy_media_thumbnail(server_name, media_id):
    """Proxy media thumbnail requests to Matrix Synapse - Önce cache'den kontrol et"""
    try:
        # ÖNCE CACHE'DEN KONTROL ET - Medya veritabanında varsa cache'den servis et
        cached_media = get_media_from_cache(media_id)
        if cached_media:
            print(f"[INFO] ✅ Thumbnail served from cache: {media_id} ({cached_media['file_size'] / 1024:.2f} KB)")
            # Cache'den direkt medya dosyasını servis et (thumbnail yerine full image)
            return Response(
                cached_media['media_data'],
                mimetype=cached_media['content_type'] or 'image/jpeg',
                headers={
                    'Content-Disposition': f'inline; filename="{media_id}"',
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*',
                    'X-Cache': 'HIT',
                    'X-Source': 'Cache'
                }
            )
        
        # Cache'de yoksa Matrix Synapse'den çek
        synapse_url = os.getenv('SYNAPSE_URL', f'https://{server_name}')
        width = request.args.get('width', '800')
        height = request.args.get('height', '600')
        method = request.args.get('method', 'scale')
        
        thumbnail_url = f'{synapse_url}/_matrix/media/r0/thumbnail/{server_name}/{media_id}?width={width}&height={height}&method={method}'
        
        print(f"[DEBUG] Thumbnail not in cache, proxying from Matrix: {thumbnail_url}")
        print(f"[DEBUG] Server name: {server_name}, Media ID: {media_id}")
        
        # Try to get sender's token from the media event
        sender_token = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Find the event that contains this media_id
            # Search in event_json table (JSON data is stored separately in Matrix Synapse)
            cur.execute("""
                SELECT e.sender 
                FROM events e
                JOIN event_json ej ON e.event_id = ej.event_id
                WHERE jsonb_typeof(ej.json::jsonb) = 'object' 
                AND (
                    (ej.json::jsonb)->'content'->>'url' LIKE %s 
                    OR (ej.json::jsonb)->'content'->'info'->>'thumbnail_url' LIKE %s
                )
                ORDER BY e.stream_ordering DESC 
                LIMIT 1
            """, (f'%{media_id}%', f'%{media_id}%'))
            
            sender_row = cur.fetchone()
            if sender_row:
                sender = sender_row[0]
                print(f"[DEBUG] Found sender for thumbnail {media_id}: {sender}")
                
                # Get sender's token
                cur.execute(
                    "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                    (sender,)
                )
                token_row = cur.fetchone()
                if token_row:
                    sender_token = token_row[0]
                    print(f"[DEBUG] Found token for sender {sender}: {sender_token[:20]}...")
            
            # Fallback: Try admin token
            if not sender_token:
                cur.execute(
                    "SELECT token FROM access_tokens WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                    (ADMIN_USER_ID,)
                )
                token_row = cur.fetchone()
                sender_token = token_row[0] if token_row else None
                if sender_token:
                    print(f"[DEBUG] Using admin token as fallback")
            
            cur.close()
            conn.close()
        except Exception as token_error:
            print(f"[WARN] Could not get sender token: {token_error}")
            sender_token = None
        
        # Forward request to Matrix Synapse with headers
        headers = {
            'User-Agent': 'Cravex-Admin-Panel/1.0'
        }
        if sender_token:
            headers['Authorization'] = f'Bearer {sender_token}'
            print(f"[DEBUG] Using sender token for authentication: {sender_token[:20]}...")
        else:
            print(f"[WARN] No token found - trying without authentication")
        
        response = requests.get(thumbnail_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
        
        if response.status_code == 200:
            # Get content type from response
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            
            # Stream the response
            def generate():
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
            
            return Response(
                generate(),
                mimetype=content_type,
                headers={
                    'Cache-Control': 'public, max-age=3600',
                    'Access-Control-Allow-Origin': '*'
                }
            )
        else:
            error_text = response.text[:500] if hasattr(response, 'text') else str(response.content[:500])
            print(f"[WARN] Thumbnail download failed: {response.status_code}")
            print(f"[WARN] Response text: {error_text}")
            print(f"[WARN] Request URL: {thumbnail_url}")
            
            # Try alternative URL format (without server_name in path) or fallback to download
            if response.status_code == 404:
                # Try download endpoint as fallback
                download_url = f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}'
                print(f"[DEBUG] Trying download endpoint as fallback: {download_url}")
                alt_response = requests.get(download_url, stream=True, timeout=30, allow_redirects=True, headers=headers)
                if alt_response.status_code == 200:
                    content_type = alt_response.headers.get('Content-Type', 'image/jpeg')
                    def generate():
                        for chunk in alt_response.iter_content(chunk_size=8192):
                            if chunk:
                                yield chunk
                    return Response(
                        generate(),
                        mimetype=content_type,
                        headers={
                            'Cache-Control': 'public, max-age=3600',
                            'Access-Control-Allow-Origin': '*'
                        }
                    )
            
            return jsonify({
                'errcode': 'M_NOT_FOUND',
                'error': f'Thumbnail not found: {response.status_code}',
                'details': error_text,
                'requested_url': thumbnail_url
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"[HATA] Thumbnail proxy error: {str(e)}")
        return jsonify({
            'errcode': 'M_UNKNOWN',
            'error': f'Thumbnail proxy error: {str(e)}'
        }), 500
    except Exception as e:
        print(f"[HATA] Thumbnail proxy error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'errcode': 'M_UNKNOWN',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("")
    print("=" * 60)
    print("  🛡️  CRAVEX ADMIN PANEL")
    print("=" * 60)
    print("")
    print("URL: http://localhost:9000")
    print("")
    print("📋 Giriş Bilgileri:")
    print("   Kullanıcı: admin")
    print("   Şifre: admin123")
    print("")
    print("✨ Özellikler:")
    print("   ✅ Güvenli login sistemi")
    print("   ✅ Minimal dark theme")
    print("   ✅ FontAwesome ikonlar")
    print("   ✅ Sayfalama (50 mesaj/sayfa)")
    print("   ✅ Gelişmiş filtreleme")
    print("   ✅ JSON/CSV export")
    print("")
    print("Durdurmak için: Ctrl+C")
    print("=" * 60)
    print("")
    
    port = int(os.getenv('PORT', '9000'))
    app.run(host='0.0.0.0', port=port, debug=False)
