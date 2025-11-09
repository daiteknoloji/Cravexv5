# ⚠️ DOMAIN UYUMSUZLUĞU SORUNU

## 🔴 SORUN

Kullanıcılar admin panelden oluşturuluyor ama Element Web'de login çalışmıyor!

**Loglar gösteriyor:**
```
Attempted to login as @4u:cravexv5-production.up.railway.app but they do not exist
```

**Sorun:** 
- Admin panel kullanıcıları `@4u:matrix-synapse.up.railway.app` domain'i ile oluşturuyor ✅
- Ama Synapse `@4u:cravexv5-production.up.railway.app` domain'i ile arıyor ❌

---

## 🔍 NEDEN OLUYOR?

Railway'deki Synapse servisi **ESKİ** `homeserver.yaml` dosyasını kullanıyor veya environment variable'ları override ediyor!

**Loglardan görünen:**
```
Server hostname: cravexv5-production.up.railway.app
Public Base URL: https://cravexv5-production.up.railway.app/
```

**Ama `homeserver.yaml` dosyasında:**
```yaml
server_name: "matrix-synapse.up.railway.app"
public_baseurl: "https://matrix-synapse.up.railway.app/"
```

---

## ✅ ÇÖZÜM

### 1. Railway'de Synapse Servisini Kontrol Et

Railway Dashboard → Synapse servisi (`cravexv5`) → **Variables**:

Şu variable'ları kontrol et:
- `SYNAPSE_SERVER_NAME` = `matrix-synapse.up.railway.app` olmalı
- `SYNAPSE_PUBLIC_BASEURL` = `https://matrix-synapse.up.railway.app/` olmalı

**Eğer yoksa veya yanlışsa:**
1. Railway Dashboard → Synapse servisi → **Variables**
2. **"New Variable"** butonuna tıklayın
3. **Name:** `SYNAPSE_SERVER_NAME`
4. **Value:** `matrix-synapse.up.railway.app`
5. **"Add"** butonuna tıklayın
6. Aynı şekilde `SYNAPSE_PUBLIC_BASEURL` = `https://matrix-synapse.up.railway.app/` ekleyin

### 2. Synapse'i Redeploy Et

Railway Dashboard → Synapse servisi → **Deployments** → **Redeploy**

### 3. Veritabanında Kullanıcı Domain'ini Kontrol Et

Railway Dashboard → PostgreSQL → **Query**:

```sql
SELECT 
    name as kullanici_id,
    split_part(name, ':', 2) as domain
FROM users
WHERE name LIKE '%4u%' OR name LIKE '%5u%';
```

**Beklenen:**
- `@4u:matrix-synapse.up.railway.app` ✅
- `@5u:matrix-synapse.up.railway.app` ✅

**Eğer farklı domain görürseniz:**
- Kullanıcılar yanlış domain ile oluşturulmuş
- Admin panel'i redeploy et ve yeniden oluştur

### 4. Element Web Config Kontrol Et

`www/element-web/webapp/config.json` dosyasında:

```json
{
  "default_server_config": {
    "m.homeserver": {
      "base_url": "https://matrix-synapse.up.railway.app",
      "server_name": "matrix-synapse.up.railway.app"
    }
  }
}
```

**Doğru mu kontrol et!**

---

## 🎯 ADIM ADIM ÇÖZÜM

### Adım 1: Railway Variables Kontrolü

1. Railway Dashboard → Synapse servisi (`cravexv5`)
2. **Variables** sekmesine gidin
3. Şu variable'ları kontrol edin:
   - `SYNAPSE_SERVER_NAME` = `matrix-synapse.up.railway.app`
   - `SYNAPSE_PUBLIC_BASEURL` = `https://matrix-synapse.up.railway.app/`

### Adım 2: Eksik Variable'ları Ekleyin

Eğer yoksa:
- `SYNAPSE_SERVER_NAME` = `matrix-synapse.up.railway.app`
- `SYNAPSE_PUBLIC_BASEURL` = `https://matrix-synapse.up.railway.app/`

### Adım 3: Synapse'i Redeploy Et

Railway Dashboard → Synapse servisi → **Deployments** → **Redeploy**

### Adım 4: Veritabanında Kontrol Et

Railway Dashboard → PostgreSQL → **Query**:

```sql
SELECT name FROM users WHERE name LIKE '%4u%' OR name LIKE '%5u%';
```

**Beklenen:** `@4u:matrix-synapse.up.railway.app`

### Adım 5: Test Et

1. Element Web'e gidin: `https://cozy-dragon-54547b.netlify.app/#/login`
2. Username: `4u`
3. Password: (admin panelden oluşturduğunuz şifre)
4. Login deneyin

---

## ⚠️ ÖNEMLİ NOTLAR

### Eğer Kullanıcılar Yanlış Domain ile Oluşturulmuşsa:

**Seçenek 1: Kullanıcıları Sil ve Yeniden Oluştur**
1. Admin Panel'den kullanıcıları silin
2. Synapse'i redeploy edin (doğru domain ile)
3. Yeniden oluşturun

**Seçenek 2: SQL ile Domain'i Değiştir (Riskli!)**
```sql
UPDATE users 
SET name = REPLACE(name, 'cravexv5-production.up.railway.app', 'matrix-synapse.up.railway.app')
WHERE name LIKE '%cravexv5-production.up.railway.app';
```

**⚠️ UYARI:** Bu işlem riskli! Önce backup alın!

---

## 📋 CHECKLIST

- [ ] Railway Dashboard → Synapse → Variables kontrol ettim
- [ ] `SYNAPSE_SERVER_NAME` = `matrix-synapse.up.railway.app` olduğunu doğruladım
- [ ] `SYNAPSE_PUBLIC_BASEURL` = `https://matrix-synapse.up.railway.app/` olduğunu doğruladım
- [ ] Synapse'i redeploy ettim
- [ ] Veritabanında kullanıcı domain'ini kontrol ettim
- [ ] Element Web config doğru mu kontrol ettim
- [ ] Login testi yaptım

---

**SONUÇ:** Railway'deki Synapse servisi eski domain'i kullanıyor. Environment variable'ları ekleyip redeploy etmeniz gerekiyor!


