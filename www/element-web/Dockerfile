# Multi-stage build for Element-web
FROM node:22-alpine AS builder

# Set working directory
WORKDIR /app

# Increase Node.js memory limit for build (Railway build optimization)
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV YARN_NETWORK_TIMEOUT=300000

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies with increased timeout
RUN yarn config set network-timeout 300000 && \
    yarn install --frozen-lockfile --network-timeout 300000

# Copy source code
COPY . .

# Build Element-web with increased memory
RUN yarn build

# Production stage - serve with nginx
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/webapp /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
