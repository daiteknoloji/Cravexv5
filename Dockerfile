# Railway için basitleştirilmiş Dockerfile
FROM matrixdotorg/synapse:latest

# Config dosyalarını kopyala
COPY synapse-config/homeserver.yaml /config/homeserver.yaml
COPY synapse-config/*.signing.key* /data/ 2>/dev/null || :
COPY synapse-config/*.log.config /data/ 2>/dev/null || :

# Data dizinini oluştur
RUN mkdir -p /data/media_store

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8008/health || exit 1

EXPOSE 8008

CMD ["python", "-m", "synapse.app.homeserver", "-c", "/data/homeserver.yaml"]

