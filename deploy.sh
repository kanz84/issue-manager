#!/bin/sh

current_time=$(date "+%Y%m%d_%H%M%S")
backup_dir=$HOME/backups/issue-manager/backup_$current_time/

mkdir -p "$HOME/artifacts/issue-manager/postgres/pgdata"
mkdir -p "$HOME/artifacts/issue-manager/app_files"
mkdir -p "$HOME/artifacts/issue-manager/app_files/static"
mkdir -p "$HOME/artifacts/issue-manager/app_files/media"
mkdir -p "$backup_dir"

docker-compose down && docker system prune -f && docker network prune -f
echo "Old docker containers removed"

tar -pczf "$backup_dir/project.tar.gz" --exclude .git .
echo "Project backed up to $backup_dir"

local_settings="local_settings.py"
if [ ! -f $local_settings ]; then
    echo "env=\"PRO\"" > $local_settings
    echo "local_settings.py created in project dir"
fi

docker-compose up -d --build --suppress-orphan-warning
echo "Docker image built"


#if [ $? -ne 0 ]; then
#    <ran if unsuccessful> for example exit;
#fi