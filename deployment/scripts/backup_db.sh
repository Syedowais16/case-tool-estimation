#!/bin/bash
# Backup script for CASE Tool database

BACKUP_DIR="./backups"
DB_USER="${DB_USER:-casetool}"
DB_HOST="${DB_HOST:-localhost}"
DB_NAME="${DB_NAME:-casetool_db}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/casetool_backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

echo "Starting database backup..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_FILE

echo "Backup completed: $BACKUP_FILE"

# Keep only last 7 backups
echo "Cleaning old backups..."
ls -t $BACKUP_DIR/casetool_backup_*.sql | tail -n +8 | xargs rm -f

echo "Backup process finished!"
