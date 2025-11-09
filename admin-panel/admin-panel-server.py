#!/usr/bin/env python3
"""
Cravex Admin Panel - Enterprise Edition
========================================
Port: 9000
URL: http://localhost:9000
Login: admin / admin123
"""

from flask import Flask, render_template_string, jsonify, request, send_file, session, redirect, url_for
import psycopg2
from datetime import datetime
import json
import csv
import io
from functools import wraps

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
                """Convert MXC URL to HTTP URL"""
                if not mxc_url or not mxc_url.startswith('mxc://'):
                    return None
                
                # Parse mxc://server.com/media_id
                mxc_path = mxc_url.replace('mxc://', '')
                if '/' not in mxc_path:
                    return None
                
                server_name, media_id = mxc_path.split('/', 1)
                
                if use_thumbnail:
                    # Thumbnail endpoint with size parameters
                    return f'{synapse_url}/_matrix/media/r0/thumbnail/{server_name}/{media_id}?width=800&height=600&method=scale'
                else:
                    # Download endpoint
                    return f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}'
            
            if media_url:
                media_http_url = mxc_to_http(media_url, use_thumbnail=False)
            
            if thumbnail_url:
                thumbnail_http_url = mxc_to_http(thumbnail_url, use_thumbnail=True)
            elif media_url:
                # If no thumbnail_url but we have media_url, use thumbnail endpoint for images
                if msgtype == 'm.image':
                    thumbnail_http_url = mxc_to_http(media_url, use_thumbnail=True)
            
            messages.append({
                'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S') if row[0] else '',
                'sender': sender,
                'room_id': room_id,
                'room_name': room_name,
                'message': row[4],
                'msgtype': msgtype,
                'media_url': media_url,
                'media_http_url': media_http_url,
                'thumbnail_url': thumbnail_url,
                'thumbnail_http_url': thumbnail_http_url,
                'mimetype': mimetype,
                'file_size': int(file_size) if file_size else None,
                'image_width': int(image_width) if image_width else None,
                'image_height': int(image_height) if image_height else None,
                'recipient': recipient_display,
                'recipient_list': recipient_full_list,
                'is_deleted': is_deleted,
                'deleted_by': row[13] if is_deleted else None,
                'event_id': row[14]
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
                """Convert MXC URL to HTTP URL"""
                if not mxc_url or not mxc_url.startswith('mxc://'):
                    return None
                
                # Parse mxc://server.com/media_id
                mxc_path = mxc_url.replace('mxc://', '')
                if '/' not in mxc_path:
                    return None
                
                server_name, media_id = mxc_path.split('/', 1)
                
                if use_thumbnail:
                    # Thumbnail endpoint with size parameters
                    return f'{synapse_url}/_matrix/media/r0/thumbnail/{server_name}/{media_id}?width=800&height=600&method=scale'
                else:
                    # Download endpoint
                    return f'{synapse_url}/_matrix/media/r0/download/{server_name}/{media_id}'
            
            if media_url:
                media_http_url = mxc_to_http(media_url, use_thumbnail=False)
            
            if thumbnail_url:
                thumbnail_http_url = mxc_to_http(thumbnail_url, use_thumbnail=True)
            elif media_url:
                # If no thumbnail_url but we have media_url, use thumbnail endpoint for images
                if msgtype == 'm.image':
                    thumbnail_http_url = mxc_to_http(media_url, use_thumbnail=True)
            
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
        
        # Step 2: First try to INVITE the user (so they get notification)
        try:
            # Use Client API to invite (sends notification)
            invite_url = f'{synapse_url}/_matrix/client/r0/rooms/{room_id}/invite'
            invite_payload = {'user_id': user_id}
            
            print(f"[1] Sending invite to {user_id} in room {room_id}...")
            invite_response = requests.post(invite_url, headers=headers, json=invite_payload, timeout=5)
            print(f"[1] Invite result: {invite_response.status_code} - {invite_response.text[:200]}")
            
            if invite_response.status_code == 200:
                # Invite successful - now auto-accept by joining them
                print(f"[2] Now force-joining {user_id}...")
                join_url = f'{synapse_url}/_synapse/admin/v1/join/{room_id}'
                join_response = requests.post(join_url, headers=headers, json={'user_id': user_id}, timeout=5)
                print(f"[2] Force-join result: {join_response.status_code} - {join_response.text[:200]}")
                
                if join_response.status_code == 200:
                    return jsonify({
                        'message': f'✅ {user_id} added and joined! Refresh Element Web to see.',
                        'success': True,
                        'method': 'matrix_api'
                    })
                else:
                    # Invite sent but couldn't force join
                    return jsonify({
                        'message': f'📧 Invite sent to {user_id}! They need to accept in Element Web.',
                        'success': True,
                        'method': 'invite_only'
                    })
            
            # If invite failed, try direct admin join
            print(f"[3] Invite failed, trying direct admin join...")
            api_url = f'{synapse_url}/_synapse/admin/v1/join/{room_id}'
            response = requests.post(api_url, headers=headers, json={'user_id': user_id}, timeout=5)
            print(f"[3] Direct join result: {response.status_code} - {response.text[:200]}")
            
            if response.status_code == 200:
                return jsonify({
                    'message': f'✅ {user_id} force-joined! Refresh Element Web.',
                    'success': True,
                    'method': 'admin_join'
                })
            elif response.status_code == 403:
                # 403 means admin doesn't have permission - often happens in DM/private rooms
                # Fallback: Try database insert (won't sync immediately but works)
                print(f"Matrix API 403, trying database fallback...")
                
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
                        'message': f'Member added via database (bypass). User may need to refresh Element Web to see the room.',
                        'method': 'database',
                        'note': 'Added directly to database - real-time sync may not work immediately'
                    })
                    
                except Exception as db_err:
                    print(f"Database fallback also failed: {db_err}")
                    return jsonify({
                        'error': f'Cannot add member. This is a private DM room and admin cannot force join.',
                        'success': False,
                        'suggestion': 'Ask existing room members to invite the user via Element Web.'
                    }), 403
            else:
                return jsonify({
                    'error': f'Matrix API error: {response.status_code}',
                    'success': False,
                    'details': response.text
                }), response.status_code
                
        except Exception as api_error:
            print(f"Matrix API error: {api_error}")
            return jsonify({
                'error': f'Failed to add member via Matrix API: {str(api_error)}',
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
        
        return jsonify({
            'user_id': user_row[0],
            'admin': bool(user_row[1]),
            'created': datetime.fromtimestamp(user_row[2]).strftime('%Y-%m-%d %H:%M:%S') if user_row[2] else '',
            'deactivated': bool(user_row[3]),
            'shadow_banned': bool(user_row[4]) if user_row[4] is not None else False,
            'locked': bool(user_row[5]) if user_row[5] is not None else False,
            'last_seen': datetime.fromtimestamp(last_seen/1000).strftime('%Y-%m-%d %H:%M:%S') if last_seen else 'Hiç görülmedi',
            'rooms': [{'room_id': r[0], 'name': r[1] or 'İsimsiz Oda', 'member_count': r[2]} for r in rooms],
            'devices': [{'device_id': d[0], 'last_seen': datetime.fromtimestamp(d[1]/1000).strftime('%Y-%m-%d %H:%M:%S') if d[1] else 'Bilinmiyor', 'ip': d[2], 'user_agent': d[3]} for d in devices]
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
                    print(f"[WARN] Matrix API password change failed: {response.status_code} - {response.text[:200]}")
                    # Fallback to database method
            
            # Fallback: Database method
            print(f"[INFO] Using database fallback for password change...")
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Hash password with bcrypt
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Update password in database
            cur.execute("""
                UPDATE users SET password_hash = %s WHERE name = %s
            """, (password_hash, user_id))
            
            conn.commit()
            affected_rows = cur.rowcount
            cur.close()
            conn.close()
            
            if affected_rows > 0:
                return jsonify({
                    'success': True,
                    'message': f'Şifre başarıyla değiştirildi (Database)',
                    'method': 'database'
                })
            else:
                return jsonify({'error': 'Kullanıcı bulunamadı', 'success': False}), 404
                
        except Exception as api_error:
            print(f"[ERROR] Password change error: {api_error}")
            return jsonify({'error': f'Şifre değiştirilemedi: {str(api_error)}', 'success': False}), 500
        
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
                        print(f"[ERROR] Falling back to database method to ensure password works...")
                        # Don't return, continue to database fallback
                    else:
                        return jsonify({
                            'success': True,
                            'user_id': user_id,
                            'message': 'User created successfully via Matrix API!',
                            'method': 'matrix_api'
                        })
                else:
                    print(f"[WARN] Synapse API failed with {response.status_code}, falling back to database")
                    print(f"[WARN] Error details: {response.text[:200]}")
        except Exception as api_error:
            print(f"[INFO] Matrix API not available, using database fallback: {api_error}")
        
        # Fallback: Direct database insert (for Railway or when Matrix API is unavailable)
        import bcrypt
        import time
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT name, password_hash FROM users WHERE name = %s", (user_id,))
        existing_user = cur.fetchone()
        if existing_user:
            # User exists - check if password needs to be updated
            existing_hash = existing_user[1]
            print(f"[INFO] User {user_id} already exists in database")
            print(f"[INFO] Existing password hash: {existing_hash[:30] if existing_hash else 'NULL'}...")
            
            # If password hash is NULL or empty, update it
            if not existing_hash:
                print(f"[INFO] User exists but has no password hash. Updating password...")
                salt = bcrypt.gensalt(rounds=12)
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
                cur.execute("UPDATE users SET password_hash = %s WHERE name = %s", (password_hash, user_id))
                conn.commit()
                cur.close()
                conn.close()
                return jsonify({
                    'success': True,
                    'user_id': user_id,
                    'message': 'User already exists - password hash updated!',
                    'method': 'database_update'
                })
            else:
                cur.close()
                conn.close()
                return jsonify({'error': 'User already exists', 'success': False}), 409
        
        # Hash password (bcrypt with 12 rounds - same as Synapse)
        # IMPORTANT: Use gensalt(rounds=12) to match Synapse's default
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        print(f"[DEBUG] Created user {user_id} with password hash: {password_hash[:30]}...")
        print(f"[DEBUG] Password hash length: {len(password_hash)}, starts with: {password_hash[:7]}")
        
        # Insert user (with all required columns)
        # Synapse uses milliseconds for creation_ts
        creation_ts = int(time.time() * 1000)  # Convert to milliseconds
        
        # Check which columns exist in users table
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('locked', 'suspended', 'approved', 'shadow_banned')
        """)
        existing_user_cols = [row[0] for row in cur.fetchall()]
        has_locked = 'locked' in existing_user_cols
        has_suspended = 'suspended' in existing_user_cols
        has_approved = 'approved' in existing_user_cols
        has_shadow_banned = 'shadow_banned' in existing_user_cols
        
        # Build INSERT query with available columns
        base_cols = "name, password_hash, creation_ts, admin, is_guest, deactivated"
        base_vals = "%s, %s, %s, %s, 0, 0"
        params = [user_id, password_hash, creation_ts, 1 if make_admin else 0]
        
        if has_locked:
            base_cols += ", locked"
            base_vals += ", %s"
            params.append(False)
        if has_suspended:
            base_cols += ", suspended"
            base_vals += ", %s"
            params.append(False)
        if has_approved:
            base_cols += ", approved"
            base_vals += ", %s"
            params.append(True)
        if has_shadow_banned:
            base_cols += ", shadow_banned"
            base_vals += ", %s"
            params.append(False)
        
        insert_query = f"""
            INSERT INTO users ({base_cols})
            VALUES ({base_vals})
        """
        
        cur.execute(insert_query, tuple(params))
        
        # Create profile (required for Matrix)
        display_name_value = displayname if displayname else username
        cur.execute("""
            INSERT INTO profiles (user_id, displayname, full_user_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET displayname = EXCLUDED.displayname, full_user_id = EXCLUDED.full_user_id
        """, (user_id, display_name_value, user_id))
        
        # Add to user_directory (CRITICAL for login!)
        cur.execute("""
            INSERT INTO user_directory (user_id, display_name, avatar_url)
            VALUES (%s, %s, NULL)
            ON CONFLICT (user_id) DO UPDATE SET display_name = EXCLUDED.display_name
        """, (user_id, display_name_value))
        
        # Add to user_directory_search (for search functionality)
        # Build search vector: lowercase username and display name
        search_vector = f"'{HOMESERVER_DOMAIN}':2 '{username.lower()}':1A,3B"
        cur.execute("""
            INSERT INTO user_directory_search (user_id, vector)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET vector = EXCLUDED.vector
        """, (user_id, search_vector))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User created successfully via database! ⚠️ User will need to login in Element Web.',
            'note': 'Created directly in database - may need Synapse restart for full sync'
        })
        
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
