#!/bin/bash
# Netlify pre-build script - Python dependencies'i skip et
set -e

# Netlify build command'dan ÖNCE requirements.txt'i kaldır
# Netlify otomatik algılama build command'dan önce çalışıyor
# Bu yüzden build path'inden çıkarmalıyız

# requirements.txt'i geçici olarak kaldır (build path'inden)
if [ -f requirements.txt ]; then
    mv requirements.txt requirements.txt.bak
    echo "✅ requirements.txt geçici olarak kaldırıldı (Netlify Python algılaması için)"
fi

# Element Web build
echo "🚀 Element Web build başlatılıyor..."
cd www/element-web

# Yarn registry hatası için retry logic
echo "📦 Dependencies yükleniyor (retry logic ile)..."
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if yarn install --network-timeout 100000; then
        echo "✅ Dependencies başarıyla yüklendi"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "⚠️ Yarn install başarısız, retry $RETRY_COUNT/$MAX_RETRIES..."
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            sleep 5
        else
            echo "❌ Yarn install $MAX_RETRIES kez denendi, başarısız oldu"
            exit 1
        fi
    fi
done

yarn build

# requirements.txt'i geri getir (cleanup - repo'da kalmalı Railway için)
if [ -f ../requirements.txt.bak ]; then
    mv ../requirements.txt.bak ../requirements.txt
    echo "✅ requirements.txt geri getirildi"
fi

