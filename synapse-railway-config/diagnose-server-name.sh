#!/bin/bash
set -e

echo "🔍 Diagnosing Synapse server_name issue..."

# Environment variables kontrolü
if [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_PORT" ]; then
    echo "❌ ERROR: PostgreSQL environment variables not fully set!"
    exit 1
fi

echo ""
echo "1️⃣ Checking ALL domains in users table:"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT DISTINCT split_part(name, ':', 2) as domain, COUNT(*) as user_count FROM users GROUP BY split_part(name, ':', 2) ORDER BY user_count DESC;"

echo ""
echo "2️⃣ Checking if server_name is stored in database (schema_version table):"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT * FROM schema_version LIMIT 5;" 2>/dev/null || echo "⚠️ schema_version table not found or empty"

echo ""
echo "3️⃣ Checking for any config tables:"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\dt" | grep -i config || echo "⚠️ No config tables found"

echo ""
echo "4️⃣ Sample users (first 10):"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT name FROM users LIMIT 10;"

echo ""
echo "✅ Diagnosis complete!"
echo ""
echo "💡 If you see multiple domains above, you need to delete users from the domain(s) that don't match cravex1-production.up.railway.app"


