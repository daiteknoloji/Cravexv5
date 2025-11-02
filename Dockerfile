# Railway Dockerfile for Matrix Synapse
FROM matrixdotorg/synapse:latest

# Copy config template
COPY synapse-config/homeserver.yaml /data/homeserver.yaml

# Ensure data directory
RUN mkdir -p /data/media_store

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8008/health || exit 1

EXPOSE 8008

# Use Synapse's default entrypoint with direct command
CMD ["run"]

