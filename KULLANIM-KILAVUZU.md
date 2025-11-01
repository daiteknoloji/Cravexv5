# 🚀 MATRIX FULL STACK - KULLANIM KILAVUZU

Bu proje **Matrix Synapse** backend + **Element Web** + **Synapse Admin** içeren tam bir mesajlaşma platformudur.

---

## 📋 İÇERİK

### Backend (Docker):
- **Matrix Synapse** - Ana sunucu (Port: 8008)
- **PostgreSQL** - Veritabanı (Port: 5432)
- **Redis** - Cache (Port: 6379)
- **Synapse Admin** - Docker admin panel (Port: 8082)

### Frontend (Node.js):
- **Element Web** - Mesajlaşma arayüzü (Port: 8080)
- **Synapse Admin** - Yönetim paneli (Port: 5173)

---

## 🎮 HIZLI BAŞLANGIÇ

### 1️⃣ HER ŞEYİ BAŞLAT
```powershell
.\BASLAT.ps1
```

**Ne yapar?**
- ✅ Docker Desktop'ı kontrol eder
- ✅ Backend container'larını başlatır (Synapse, PostgreSQL, Redis)
- ✅ Element Web'i başlatır (yeni terminal açar)
- ✅ Synapse Admin'i başlatır (yeni terminal açar)
- ✅ Tüm servislerin sağlığını kontrol eder

**Bekleme Süreleri:**
- Backend: ~10 saniye
- Element Web: ~30-60 saniye (ilk açılış)
- Synapse Admin: ~5-10 saniye

---

### 2️⃣ DURUMU KONTROL ET
```powershell
.\DURUM.ps1
```

**Ne gösterir?**
- ✅ Backend servislerin durumu
- ✅ Frontend servislerin durumu
- ✅ Tüm erişim URL'leri
- ✅ Veritabanı istatistikleri

---

### 3️⃣ HER ŞEYİ DURDUR
```powershell
.\DURDUR.ps1
```

**Ne yapar?**
- ✅ Frontend'leri durdurur (Port 8080, 5173)
- ✅ Backend container'larını durdurur

---

## 🌐 ERİŞİM ADRESLERİ

| Servis | URL | Açıklama |
|--------|-----|----------|
| **Element Web** | http://localhost:8080 | Mesajlaşma arayüzü (WhatsApp gibi) |
| **Synapse Admin** | http://localhost:5173 | Yönetim paneli (kullanıcı/oda yönetimi) |
| **Docker Admin** | http://localhost:8082 | Docker içindeki admin panel |
| **Backend API** | http://localhost:8008 | Matrix Synapse API |

---

## 🔐 GİRİŞ BİLGİLERİ

### Element Web'e Giriş:
```
URL: http://localhost:8080
Username: admin
Password: Admin@2024!Guclu
Homeserver: Otomatik yüklenir (config.json'da tanımlı)
```

### Synapse Admin'e Giriş:
```
URL: http://localhost:5173
Homeserver: http://localhost:8008
Username: @admin:localhost
Password: Admin@2024!Guclu
```

---

## 📁 DOSYA YAPISI

```
C:\Users\Can Cakir\Downloads\www-backup\
│
├── BASLAT.ps1              ← Tümünü başlat
├── DURDUR.ps1              ← Tümünü durdur
├── DURUM.ps1               ← Durum kontrol et
├── KULLANIM-KILAVUZU.md    ← Bu dosya
│
├── docker-compose.yml      ← Backend yapılandırması
├── .env                    ← Backend şifreleri
│
├── synapse-config/
│   ├── homeserver.yaml     ← Synapse ayarları
│   └── localhost.log.config
│
└── www/
    ├── admin/              ← Synapse Admin (Port 5173)
    │   ├── package.json
    │   └── src/
    │
    └── element-web/        ← Element Web (Port 8080)
        ├── package.json
        ├── config.json     ← Homeserver ayarları
        └── src/
```

---

## 🛠️ SORUN GİDERME

### Docker Desktop Çalışmıyor
```
HATA: Docker Desktop calismyor!
ÇÖZÜM: Windows menüsünden "Docker Desktop" uygulamasını başlat
```

### Port Zaten Kullanımda
```
HATA: Port 8080 zaten kullanımda
ÇÖZÜM: 
1. .\DURDUR.ps1 çalıştır
2. VEYA: netstat -ano | findstr :8080
3. Process ID'yi bul ve sonlandır: taskkill /PID <PID> /F
```

### Element Web Açılmıyor
```
HATA: Varsayılan sunucu belirtilmedi
ÇÖZÜM: config.json dosyası eksik
1. www/element-web/config.json dosyasının olduğunu kontrol et
2. Yoksa: .\restart-element.ps1 çalıştır
```

