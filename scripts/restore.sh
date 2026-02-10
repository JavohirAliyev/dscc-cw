#!/bin/bash
# Restore script for Library Management System

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh TIMESTAMP"
    echo "Example: ./restore.sh 20260210_153000"
    echo ""
    echo "Available backups:"
    ls -1 backups/ | grep "backup_" | cut -d'_' -f2,3 | cut -d'_' -f1,2 | sort -u
    exit 1
fi

TIMESTAMP=$1
BACKUP_DIR="backups"
BACKUP_PREFIX="${BACKUP_DIR}/backup_${TIMESTAMP}"

echo "🔄 Starting restore process for backup: $TIMESTAMP"

# Check if backup files exist
if [ ! -f "${BACKUP_PREFIX}_database.sql" ]; then
    echo "❌ Database backup file not found!"
    exit 1
fi

# Restore database
echo "📦 Restoring database..."
docker-compose exec -T db psql -U library_user library_db < "${BACKUP_PREFIX}_database.sql"

# Restore media files
if [ -f "${BACKUP_PREFIX}_media.tar.gz" ]; then
    echo "📸 Restoring media files..."
    tar -xzf "${BACKUP_PREFIX}_media.tar.gz"
fi

# Restore configuration
if [ -f "${BACKUP_PREFIX}_config.tar.gz" ]; then
    echo "⚙️  Restoring configuration..."
    read -p "This will overwrite current configuration. Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        tar -xzf "${BACKUP_PREFIX}_config.tar.gz"
    fi
fi

echo "✅ Restore completed successfully!"
echo "🔄 Restarting services..."
docker-compose restart

echo "🎉 Restore process complete!"
