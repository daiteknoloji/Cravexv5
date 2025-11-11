# Admin Kullanıcısı Şifre Reset

## Sorun
SQL ile oluşturulan admin kullanıcısı ile login olunamıyor. Matrix Synapse password hash formatı farklı olabilir.

## Çözüm: Matrix Synapse Admin API Kullanarak Şifre Reset

### Yöntem 1: Python Script ile (Önerilen)

```bash
# Railway'de Admin Panel servisinde çalıştırın
cd admin-panel
python reset_admin_password_via_api.py "GizliKayitAnahtari123456789" "GucluBirSifre123!"
```

### Yöntem 2: Railway'de Environment Variable ile

1. Railway Dashboard → Admin Panel servisi → Settings → Variables
2. `REGISTRATION_SHARED_SECRET` variable'ını ekleyin: `GizliKayitAnahtari123456789`
3. Railway'de Admin Panel servisinde terminal açın
4. Şu komutu çalıştırın:

```bash
python reset_admin_password_via_api.py
```

### Yöntem 3: Manuel API Call (curl)

```bash
# 1. Nonce al
NONCE=$(curl -s https://matrix-synapse.up.railway.app/_synapse/admin/v1/register | jq -r '.nonce')

# 2. HMAC hesapla (Python ile)
python -c "
import hmac
import hashlib
nonce = '$NONCE'
username = 'admin'
password = 'GucluBirSifre123!'
secret = 'GizliKayitAnahtari123456789'
message = f'{nonce}\x00{username}\x00{password}\x00admin'
mac = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()
print(mac)
"

# 3. Admin kullanıcısı oluştur/reset et
curl -X POST https://matrix-synapse.up.railway.app/_synapse/admin/v1/register \
  -H "Content-Type: application/json" \
  -d "{
    \"nonce\": \"$NONCE\",
    \"username\": \"admin\",
    \"password\": \"GucluBirSifre123!\",
    \"admin\": true,
    \"mac\": \"CALCULATED_MAC_HERE\"
  }"
```

## Login Bilgileri

- **Kullanıcı adı:** `admin`
- **Şifre:** `GucluBirSifre123!`

## Not

Bu yöntem Matrix Synapse'in kendi API'sini kullandığı için password hash formatı sorunu olmaz. Matrix Synapse şifreyi doğru formatta hash'ler ve veritabanına kaydeder.

