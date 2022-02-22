#!/bin/sh
current_time=$(date "+%Y%m%d_%H%M%S")
echo "Current Time : $current_time"

new_fileName=deploy_$current_time
echo "New FileName: " "$new_fileName"

mkdir ~/artifacts/issue-manager-pro/$new_fileName
cp -r ./*  ~/artifacts/issue-manager-pro/$new_fileName/

cd ~/artifacts/issue-manager-pro/$new_fileName/
python3.6 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

sudo chgrp -R www-data ~/artifacts/issue-manager-pro/$new_fileName
sudo find ~/artifacts/issue-manager-pro/$new_fileName -type d -exec chmod g+rx {} +
sudo find ~/artifacts/issue-manager-pro/$new_fileName -type f -exec chmod g+r {} +

rm ~/artifacts/issue-manager-pro/current
ln -s ~/artifacts/issue-manager-pro/$new_fileName ~/artifacts/issue-manager-pro/current