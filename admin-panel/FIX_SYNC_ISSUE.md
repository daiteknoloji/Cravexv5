# Synapse Sync 404 Hatası Düzeltme Kılavuzu

## Sorun
Element Web'de yeni oda/chat oluşturulduğunda görünmüyor. Console'da `404: No row found` hatası alınıyor.

## Neden
Büyük veri silme işlemlerinden sonra Synapse'in internal state'i bozulmuş. `event_push_actions` tablosunda beklenen rotation tracking row'u eksik.

## Çözüm Adımları

### 1. Synapse Servisini Yeniden Başlatın (ÖNERİLEN)

Railway'de Synapse servisini restart edin:
- Railway Dashboard → Synapse servisi → Settings → Restart

Bu, Synapse'in internal state'ini otomatik olarak reinitialize edecektir.

### 2. Eğer Restart İşe Yaramazsa: SQL Script Çalıştırın

`fix_synapse_sync_state.sql` dosyasını çalıştırın. Bu script:
- Mevcut durumu kontrol eder
- Gerekirse stream_ordering sequence'larını resetler

### 3. Element Web Cache'ini Temizleyin

1. Browser Developer Tools'u açın (F12)
2. Application/Storage sekmesine gidin
3. IndexedDB → Element Web veritabanını silin
4. Local Storage → Element Web verilerini temizleyin
5. Browser'ı kapatıp yeniden açın
6. Element Web'e yeniden login olun

### 4. Kontrol

- Yeni bir oda oluşturun
- Admin panel'de görünüyor mu kontrol edin
- Element Web'de görünüyor mu kontrol edin

## Alternatif: Stream Ordering Sequence Reset

Eğer yukarıdaki adımlar işe yaramazsa, stream_ordering sequence'ını resetleyin:

```sql
-- DİKKAT: Bu sadece TÜM events silindiyse yapılmalı!
ALTER SEQUENCE event_stream_ordering RESTART WITH 1;
```

Sonra Synapse'i yeniden başlatın.

## Notlar

- Bu sorun genellikle büyük veri silme işlemlerinden sonra oluşur
- Synapse restart genellikle sorunu çözer
- Eğer sorun devam ederse, Railway logs'ları kontrol edin

