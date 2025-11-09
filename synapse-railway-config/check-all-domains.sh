#!/bin/bash
set -e

echo "🔍 Checking ALL user domains in PostgreSQL database on Railway..."

# Environment variables kontrolü
if [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_PORT" ]; then
    echo "❌ ERROR: PostgreSQL environment variables not fully set!"
    exit 1
fi

# Tüm domain'leri listele (sadece DISTINCT değil, tüm kullanıcıları göster)
echo ""
echo "📊 All domains found in users table:"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as user_count FROM users GROUP BY split_part(name, ':', 2) ORDER BY user_count DESC;"

echo ""
echo "📋 Sample users from each domain:"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT split_part(name, ':', 2) as domain, name as user_id FROM users ORDER BY domain, name LIMIT 20;"

echo ""
echo "✅ Domain check complete!"


