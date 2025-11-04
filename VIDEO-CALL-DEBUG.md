# Video Call Debugging Guide

## Sorun Analizi

Console loglarına göre iki ana sorun var:

1. **JavaScript Initialization Error**: `ReferenceError: can't access lexical declaration 'B' before initialization`
   - Widget store'ların başlatılmasında sorun
   - Bu, video call'ları engelleyebilir

2. **TURN Server Connectivity**: 
   - Endpoint 200 dönüyor ama ICE candidates oluşmuyor
   - Railway TURN server çalışmıyor olabilir

## Debug Adımları

### 1. TURN Server Response Kontrolü

Browser console'da şunu çalıştır:

```javascript
// TURN server bilgilerini kontrol et
const client = window.mxMatrixClient;
if (client) {
    console.log("TURN Servers:", client.getTurnServers());
    console.log("TURN Servers Expiry:", new Date(client.getTurnServersExpiry()));
    
    // TURN server endpoint'ini manuel test et
    fetch('https://cravex1-production.up.railway.app/_matrix/client/v3/voip/turnServer', {
        headers: {
            'Authorization': 'Bearer ' + client.getAccessToken()
        }
    })
    .then(r => r.json())
    .then(data => {
        console.log("TURN Server Response:", JSON.stringify(data, null, 2));
    })
    .catch(err => console.error("TURN Server Error:", err));
}
```

### 2. Railway TURN Server Logs Kontrol

1. Railway Dashboard > TURN-SERVER service > Logs
2. Coturn başladı mı kontrol et
3. Connection attempts var mı bak

### 3. ICE Candidates Kontrolü

Video call başlatırken console'da şunu ara:
- `ICE candidate` mesajları
- `relay` type candidates var mı?
- `host` candidates var mı?

### 4. WebRTC Peer Connection Debug

```javascript
// Peer connection'i kontrol et
const call = window.mxCallHandler?.getCallForRoom('!ROOM_ID');
if (call) {
    const pc = call.peerConn;
    if (pc) {
        console.log("ICE Connection State:", pc.iceConnectionState);
        console.log("ICE Gathering State:", pc.iceGatheringState);
        console.log("Signaling State:", pc.signalingState);
        
        // ICE candidates'i dinle
        pc.addEventListener('icecandidate', (event) => {
            if (event.candidate) {
                console.log("ICE Candidate:", event.candidate.candidate);
                console.log("Type:", event.candidate.type);
                console.log("Protocol:", event.candidate.protocol);
            }
        });
    }
}
```

## Olası Çözümler

### Çözüm 1: Railway TURN Server Restart

Eğer Railway TURN server çalışmıyorsa:
1. Railway Dashboard > TURN-SERVER service
2. Settings > Restart

### Çözüm 2: TURN Server Config Düzelt

Eğer TURN server çalışıyor ama bağlanamıyorsa:
- `turnserver.conf` dosyasını kontrol et
- Railway'in UDP desteği sınırlı olabilir
- TCP-only çalışmayı deneyin

### Çözüm 3: Fallback TURN Servers

Metered.ca TURN servers zaten config'de var, ama Railway TURN server öncelikli. Eğer Railway TURN server çalışmıyorsa, Metered.ca kullanılmalı.

### Çözüm 4: JavaScript Error Fix

`ReferenceError: can't access lexical declaration 'B' before initialization` hatası için:
- Browser cache'i temizle
- Hard refresh (Ctrl+Shift+R)
- Incognito mode'da test et

## Test Senaryosu

1. İki farklı browser'da aç (veya incognito + normal)
2. İki farklı kullanıcı ile login ol
3. Video call başlat
4. Console logları kontrol et:
   - TURN server response
   - ICE candidates
   - WebRTC connection state

## Beklenen Sonuç

Başarılı bir video call için:
- ✅ TURN server response'da `uris` array'i olmalı
- ✅ ICE candidates'de `relay` type olmalı
- ✅ `iceConnectionState` `connected` olmalı
- ✅ Audio/video stream'ler aktive olmalı

