#!/bin/sh

cd ~/projects/issue-manager/project || exit
echo "Changed dir to project dir"

current_time=$(date "+%Y%m%d_%H%M%S")
new_file_name=backup_$current_time
backup_dir=$HOME/backups/issue-manager/$new_file_name/

mkdir -p "$HOME/artifacts/issue-manager/postgres/pgdata"
mkdir -p "$HOME/artifacts/issue-manager/app_files"
mkdir -p "$HOME/artifacts/issue-manager/app_files/static"
mkdir -p "$HOME/artifacts/issue-manager/app_files/media"
mkdir -p "$backup_dir"

docker-compose down && docker system prune -f && docker network prune -f
echo "Old docker containers removed"

cp -r ./* "$backup_dir"
echo "Project backed up to $backup_dir"

cp --update ../local_settings.py ./
echo "local_settings.py copied to project dir"

docker-compose up -d --build
echo "Docker image built"


#if [ $? -ne 0 ]; then
#    <ran if unsuccessful> for example exit;
#fi