# 🔒 "Pasif Yap" Butonu Açıklaması

## 📋 Ne İşe Yarar?

**"Pasif Yap" butonu** kullanıcıyı geçici olarak devre dışı bırakır. Kullanıcı veritabanında kalır ama pasif duruma geçer.

---

## ⚙️ Nasıl Çalışır?

### Backend İşlemi:
```python
UPDATE users SET deactivated = 1 WHERE name = %s
```

- Kullanıcının `deactivated` flag'i `1` yapılır
- Kullanıcı veritabanında kalır (silinmez)
- Kullanıcı bilgileri korunur

### Frontend İşlemi:
- Pasif kullanıcılar listede **"Pasif"** badge'i ile gösterilir
- Pasif kullanıcılar için **"Aktif Yap"** butonu görünür
- Aktif kullanıcılar için **"Pasif Yap"** butonu görünür

---

## 🔄 Pasif Yap vs Silme Farkı

| Özellik | Pasif Yap | Silme |
|---------|-----------|-------|
| **Veritabanı** | Kullanıcı kalır | Kullanıcı silinir |
| **Geri Alınabilir** | ✅ Evet (Aktif Yap) | ❌ Hayır |
| **Kullanıcı Bilgileri** | Korunur | Silinir |
| **Mesajlar** | Korunur | Korunur (ama kullanıcı yok) |
| **Odalar** | Korunur | Odalardan çıkarılır |

---

## ✅ GÜNCEL DURUM

**Pasif yap butonu artık Matrix Synapse Admin API kullanıyor!**

**Özellikler:**
- ✅ Matrix Admin API ile deactivate ediliyor
- ✅ Kullanıcı logout edilir
- ✅ Tüm oturumlar kapatılır (access tokens silinir)
- ✅ Tüm cihazlar kaldırılır (devices silinir)
- ✅ Tekrar login olamaz
- ✅ Veritabanı da güncellenir (`deactivated = 1`)

**Fallback:** Eğer Matrix API kullanılamazsa, veritabanı yöntemi kullanılır (access tokens ve devices yine de silinir).

---

## 🎯 Kullanım Senaryoları

### Pasif Yap Ne Zaman Kullanılır?
- ✅ Geçici olarak kullanıcıyı devre dışı bırakmak
- ✅ Kullanıcıyı silmeden erişimini engellemek
- ✅ Daha sonra tekrar aktif yapabilmek
- ✅ Kullanıcı bilgilerini korumak

### Silme Ne Zaman Kullanılır?
- ✅ Kullanıcıyı kalıcı olarak kaldırmak
- ✅ Veritabanından tamamen silmek
- ✅ Geri alınamaz işlem

---

## 🔧 Teknik Detaylar

### Backend Endpoint:
```
PUT /api/users/<user_id>/deactivate
Body: { "deactivated": true/false }
```

### Frontend Fonksiyon:
```javascript
toggleUserDeactivate(userId, deactivate)
```

### Veritabanı Değişikliği:
```sql
UPDATE users SET deactivated = 1 WHERE name = 'user_id'
```

---

## 📊 Pasif Kullanıcı Göstergeleri

- **Listede:** Kırmızı "Pasif" badge'i görünür
- **Buton:** "Aktif Yap" butonu görünür
- **Filtreleme:** "Pasif" filtresi ile gösterilebilir

---

## ✅ Özet

**"Pasif Yap" butonu:**
- Kullanıcıyı geçici olarak devre dışı bırakır
- Veritabanında kalır (silinmez)
- Geri alınabilir (Aktif Yap ile)
- Kullanıcı bilgileri korunur

**"Sil" butonu:**
- Kullanıcıyı kalıcı olarak siler
- Veritabanından tamamen kaldırılır
- Geri alınamaz
- Tüm ilişkili veriler silinir

---

**Hazırlayan:** AI Assistant  
**Tarih:** 2025

