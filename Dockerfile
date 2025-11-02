# Railway Dockerfile for Matrix Synapse
FROM matrixdotorg/synapse:latest

# Set working directory
WORKDIR /data

# Copy config template
COPY synapse-config/homeserver.yaml /data/homeserver.yaml

# Create startup script
RUN printf '#!/bin/bash\n\
set -e\n\
echo "Starting Matrix Synapse..."\n\
exec python -m synapse.app.homeserver -c /data/homeserver.yaml\n' > /start.sh \
    && chmod +x /start.sh

# Healthcheck disabled - server takes time for DB migrations
# Railway will use port 8008 availability instead

EXPOSE 8008

# Use bash directly
ENTRYPOINT ["/bin/bash"]
CMD ["/start.sh"]

