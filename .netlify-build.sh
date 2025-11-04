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
yarn install
yarn build

# requirements.txt'i geri getir (cleanup - repo'da kalmalı Railway için)
if [ -f ../requirements.txt.bak ]; then
    mv ../requirements.txt.bak ../requirements.txt
    echo "✅ requirements.txt geri getirildi"
fi

