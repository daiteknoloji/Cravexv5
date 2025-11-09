# 💾 RAILWAY SETTINGS BACKUP REHBER v2

## 🎯 AMAÇ

Railway servislerinin tüm ayarlarını (config, variables, networking) export edip local'de backup almak.

---

## 🚀 HIZLI KULLANIM

### PowerShell Script ile:

```powershell
.\railway-export-settings-v2.ps1
```

**Ne yapar?**
- ✅ Railway CLI kontrol eder
- ✅ Railway'a login kontrol eder
- ✅ Tüm servisleri export eder
- ✅ Variables'ları export eder
- ✅ Config dosyalarını kopyalar
- ✅ JSON formatında tam backup oluşturur
- ✅ Local klasöre kaydeder

---

## 📋 MANUEL BACKUP ADIMLARI

### 1. Railway CLI Kurulumu

```powershell
npm install -g @railway/cli
```

### 2. Railway'a Login

```powershell
railway login
```

### 3. Projeyi Seç

```powershell
railway link
```

### 4. Servisleri Export Et

#### Synapse Servisi (cravexv5):

```powershell
# Service info
railway service --service cravexv5 > synapse-service-info.txt

# Variables (JSON)
railway variables --service cravexv5 --json > synapse-variables.json

# Variables (Human-readable)
railway variables --service cravexv5 > synapse-variables.txt
```

#### Admin Panel Servisi (considerate-adaptation):

```powershell
# Service info
railway service --service considerate-adaptation > admin-panel-service-info.txt

# Variables (JSON)
railway variables --service considerate-adaptation --json > admin-panel-variables.json

# Variables (Human-readable)
railway variables --service considerate-adaptation > admin-panel-variables.txt
```

#### Element Web Servisi (surprising-emotion):

```powershell
# Service info
railway service --service surprising-emotion > element-web-service-info.txt

# Variables (JSON)
railway variables --service surprising-emotion --json > element-web-variables.json

# Variables (Human-readable)
railway variables --service surprising-emotion > element-web-variables.txt
```

---

## 📁 BACKUP KLASÖR YAPISI

```
railway-backups/
└── railway-settings-2025-11-08_23-45-00/
    ├── README.md                          # Özet bilgiler
    ├── railway-backup-full.json          # Tüm backup (JSON)
    ├── railway-env-template.txt          # Environment variables template
    ├── railway-synapse.json              # Synapse config
    ├── railway-admin-panel.json          # Admin Panel config
    ├── railway-turnserver.json           # TURN Server config
    ├── cravexv5/                         # Synapse servis backup
    │   ├── service-info.txt
    │   ├── variables.json
    │   ├── variables.txt
    │   └── networking.txt
    ├── considerate-adaptation/            # Admin Panel servis backup
    │   ├── service-info.txt
    │   ├── variables.json
    │   ├── variables.txt
    │   └── networking.txt
    └── surprising-emotion/                # Element Web servis backup
        ├── service-info.txt
        ├── variables.json
        ├── variables.txt
        └── networking.txt
```

---

## 🔄 RESTORE (GERİ YÜKLEME)

### Railway Dashboard'dan Manuel Restore:

1. **Railway Dashboard → Service → Variables**
2. **Variables'ları tek tek ekleyin:**
   - Backup klasöründeki `variables.txt` dosyasından kopyalayın
   - Railway Dashboard → Variables → "New Variable"
   - Name ve Value'yu yapıştırın

3. **Config dosyalarını restore edin:**
   - Backup klasöründeki `railway-*.json` dosyalarını kullanın
   - Railway Dashboard → Service → Settings → Config File

---

## 📋 EXPORT EDİLEN BİLGİLER

### Her Servis İçin:

1. ✅ **Service Info:**
   - Service name
   - Service ID
   - Build settings
   - Deploy settings

2. ✅ **Variables:**
   - Tüm environment variables
   - JSON formatında
   - Human-readable formatında

3. ✅ **Networking:**
   - Public domain
   - Port mappings
   - Networking settings

4. ✅ **Config Files:**
   - `railway-*.json` dosyaları
   - Dockerfile paths
   - Build commands

---

## 🎯 ÖNEMLİ VARIABLES

### Synapse (cravexv5):

```
SYNAPSE_SERVER_NAME="matrix-synapse.up.railway.app"
SYNAPSE_PUBLIC_BASEURL="https://matrix-synapse.up.railway.app/"
WEB_CLIENT_LOCATION="https://surprising-emotion-production.up.railway.app"
POSTGRES_HOST=${{Postgres.PGHOST}}
POSTGRES_PORT=${{Postgres.PGPORT}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
POSTGRES_DB=${{Postgres.PGDATABASE}}
```

### Admin Panel (considerate-adaptation):

```
HOMESERVER_DOMAIN="matrix-synapse.up.railway.app"
SYNAPSE_URL="https://matrix-synapse.up.railway.app"
ADMIN_PASSWORD="GüçlüBirŞifre123!"
PGDATABASE=${{Postgres.PGDATABASE}}
PGHOST=${{Postgres.PGHOST}}
PGPASSWORD=${{Postgres.PGPASSWORD}}
PGPORT=${{Postgres.PGPORT}}
PGUSER=${{Postgres.PGUSER}}
RAILWAY_DOCKERFILE_PATH="admin-panel.Dockerfile"
```

---

## ✅ BACKUP DOĞRULAMA

Backup sonrası kontrol edin:

1. ✅ Backup klasörü oluşturuldu mu?
2. ✅ Tüm servisler export edildi mi?
3. ✅ Variables dosyaları var mı?
4. ✅ Config dosyaları kopyalandı mı?
5. ✅ JSON backup oluşturuldu mu?

---

## 🔄 OTOMATIK BACKUP

### Scheduled Backup (Opsiyonel):

Windows Task Scheduler ile otomatik backup:

```powershell
# Task oluştur
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\path\to\railway-export-settings-v2.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "RailwayBackup" -Action $action -Trigger $trigger
```

---

## 📋 CHECKLIST

- [ ] Railway CLI kurulu mu?
- [ ] Railway'a login yapıldı mı?
- [ ] Proje seçildi mi?
- [ ] Backup script çalıştırıldı mı?
- [ ] Backup klasörü kontrol edildi mi?
- [ ] Tüm servisler export edildi mi?
- [ ] Variables dosyaları var mı?
- [ ] Config dosyaları kopyalandı mı?

---

**SONUÇ:** Railway settings'lerinizi v2 formatında export edip local backup alabilirsiniz! 💾


