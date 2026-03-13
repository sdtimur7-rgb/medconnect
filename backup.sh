#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
BACKUP_FILE="${BACKUP_DIR}/medconnect_${DATE}.sql"

mkdir -p ${BACKUP_DIR}

echo "🗄️  Creating database backup..."

docker-compose exec -T postgres pg_dump -U medconnect medconnect > ${BACKUP_FILE}

if [ $? -eq 0 ]; then
    gzip ${BACKUP_FILE}
    echo "✅ Backup created: ${BACKUP_FILE}.gz"
    
    echo "🧹 Removing backups older than 30 days..."
    find ${BACKUP_DIR} -name "*.sql.gz" -mtime +30 -delete
    
    echo "📦 Total backups:"
    ls -lh ${BACKUP_DIR}/*.sql.gz 2>/dev/null | wc -l
else
    echo "❌ Backup failed!"
    exit 1
fi
