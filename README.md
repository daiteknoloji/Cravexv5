# 🚀 Matrix Synapse Full Stack - Cravex v5

Tam özellikli, şifreleme devre dışı bırakılmış, admin denetimli Matrix mesajlaşma sistemi.

## 📋 İçerik

- **Matrix Synapse** - Backend mesajlaşma sunucusu
- **Element Web** - Modern mesajlaşma arayüzü
- **Synapse Admin Panel** - Yönetim paneli
- **PostgreSQL** - Veritabanı
- **Redis** - Cache
- **Auto-Add System** - Otomatik admin ekleme servisi

## 🎯 Özellikler

### ✅ Şifreleme Devre Dışı
- Tüm yeni odalar şifresiz oluşur
- Admin tüm mesajları görebilir
- Database'den tam erişim

### ✅ Otomatik Admin Ekleme
- Her 60 saniyede yeni odaları kontrol eder
- Public odalara admin'i otomatik ekler
- Private odalar için uyarı verir

### ✅ Tam Yönetim
- Synapse Admin Panel (Web UI)
- PowerShell scriptleri
- SQL database erişimi

## 🖥️ Sistem Gereksinimleri

- Windows 10/11
- Docker Desktop
- Node.js v20+
- Yarn
- PostgreSQL (Docker ile)
- PowerShell 5.1+

## 🚀 Kurulum

### 1. Önkoşullar

```powershell
# Docker Desktop'i başlat
# Node.js ve Yarn kurulu olmalı
```

### 2. Backend Kurulum

```powershell
# Tüm servisleri başlat
.\BASLAT.ps1
```

### 3. Frontend Kurulum

Element Web ve Synapse Admin otomatik başlayacak.

## 🌐 Erişim Bilgileri

| Servis | URL | Açıklama |
|--------|-----|----------|
| **Element Web** | http://localhost:8080 | Mesajlaşma arayüzü |
| **Synapse Admin** | http://localhost:5173 | Yönetim paneli |
| **Docker Admin** | http://localhost:8082 | Web admin panel |
| **Backend API** | http://localhost:8008 | Matrix Synapse API |

## 🔐 Giriş Bilgileri

```
Username: admin
Password: Admin@2024!Guclu
Homeserver: http://localhost:8008
```

## 📜 Kullanım

### Tüm Servisleri Başlat
```powershell
.\BASLAT.ps1
```

### Auto-Add Servisini Başlat
```powershell
.\AUTO-ADD-ADMIN.ps1
```

### Durumu Kontrol Et
```powershell
.\DURUM.ps1
```

### Tümünü Durdur
```powershell
.\DURDUR.ps1
```

## 📊 Database Sorguları

### Son Mesajları Gör
```powershell
.\db-query-messages.ps1 -Query last -Limit 20
```

### Belirli Odanın Mesajları
```powershell
.\db-query-messages.ps1 -Query room -RoomId "!abc:localhost"
```

### Kelime Ara
```powershell
.\db-query-messages.ps1 -Query search -Search "test"
```

## 🛠️ Scriptler

| Script | Açıklama |
|--------|----------|
| `BASLAT.ps1` | Tüm servisleri başlatır |
| `DURDUR.ps1` | Tüm servisleri durdurur |
| `DURUM.ps1` | Durum kontrolü |
| `AUTO-ADD-ADMIN.ps1` | Yeni odalara admin ekler |
| `get-all-messages.ps1` | Tüm mesajları export eder |
| `get-room-messages.ps1` | Belirli odanın mesajlarını alır |
| `force-add-admin-to-room.ps1` | Admin'i zorla odaya ekler |
| `db-query-messages.ps1` | Database sorgulama |
| `LIST-ENCRYPTED-ROOMS.ps1` | Şifreli odaları listeler |
| `CHECK-ENCRYPTED-ROOMS-ALERT.ps1` | Şifreli oda uyarı sistemi |

## 📁 Dosya Yapısı

```
.
├── docker-compose.yml          # Backend yapılandırması
├── synapse-config/
│   └── homeserver.yaml        # Synapse ayarları
├── www/
│   ├── admin/                 # Synapse Admin (Port 5173)
│   └── element-web/           # Element Web (Port 8080)
│       └── config.json        # Element yapılandırması
├── BASLAT.ps1                # Ana başlatma
├── AUTO-ADD-ADMIN.ps1        # Otomatik admin ekleme
└── *.ps1                     # Diğer yardımcı scriptler
```

## 🔒 Güvenlik Notları

### ⚠️ ÖNEMLİ

Bu sistem **LOCAL DEVELOPMENT** içindir!

**Production için:**
- Tüm şifreleri değiştir
- HTTPS/TLS ekle
- Firewall ayarla
- Domain kullan
- Email servisi yapılandır
- Backup stratejisi oluştur

## 🎯 Şifreleme Politikası

### Sistem Ayarları:
- ✅ Şifreleme default **KAPALI**
- ✅ Tüm yeni odalar **şifresiz**
- ✅ Admin **tüm mesajları** görebilir
- ❌ End-to-end encryption **devre dışı**

### Kullanıcı Kuralı:
```
⚠️ UYARI: "Uçtan uca şifrelemeyi etkinleştir" seçeneğini AÇMAYIN!
Açarsanız:
- Mesajlar decrypt edilemez
- Admin göremez
- Oda silinebilir
```

## 📊 Database Yapısı

### Önemli Tablolar:
- `events` - Tüm mesajlar ve event'ler
- `rooms` - Oda bilgileri
- `users` - Kullanıcı bilgileri
- `room_memberships` - Kullanıcı-oda ilişkileri

### PostgreSQL Bağlantı:
```bash
docker exec -it matrix-postgres psql -U synapse_user -d synapse
```

## 🤖 Otomatik Sistemler

### Auto-Add Servisi:
- Her 60 saniyede yeni odaları kontrol eder
- Public odalara admin'i otomatik ekler
- Private odaları loglar

### Şifreli Oda Uyarı Sistemi:
```powershell
.\CHECK-ENCRYPTED-ROOMS-ALERT.ps1
```
- Her 5 dakikada kontrol eder
- Şifreli oda bulunca Windows bildirimi gösterir

## 📝 Değişiklik Geçmişi

### v5.0 (1 Kasım 2025)
- ✅ Şifreleme tamamen devre dışı bırakıldı
- ✅ Auto-add servisi eklendi
- ✅ Element Web + Synapse Admin entegre edildi
- ✅ Database query scriptleri eklendi
- ✅ Şifreli oda uyarı sistemi eklendi

## 🆘 Sorun Giderme

### Backend başlamıyor
```powershell
docker logs matrix-synapse --tail 50
docker restart matrix-synapse
```

### Port zaten kullanımda
```powershell
.\DURDUR.ps1
netstat -ano | findstr :8080
```

### Element Web açılmıyor
```powershell
# Terminal'de "Compiled successfully" bekle
# Tarayıcıda F5 (yenile)
```

## 📚 Kaynaklar

- [Matrix Synapse Docs](https://element-hq.github.io/synapse/latest/)
- [Element Web](https://github.com/element-hq/element-web)
- [Synapse Admin](https://github.com/Awesome-Technologies/synapse-admin)

## 📞 Destek

Sorun yaşarsanız:
1. `.\DURUM.ps1` çalıştırın
2. `docker logs matrix-synapse` kontrol edin
3. `SISTEM-OZET.md` dosyasına bakın

## 📄 Lisans

Bu proje özel kullanım içindir.

---

**Son Güncelleme:** 1 Kasım 2025  
**Versiyon:** 5.0  
**Geliştirici:** Dai Teknoloji

