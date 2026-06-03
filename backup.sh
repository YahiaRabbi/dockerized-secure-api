#!/bin/bash
# Automated Backup Script for Noorzaah Database
echo "Starting PostgreSQL database backup..."
docker exec dockersql-postgres_db-1 pg_dump -U admin noorzaah_db > db_backup.sql
echo "Backup completed successfully! Saved as db_backup.sql"