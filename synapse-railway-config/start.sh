#!/bin/bash
set -e

echo "🚀 Starting Matrix Synapse on Railway..."

# Environment variables kontrolü
if [ -z "$POSTGRES_HOST" ]; then
    echo "❌ ERROR: POSTGRES_HOST not set!"
    exit 1
fi

# Synapse data dizini - Railway'de /tmp dizini yazılabilir
DATA_DIR="/tmp"
mkdir -p $DATA_DIR

# homeserver.yaml'ı kopyala ve environment variables ile güncelle
# Önce /data dizininden kontrol et (Dockerfile'dan kopyalanmış olabilir)
if [ -f /data/homeserver.yaml ]; then
    cp /data/homeserver.yaml $DATA_DIR/homeserver.yaml
elif [ -f /config/homeserver.yaml ]; then
    cp /config/homeserver.yaml $DATA_DIR/homeserver.yaml
else
    echo "❌ ERROR: homeserver.yaml not found!"
    exit 1
fi

# Server name güncelle
if [ ! -z "$SYNAPSE_SERVER_NAME" ]; then
    # Herhangi bir server_name değerini replace et
    sed -i "s|server_name: \".*\"|server_name: \"$SYNAPSE_SERVER_NAME\"|g" $DATA_DIR/homeserver.yaml
    # Herhangi bir public_baseurl değerini replace et
    sed -i "s|public_baseurl: \"https://.*/\"|public_baseurl: \"https://$SYNAPSE_SERVER_NAME/\"|g" $DATA_DIR/homeserver.yaml
fi

# Web client location güncelle
if [ ! -z "$WEB_CLIENT_LOCATION" ]; then
    sed -i "s|https://synapse-admin-ui-production.up.railway.app|$WEB_CLIENT_LOCATION|g" $DATA_DIR/homeserver.yaml
fi

# PostgreSQL ayarlarını güncelle
sed -i "s|user: postgres|user: $POSTGRES_USER|g" $DATA_DIR/homeserver.yaml
sed -i "s|password: changeme|password: $POSTGRES_PASSWORD|g" $DATA_DIR/homeserver.yaml
sed -i "s|database: railway|database: $POSTGRES_DB|g" $DATA_DIR/homeserver.yaml
sed -i "s|host: localhost|host: $POSTGRES_HOST|g" $DATA_DIR/homeserver.yaml
sed -i "s|port: 5432|port: $POSTGRES_PORT|g" $DATA_DIR/homeserver.yaml

# SMTP email password güncelle (eğer environment variable varsa)
if [ ! -z "$SYNAPSE_EMAIL_SMTP_PASS" ]; then
    echo "📧 Updating SMTP password from environment variable..."
    # ${SYNAPSE_EMAIL_SMTP_PASS} formatını replace et
    sed -i "s|\${SYNAPSE_EMAIL_SMTP_PASS}|$SYNAPSE_EMAIL_SMTP_PASS|g" $DATA_DIR/homeserver.yaml
    # Veya direkt smtp_pass satırını replace et
    sed -i "s|smtp_pass: \".*\"|smtp_pass: \"$SYNAPSE_EMAIL_SMTP_PASS\"|g" $DATA_DIR/homeserver.yaml
else
    echo "⚠️  WARNING: SYNAPSE_EMAIL_SMTP_PASS not set - email functionality may not work!"
fi

# Signing key oluştur (yoksa) - /tmp dizininde
if [ ! -f "$DATA_DIR/signing.key" ]; then
    echo "🔑 Generating signing key..."
    python3 -m synapse.app.homeserver \
        --config-path=$DATA_DIR/homeserver.yaml \
        --generate-keys
fi

# Log config oluşturma - Railway'de log_config disabled, bu yüzden skip ediyoruz
# Railway varsayılan console logging kullanacak
echo "📝 Using default console logging (log_config disabled for Railway)"

echo "✅ Configuration complete!"
echo "📍 Server: $SYNAPSE_SERVER_NAME"
echo "🗄️  Database: $POSTGRES_HOST:$POSTGRES_PORT"
echo ""
echo "🚀 Starting Synapse..."

# Synapse başlat
exec python3 -m synapse.app.homeserver -c $DATA_DIR/homeserver.yaml

