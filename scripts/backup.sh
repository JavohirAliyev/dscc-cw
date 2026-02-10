#!/bin/bash
# Backup script for Library Management System

set -e

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}"

echo "💾 Starting backup process..."

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup database
echo "📦 Backing up database..."
docker-compose exec -T db pg_dump -U library_user library_db > "${BACKUP_FILE}_database.sql"

# Backup media files
echo "📸 Backing up media files..."
tar -czf "${BACKUP_FILE}_media.tar.gz" media/

# Backup configuration
echo "⚙️  Backing up configuration..."
tar -czf "${BACKUP_FILE}_config.tar.gz" .env docker-compose.yml nginx/

echo "✅ Backup completed successfully!"
echo "📁 Backup files:"
echo "   - ${BACKUP_FILE}_database.sql"
echo "   - ${BACKUP_FILE}_media.tar.gz"
echo "   - ${BACKUP_FILE}_config.tar.gz"

# Clean up old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find $BACKUP_DIR -name "backup_*" -mtime +7 -delete

echo "🎉 Backup process complete!"
