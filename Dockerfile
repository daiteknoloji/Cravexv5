# Multi-stage Dockerfile for Synapse Admin
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY www/admin/package*.json ./
RUN npm ci

# Copy source
COPY www/admin ./

# Build
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Copy built files
COPY --from=build /app/dist ./dist

# Expose port
EXPOSE 3000

# Start with vite preview
CMD ["sh", "-c", "npx vite preview --host 0.0.0.0 --port ${PORT:-3000}"]
