# 🚀 MATRIX MESAJLAŞMA SİSTEMİ - KOMPLE KILAVUZ

**Hazırlanma Tarihi:** 1 Kasım 2025  
**Sistem Sahibi:** Can Cakir  
**Konum:** C:\Users\Can Cakir\Desktop\www-backup

---

## 📋 İÇİNDEKİLER
1. [Sistemin Yapısı](#sistemin-yapısı)
2. [Kurulu Servisler](#kurulu-servisler)
3. [Erişim Bilgileri](#erişim-bilgileri)
4. [Kullanıcı Tipleri](#kullanıcı-tipleri)
5. [Oda Tipleri](#oda-tipleri)
6. [Başlatma/Durdurma Komutları](#başlatmadurdurma-komutları)
7. [Mesajlaşma Nasıl Çalışır](#mesajlaşma-nasıl-çalışır)
8. [Admin Yetkileri](#admin-yetkileri)
9. [Dosya Yapısı](#dosya-yapısı)
10. [Sorun Giderme](#sorun-giderme)

---

## 🏗️ SİSTEMİN YAPISI

```
┌─────────────────────────────────────────────────────────┐
│                    KULLANICILAR                         │
│  (1k, 2k, admin, vb. - Tarayıcıdan bağlanır)           │
└─────────────────────────────────────────────────────────┘
                          ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (Kullanıcı Arayüzü)               │
│  ┌──────────────────┐    ┌──────────────────┐          │
│  │  ELEMENT WEB     │    │  SYNAPSE ADMIN   │          │
│  │  Port: 8080      │    │  Port: 5173      │          │
│  │  Mesajlaşma UI   │    │  Yönetim Paneli  │          │
│  └──────────────────┘    └──────────────────┘          │
└─────────────────────────────────────────────────────────┘
                          ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              BACKEND (Sunucu Tarafı)                    │
│  ┌──────────────────────────────────────────┐           │
│  │      MATRIX SYNAPSE                      │           │
│  │      Port: 8008                          │           │
│  │      Ana Mesajlaşma Sunucusu            │           │
│  └──────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
                          ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              VERİTABANI & CACHE                         │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │ POSTGRESQL   │  │    REDIS     │                    │
│  │ Port: 5432   │  │  Port: 6379  │                    │
│  │ Veri Deposu  │  │  Önbellek    │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
                          ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              OTOMATIK SERVİSLER                         │
│  ┌──────────────────────────────────────────┐           │
│  │   AUTO-ADD ADMIN SERVİSİ                 │           │
│  │   Her 60 saniyede yeni odaları kontrol  │           │
│  │   Admin'i otomatik ekler                │           │
│  └──────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

---

## 🖥️ KURULU SERVİSLER

| # | Servis Adı | Port | Çalışma Yeri | Ne İşe Yarar | Durum |
|---|------------|------|--------------|--------------|-------|
| 1 | **Matrix Synapse** | 8008 | Docker Container | Ana mesajlaşma sunucusu (backend) | ✅ Çalışıyor |
| 2 | **PostgreSQL** | 5432 | Docker Container | Veritabanı (kullanıcılar, mesajlar, odalar) | ✅ Çalışıyor |
| 3 | **Redis** | 6379 | Docker Container | Önbellek (hız için) | ✅ Çalışıyor |
| 4 | **Element Web** | 8080 | Node.js (Terminal) | Mesajlaşma arayüzü (WhatsApp gibi) | ✅ Çalışıyor |
| 5 | **Synapse Admin** | 5173 | Node.js (Terminal) | Yönetim paneli (kullanıcı/oda yönetimi) | ✅ Çalışıyor |
| 6 | **Docker Admin Panel** | 8082 | Docker Container | Web tabanlı admin paneli | ✅ Çalışıyor |
| 7 | **Auto-Add Servisi** | - | PowerShell Script | Yeni odalara admin'i otomatik ekler | ✅ Çalışıyor |

---

## 🌐 ERİŞİM BİLGİLERİ

### 📱 ELEMENT WEB (Mesajlaşma)
```
URL: http://localhost:8080
Kullanım: Mesaj gönderme, oda oluşturma, sohbet
Giriş: Herhangi bir kullanıcı (1k, 2k, admin, vb.)
```

### 🛠️ SYNAPSE ADMIN (Yönetim Paneli)
```
URL: http://localhost:5173
Kullanım: Kullanıcı yönetimi, oda yönetimi, mesaj okuma
Giriş: Sadece admin kullanıcısı
  - Username: @admin:localhost
  - Password: Admin@2024!Guclu
  - Homeserver: http://localhost:8008
```

### 🐳 DOCKER ADMIN PANEL
```
URL: http://localhost:8082
Kullanım: Web tabanlı yönetim (alternatif)
Giriş: Admin bilgileri ile
```

### 🔧 BACKEND API
```
URL: http://localhost:8008
Kullanım: Doğrudan API çağrıları (gelişmiş)
Erişim: Token ile
```

---

## 👥 KULLANICI TİPLERİ

| Kullanıcı Adı | Matrix ID | Şifre | Yetki | Ne Yapabilir |
|--------------|-----------|-------|-------|--------------|
| **admin** | @admin:localhost | Admin@2024!Guclu | 🔴 Admin | - Tüm odaları görebilir<br>- Kullanıcı ekle/sil<br>- Oda yönetimi<br>- Mesajları okuyabilir<br>- Sistem ayarları |
| **1k** | @1k:localhost | (şifre belirtilmemiş) | 🔵 Normal | - Mesaj gönderme<br>- Oda oluşturma<br>- Kendi odalarını yönetme |
| **2k** | @2k:localhost | (şifre belirtilmemiş) | 🔵 Normal | - Mesaj gönderme<br>- Oda oluşturma<br>- Kendi odalarını yönetme |

### 🆕 Yeni Kullanıcı Oluşturma

**Komut Satırından:**
```powershell
docker exec matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u KULLANICI_ADI -p SIFRE
```

**Admin Kullanıcı Oluşturma:**
```powershell
docker exec matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u KULLANICI_ADI -p SIFRE -a
```

**Synapse Admin Panelinden:**
1. http://localhost:5173 → Giriş yap
2. Users → Create
3. Bilgileri doldur → Kaydet

---

## 🏠 ODA TİPLERİ

| Oda Tipi | Link Olan Girebilir mi? | Onay Gerekli mi? | Oda Listesinde Görünür mü? | Auto-Add Çalışır mı? | Kullanım Senaryosu |
|----------|------------------------|------------------|---------------------------|---------------------|-------------------|
| **Public** | ✅ Direkt girer | ❌ Hayır | ✅ Evet | ✅ Evet | Genel sohbet, duyurular |
| **Private (Invite)** | ❌ Hayır | ✅ Davet gerekli | ❌ Hayır | ❌ Hayır* | Özel gruplar, gizli sohbetler |
| **Private (Knock)** | ⚠️ İstek gönderir | ✅ Admin onaylar | ❌ Hayır | ⚠️ DB Trigger ile** | Kontrollü giriş, moderasyon |
| **Şifreli (Encrypted)** | ⚠️ Duruma göre | ⚠️ Duruma göre | ⚠️ Duruma göre | ⚠️ Public ise evet | Güvenli iletişim |

**Notlar:**
- (*) Private odalar için admin'in davet edilmesi gerekir
- (**) Database trigger kurulursa çalışır

---

## 🚀 BAŞLATMA/DURDURMA KOMUTLARI

### ✅ HER ŞEYİ BAŞLAT

**Yöntem 1: Ana Servisler + Manuel Auto-Add**
```powershell
# 1. Ana servisleri başlat
& "C:\Users\Can Cakir\Desktop\www-backup\BASLAT.ps1"

# 2. 2 dakika bekle (backend hazır olsun)

# 3. Auto-add servisi başlat (yeni terminal)
& "C:\Users\Can Cakir\Desktop\www-backup\AUTO-ADD-ADMIN.ps1"
```

**Yöntem 2: Tek Komutla Her Şey (Otomatik)**
```powershell
& "C:\Users\Can Cakir\Desktop\www-backup\BASLAT-AUTO-ADD.ps1"
```

### 🛑 HER ŞEYİ DURDUR

```powershell
& "C:\Users\Can Cakir\Desktop\www-backup\DURDUR.ps1"
```

### 📊 DURUM KONTROLÜ

```powershell
& "C:\Users\Can Cakir\Desktop\www-backup\DURUM.ps1"
```

### 🔄 YENİDEN BAŞLAT

```powershell
# Önce durdur
.\DURDUR.ps1

# 5 saniye bekle
Start-Sleep -Seconds 5

# Tekrar başlat
.\BASLAT.ps1
```

---

## 💬 MESAJLAŞMA NASIL ÇALIŞIR?

### 1️⃣ KULLANICI GİRİŞİ
```
Kullanıcı → Element Web (http://localhost:8080) açar
         → Username/Password girer
         → Matrix Synapse giriş kontrolü yapar
         → Token oluşturur
         → Kullanıcı giriş yapar ✅
```

### 2️⃣ ODA OLUŞTURMA
```
Kullanıcı → Element Web'de "Create Room" tıklar
         → Oda tipi seçer (Public/Private)
         → Oda adı girer
         → Matrix Synapse odayı oluşturur
         → PostgreSQL'e kaydeder
         → Auto-Add Servisi yeni odayı bulur (60 saniye içinde)
         → Admin'i otomatik ekler ✅
```

### 3️⃣ MESAJ GÖNDERME
```
Kullanıcı → Element Web'de mesaj yazar
         → Send butonuna basar
         → Matrix Synapse mesajı alır
         → PostgreSQL'e kaydeder
         → Odadaki diğer kullanıcılara iletir (WebSocket)
         → Diğer kullanıcılar mesajı görür ✅
```

### 4️⃣ MESAJ OKUMA (Başka Kullanıcı)
```
Diğer Kullanıcı → Element Web açık
               → Matrix Synapse yeni mesaj bildirir (real-time)
               → Mesaj ekranda görünür ✅
```

### 5️⃣ ADMIN MESAJ OKUMA
```
Admin → Synapse Admin Panel (http://localhost:5173) açar
      → Rooms → Oda seçer
      → Show Events tıklar
      → Tüm mesajları görür ✅
```

**Alternatif (Komut Satırı):**
```powershell
.\get-room-messages.ps1 -RoomId "!ODAID:localhost"
```

---

## 👑 ADMIN YETKİLERİ

### 🔍 Admin Neler Yapabilir?

| Yetki | Nasıl Yapılır | Araç |
|-------|--------------|------|
| **Tüm odaları görme** | Synapse Admin → Rooms | Web Panel |
| **Tüm mesajları okuma** | Synapse Admin → Rooms → Show Events | Web Panel |
| **Kullanıcı ekleme/silme** | Synapse Admin → Users → Create/Delete | Web Panel |
| **Oda silme** | Synapse Admin → Rooms → Delete | Web Panel |
| **Kullanıcı banlama** | Synapse Admin → Users → Deactivate | Web Panel |
| **Mesaj geçmişi indirme** | `.\get-all-messages.ps1` | PowerShell |
| **Belirli odanın mesajlarını alma** | `.\get-room-messages.ps1 -RoomId "!xxx:localhost"` | PowerShell |
| **Admin'i odaya zorla ekleme** | `.\force-add-admin-to-room.ps1 -RoomId "!xxx:localhost"` | PowerShell |
| **Tüm odalara admin ekleme** | `.\add-admin-to-all-rooms.ps1` | PowerShell |

---

## 📁 DOSYA YAPISI

```
C:\Users\Can Cakir\Desktop\www-backup\
│
├── 📄 BASLAT.ps1                    ← Ana başlatma scripti
├── 📄 DURDUR.ps1                    ← Durdurma scripti
├── 📄 DURUM.ps1                     ← Durum kontrolü
├── 📄 BASLAT-AUTO-ADD.ps1           ← Her şeyi başlat (auto-add dahil)
├── 📄 AUTO-ADD-ADMIN.ps1            ← Otomatik admin ekleme servisi
├── 📄 FORCE-JOIN-ANY-ROOM.ps1       ← Zorla herhangi bir odaya admin ekle
│
├── 📄 get-admin-token.ps1           ← Admin token al
├── 📄 get-all-messages.ps1          ← Tüm mesajları indir
├── 📄 get-room-messages.ps1         ← Belirli odanın mesajlarını al
├── 📄 add-admin-to-room.ps1         ← Admin'i odaya ekle
├── 📄 force-add-admin-to-room.ps1   ← Admin'i zorla ekle (admin API)
├── 📄 add-admin-to-all-rooms.ps1    ← Tüm odalara admin ekle
│
├── 📄 docker-compose.yml            ← Backend yapılandırması
├── 📄 .env                          ← Şifreler ve ortam değişkenleri
│
├── 📂 synapse-config\
│   ├── homeserver.yaml              ← Synapse ana ayarları
│   └── localhost.log.config         ← Log ayarları
│
├── 📂 www\
│   ├── 📂 admin\                    ← Synapse Admin Panel (Port 5173)
│   │   ├── package.json
│   │   ├── src\
│   │   └── public\config.json
│   │
│   └── 📂 element-web\              ← Element Web (Port 8080)
│       ├── package.json
│       ├── config.json              ← Homeserver ayarları
│       └── src\
│
└── 📄 SISTEM-OZET.md                ← Bu dosya (sistem dokümantasyonu)
```

---

## 🎯 KULLANIM SENARYOLARI

### 🔹 Senaryo 1: Normal Kullanıcı Mesaj Gönderme

```
1. Element Web aç: http://localhost:8080
2. Kullanıcı adı ile giriş yap (örn: 1k)
3. Sol taraftan oda seç VEYA yeni oda oluştur
4. Mesaj yaz ve gönder
5. Diğer kullanıcılar mesajı görür
```

### 🔹 Senaryo 2: Admin Tüm Mesajları Görme

```
1. Synapse Admin aç: http://localhost:5173
2. Admin giriş: @admin:localhost / Admin@2024!Guclu
3. Rooms menüsüne git
4. İstediğin odayı seç
5. "Show Events" tıkla
6. Tüm mesajları ve event'leri gör
```

### 🔹 Senaryo 3: Yeni Kullanıcı Ekleme

```
Yöntem A (Web):
1. Synapse Admin → Users → Create
2. Username, Password gir
3. Admin yetkisi verilsin mi? (Evet/Hayır)
4. Save

Yöntem B (Komut):
docker exec matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u KULLANICI_ADI -p SIFRE
```

### 🔹 Senaryo 4: Public Oda Oluşturma (Auto-Add İçin)

```
1. Element Web → Create Room
2. Room name: "Test Room"
3. Room visibility: PUBLIC ✅
4. Enable encryption: OFF ✅
5. Create
6. 60 saniye bekle
7. Admin otomatik eklenir! ✅
```

### 🔹 Senaryo 5: Mesajları JSON'a Aktarma

```powershell
# Tüm mesajları al
.\get-all-messages.ps1

# Çıktı: all-messages_20251101_203045.json

# Belirli odanın mesajlarını al
.\get-room-messages.ps1 -RoomId "!dpJrFkREUMoGwNJRQu:localhost"

# Çıktı: room_messages_dpJrFkREUMoGwNJRQudpJrFkREUMoGwNJRQu_20251101_203045.json
```

---

## 🔧 VERİTABANI BİLGİLERİ

### PostgreSQL Bağlantı Bilgileri
```
Host: localhost (Docker içinde: postgres)
Port: 5432
Database: synapse
Username: synapse_user
Password: SuperGucluSifre2024!
```

### Veritabanına Bağlanma
```powershell
# PostgreSQL shell'e gir
docker exec -it matrix-postgres psql -U synapse_user -d synapse

# Kullanıcıları listele
\dt users

# Odaları listele
SELECT room_id, name FROM rooms;

# Mesajları listele (son 10)
SELECT sender, type, content FROM events ORDER BY stream_ordering DESC LIMIT 10;
```

### Önemli Tablolar
| Tablo Adı | Ne Tutar |
|-----------|----------|
| `users` | Kullanıcı bilgileri |
| `rooms` | Oda bilgileri |
| `events` | Mesajlar ve event'ler |
| `room_memberships` | Kullanıcı-oda ilişkileri |
| `device_lists_stream` | Cihaz listesi |

---

## ⚠️ SORUN GİDERME

### ❌ "Backend'e bağlanılamıyor"
```
SORUN: Synapse çalışmıyor
ÇÖZÜM:
1. docker ps -a
2. matrix-synapse container'ını kontrol et
3. docker logs matrix-synapse --tail 50
4. docker restart matrix-synapse
```

### ❌ "Port zaten kullanımda"
```
SORUN: 8080, 5173 portları dolu
ÇÖZÜM:
1. .\DURDUR.ps1 çalıştır
2. netstat -ano | findstr :8080
3. PID'yi bul
4. taskkill /PID XXXX /F
```

### ❌ "Element Web açılmıyor"
```
SORUN: Frontend başlamadı
ÇÖZÜM:
1. Terminal'de "Compiled successfully" bekle
2. http://localhost:8080 aç
3. F12 → Console → Hata kontrolü
4. www\element-web\config.json dosyası var mı kontrol et
```

### ❌ "Admin mesajları göremiyorsun"
```
SORUN: Admin odaya üye değil
ÇÖZÜM:
.\force-add-admin-to-room.ps1 -RoomId "!ODAID:localhost"
```

### ❌ "Auto-add çalışmıyor"
```
SORUN: Script hata veriyor
KONTROL:
1. Backend çalışıyor mu? http://localhost:8008/health
2. Auto-add terminali açık mı?
3. Terminal'de hata mesajı var mı?

ÇÖZÜM:
Ctrl+C ile durdur, .\AUTO-ADD-ADMIN.ps1 ile tekrar başlat
```

---

## 📊 SİSTEM GEREKSİNİMLERİ

### Minimum:
- **OS:** Windows 10/11
- **RAM:** 4GB
- **Disk:** 10GB boş
- **Docker Desktop:** Kurulu ve çalışıyor
- **Node.js:** v20+ (Element Web için)
- **Yarn:** Kurulu

### Önerilen:
- **RAM:** 8GB+
- **Disk:** 20GB (SSD)
- **CPU:** 4 çekirdek

---

## 🔐 GÜVENLİK NOTLARI

### ⚠️ ÖNEMLİ!
Bu yapılandırma **LOCAL DEVELOPMENT** içindir.

### Production İçin Yapılması Gerekenler:
1. ✅ Tüm şifreleri değiştir (homeserver.yaml, .env)
2. ✅ HTTPS/TLS ekle
3. ✅ Firewall ayarla
4. ✅ Domain kullan (localhost yerine)
5. ✅ Email servisi yapılandır
6. ✅ Backup stratejisi oluştur
7. ✅ Log rotation
8. ✅ Monitoring (Prometheus, Grafana)
9. ✅ Rate limiting sıkılaştır
10. ✅ Admin şifrelerini güçlendir

---

## 📞 YARDIM ve KAYNAKLAR

### Resmi Dokümantasyon:
- Matrix Synapse: https://element-hq.github.io/synapse/latest/
- Element Web: https://github.com/element-hq/element-web
- Matrix Protokolü: https://matrix.org/docs/

### Scriptler:
| Script | Ne İşe Yarar |
|--------|--------------|
| `BASLAT.ps1` | Her şeyi başlatır |
| `DURDUR.ps1` | Her şeyi durdurur |
| `AUTO-ADD-ADMIN.ps1` | Yeni odalara admin ekler (60 saniyede bir) |
| `get-all-messages.ps1` | Tüm mesajları JSON'a aktarır |

---

## 📝 DEĞİŞİKLİK GEÇMİŞİ

| Tarih | Değişiklik |
|-------|-----------|
| 1 Kasım 2025 | İlk kurulum - Tüm servisler ayarlandı |
| 1 Kasım 2025 | Auto-add servisi eklendi |
| 1 Kasım 2025 | Element Web + Synapse Admin entegre edildi |
| 1 Kasım 2025 | Şifreleme devre dışı bırakıldı (admin mesaj okusun) |

---

## ✅ HIZLI REFERANS

### Başlatma (Kısa)
```powershell
.\BASLAT.ps1
.\AUTO-ADD-ADMIN.ps1
```

### Erişim (Kısa)
```
Element Web: http://localhost:8080
Admin Panel: http://localhost:5173
```

### Giriş (Kısa)
```
Admin: @admin:localhost / Admin@2024!Guclu
```

### Durdurma (Kısa)
```powershell
.\DURDUR.ps1
```

---

**Son Güncelleme:** 1 Kasım 2025  
**Hazırlayan:** AI Assistant (Claude)  
**Sistem Sahibi:** Can Cakir


