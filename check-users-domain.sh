#!/bin/bash
# Veritabanındaki kullanıcıların domain'lerini kontrol et

echo "🔍 Veritabanındaki kullanıcı domain'lerini kontrol ediyoruz..."
echo ""

# Railway CLI ile PostgreSQL'e bağlan ve domain'leri listele
railway run --service postgres psql -c "
SELECT 
    split_part(name, ':', 2) as domain,
    COUNT(*) as kullanici_sayisi
FROM users 
GROUP BY split_part(name, ':', 2)
ORDER BY kullanici_sayisi DESC;
"

echo ""
echo "📊 Son 10 kullanıcı:"
railway run --service postgres psql -c "
SELECT name, creation_ts 
FROM users 
ORDER BY creation_ts DESC 
LIMIT 10;
"

echo ""
echo "✅ Hangi domain'de kullanıcılar var görüldü!"
echo "💡 Synapse'i EN ÇOK KULLANICININ OLDUĞU domain ile başlat!"


