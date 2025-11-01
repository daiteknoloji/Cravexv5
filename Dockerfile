# Railway için basitleştirilmiş Dockerfile
FROM matrixdotorg/synapse:latest

# Gerekli dizinleri oluştur
RUN mkdir -p /data /config /data/media_store

# Config template kopyala
COPY synapse-config/homeserver.yaml /config/homeserver.yaml.template

# Startup script oluştur
RUN echo '#!/bin/bash\n\
if [ ! -f /data/homeserver.yaml ]; then\n\
  echo "Generating initial config..."\n\
  python -m synapse.app.homeserver \\\n\
    --server-name=${RAILWAY_PUBLIC_DOMAIN:-localhost} \\\n\
    --config-path=/data/homeserver.yaml \\\n\
    --generate-config \\\n\
    --report-stats=no\n\
fi\n\
echo "Starting Synapse..."\n\
exec python -m synapse.app.homeserver -c /data/homeserver.yaml\n\
' > /start.sh && chmod +x /start.sh

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8008/health || exit 1

EXPOSE 8008

# Basit komut formatı
CMD ["/start.sh"]

