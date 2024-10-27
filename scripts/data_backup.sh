#!/bin/bash

# Script: scripts/data_backup.sh
# Purpose: This script automates the backup of simulation results and datasets to ensure data preservation.

# Configuration
BACKUP_SRC="./data/"  # Source directory for data backup
BACKUP_DEST="./backups/"  # Backup destination directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DEST}backup_${TIMESTAMP}.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DEST"

# Create a compressed backup
echo "Starting backup of $BACKUP_SRC..."
tar -czvf "$BACKUP_FILE" "$BACKUP_SRC"
echo "Backup completed: $BACKUP_FILE"

# Verify backup
if [[ -f "$BACKUP_FILE" ]]; then
    echo "Backup verification: SUCCESS"
else
    echo "Backup verification: FAILED"
    exit 1
fi

# Optional: Remove old backups to save space (e.g., older than 7 days)
find "$BACKUP_DEST" -type f -name "*.tar.gz" -mtime +7 -exec rm {} \;
echo "Old backups cleaned up."

echo "Backup process completed successfully."
