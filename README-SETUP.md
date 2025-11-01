# 🚀 Matrix Synapse Full Stack Setup

Bu proje **Matrix Synapse** sunucusu, **PostgreSQL** veritabanı ve **Element Web** + **Synapse Admin** arayüzlerini içeren tam bir Matrix platform kurulumudur.

---

## 📦 İçerik

- **Matrix Synapse Server** - Matrix protokolü sunucusu
- **PostgreSQL** - Ana veritabanı
- **Redis** - Cache ve worker desteği
- **Element Web** - Matrix web client (mesajlaşma arayüzü)
- **Synapse Admin** - Yönetim paneli

---

## 🔧 Gereksinimler

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows için)
- [Node.js](https://nodejs.org/) >= 20.0.0
- [Yarn](https://yarnpkg.com/) paket yöneticisi
- En az 4GB RAM
- En az 10GB disk alanı

---

## 🚀 Kurulum Adımları

### 1. Environment Dosyasını Hazırla

```powershell
# .env.example dosyasını .env olarak kopyala (Windows PowerShell)
Copy-Item .env.example .env

# Gerekirse .env içindeki şifreleri güncelle
notepad .env
```

### 2. Docker Container'ları Başlat

```powershell
# Tüm servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f synapse
```

**İlk başlatma 2-3 dakika sürebilir!** Veritabanı oluşturulup Synapse başlatılıyor.

### 3. Synapse'in Başlamasını Bekle

```powershell
# Synapse health check
curl http://localhost:8008/health

# Başarılı yanıt: "OK"
```

### 4. Admin Kullanıcı Oluştur

```powershell
# Docker container içinde admin kullanıcı oluştur
docker exec -it matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -a

# Kullanıcı adı: admin
# Şifre: (güçlü bir şifre gir)
# Admin olsun mu? yes
```

### 5. Frontend'leri Başlat

#### Element Web (Mesajlaşma)
```powershell
cd www\element-web
yarn install
yarn start
```
🌐 **Adres:** http://localhost:8080

#### Synapse Admin (Yönetim Paneli)
```powershell
# Yeni terminal aç
cd www\admin
yarn install
yarn start
```
🌐 **Adres:** http://localhost:5173

---

## 🌐 Erişim Bilgileri

| Servis | URL | Port |
|--------|-----|------|
| **Matrix Synapse API** | http://localhost:8008 | 8008 |
| **Element Web** | http://localhost:8080 | 8080 |
| **Synapse Admin** | http://localhost:5173 | 5173 |
| **PostgreSQL** | localhost | 5432 |
| **Redis** | localhost | 6379 |

---

## 📝 İlk Giriş

### Element Web'e Giriş
1. http://localhost:8080 aç
2. "Sign In" tıkla
3. **Homeserver:** `http://localhost:8008` gir
4. **Username:** `admin`
5. **Password:** (oluşturduğun şifre)

### Synapse Admin'e Giriş
1. http://localhost:5173 aç
2. **Homeserver URL:** `http://localhost:8008` gir
3. **Username:** `@admin:localhost`
4. **Password:** (oluşturduğun şifre)

---

## 🛠️ Yönetim Komutları

### Docker Servisleri

```powershell
# Servisleri başlat
docker-compose up -d

# Servisleri durdur
docker-compose down

# Logları görüntüle
docker-compose logs -f

# Sadece Synapse'i yeniden başlat
docker-compose restart synapse

# Tüm servislerin durumunu kontrol et
docker-compose ps
```

### Yeni Kullanıcı Oluşturma

```powershell
# Normal kullanıcı
docker exec -it matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml

# Admin kullanıcı
docker exec -it matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -a
```

### Veritabanı Backup

```powershell
# PostgreSQL backup
docker exec matrix-postgres pg_dump -U synapse_user synapse > backup.sql

# Restore
docker exec -i matrix-postgres psql -U synapse_user synapse < backup.sql
```

---

## 🐛 Sorun Giderme

### Synapse başlamıyor
```powershell
# Logları kontrol et
docker-compose logs synapse

# Container'ı yeniden başlat
docker-compose restart synapse
```

### PostgreSQL bağlantı hatası
```powershell
# PostgreSQL sağlık kontrolü
docker exec matrix-postgres pg_isready -U synapse_user

# Veritabanına bağlan ve kontrol et
docker exec -it matrix-postgres psql -U synapse_user -d synapse
```

### Port zaten kullanımda
```powershell
# Port 8008 kullanımda mı kontrol et
netstat -ano | findstr :8008

# Process'i sonlandır (PID numarasını değiştir)
taskkill /PID <PID_NUMARASI> /F
```

### Element Web bağlanamıyor
1. http://localhost:8008/health adresini kontrol et
2. Homeserver URL'sini `http://localhost:8008` olarak gir (https değil!)
3. Tarayıcı console'unda CORS hatası varsa, synapse config'i kontrol et

---

## 📊 Veritabanı Bilgileri

```yaml
Host: localhost (veya postgres container içinden)
Port: 5432
Database: synapse
User: synapse_user
Password: .env dosyasında tanımlı
```

---

## 🔐 Güvenlik Notları

⚠️ **Bu yapılandırma sadece LOCAL DEVELOPMENT içindir!**

Production için:
- Tüm şifreleri değiştir
- HTTPS/TLS ekle
- Firewall kuralları ayarla
- CORS politikalarını güncelle
- Email servisi yapılandır
- Backup stratejisi oluştur

---

## 📚 Daha Fazla Bilgi

- [Synapse Documentation](https://element-hq.github.io/synapse/latest/)
- [Element Web Docs](https://github.com/element-hq/element-web)
- [Matrix Protocol](https://matrix.org/docs/)
- [Synapse Admin Guide](https://element-hq.github.io/synapse/latest/admin_api/)

---

## 🆘 Destek

Sorun yaşarsan:
1. `docker-compose logs -f` ile logları kontrol et
2. `docker-compose ps` ile servislerin durumunu kontrol et
3. README dosyasındaki troubleshooting bölümünü oku

---

**Kolay gelsin! 🚀**