### Backend Bağlantı Hatası
```
HATA: Backend'e bağlanılamıyor
ÇÖZÜM:
1. Docker container'ları kontrol et: docker ps
2. Synapse loglarını kontrol et: docker logs matrix-synapse --tail 50
3. Health check: Invoke-WebRequest http://localhost:8008/health
```

### Yavaş Çalışıyor
```
İLK AÇILIŞ: Element Web ilk açılışta 30-60 saniye sürer (webpack build)
ÇÖZÜM: Sabırlı ol, terminal penceresinde "Compiled successfully" yazısını bekle
```

---

## 💾 VERİTABANI

### Veritabanı Konumu:
```
Docker Volume: www-backup_postgres_data
Fiziksel Path: /var/lib/docker/volumes/www-backup_postgres_data/_data
```

### Veritabanına Bağlan:
```powershell
# PostgreSQL shell'e gir
docker exec -it matrix-postgres psql -U synapse_user -d synapse

# Kullanıcıları listele
docker exec matrix-postgres psql -U synapse_user -d synapse -c "SELECT name FROM users;"

# Veritabanı boyutu
docker exec matrix-postgres psql -U synapse_user -d synapse -c "SELECT pg_size_pretty(pg_database_size('synapse'));"
```

### Backup Al:
```powershell
# Veritabanını yedekle
docker exec matrix-postgres pg_dump -U synapse_user synapse > backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql

# Geri yükle
docker exec -i matrix-postgres psql -U synapse_user synapse < backup_20251031_123456.sql
```

---

## 👥 YENİ KULLANICI OLUŞTUR

### Komut Satırından:
```powershell
# Normal kullanıcı
docker exec matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u kullanici_adi -p sifre123

# Admin kullanıcı
docker exec matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u admin2 -p sifre123 -a
```

### Synapse Admin Panel'den:
1. http://localhost:5173 aç
2. Giriş yap
3. **Users** menüsüne git
4. **Create** tıkla
5. Kullanıcı bilgilerini doldur

---

## 🔧 GELİŞMİŞ KOMUTLAR

### Docker Komutları:
```powershell
# Tüm container'ları göster
docker ps -a

# Logları izle
docker logs -f matrix-synapse

# Container'ı yeniden başlat
docker restart matrix-synapse

# Container'a shell ile gir
docker exec -it matrix-synapse /bin/bash

# Volume'leri listele
docker volume ls

# Volume'ü incele
docker volume inspect www-backup_postgres_data
```

### Node.js Komutları:
```powershell
# Element Web
cd www\element-web
yarn start              # Dev server başlat
yarn build             # Production build
yarn lint              # Kod kontrolü

# Synapse Admin
cd www\admin
yarn start              # Dev server başlat
yarn build             # Production build
yarn test              # Testleri çalıştır
```

---

## 📊 SİSTEM GEREKSİNİMLERİ

### Minimum:
- **OS:** Windows 10/11
- **RAM:** 4GB
- **Disk:** 10GB boş alan
- **Docker Desktop:** En son sürüm
- **Node.js:** v20.0.0 veya üzeri
- **Yarn:** Kurulu

### Önerilen:
- **RAM:** 8GB veya üzeri
- **Disk:** 20GB boş alan (SSD öneriliir)
- **CPU:** 4 çekirdek

---

## 🚨 ÖNEMLİ NOTLAR

⚠️ **Bu yapılandırma sadece LOCAL DEVELOPMENT içindir!**

**Production için yapman gerekenler:**
1. ✅ Tüm şifreleri değiştir (.env dosyası)
2. ✅ HTTPS/TLS ekle
3. ✅ Firewall kuralları ayarla
4. ✅ Domain name kullan (localhost yerine)
5. ✅ Email servisi yapılandır
6. ✅ Düzenli backup stratejisi oluştur
7. ✅ Log rotation ayarla
8. ✅ Monitoring ekle (Prometheus, Grafana)

---

## 📚 EK KAYNAKLAR

- [Matrix Synapse Docs](https://element-hq.github.io/synapse/latest/)
- [Element Web Docs](https://github.com/element-hq/element-web)
- [Matrix Protocol](https://matrix.org/docs/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

## 🆘 YARDIM

Sorun yaşıyorsan:

1. **Durumu kontrol et:** `.\DURUM.ps1`
2. **Logları kontrol et:** `docker logs matrix-synapse --tail 100`
3. **Container'ları kontrol et:** `docker ps -a`
4. **Port'ları kontrol et:** `netstat -ano | findstr ":8008 :8080"`

---

**Kolay gelsin! 🚀**

Son Güncelleme: 31 Ekim 2025

