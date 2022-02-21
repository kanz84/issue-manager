#!/bin/sh
current_time=$(date "+%Y%m%d_%H%M%S")
echo "Current Time : $current_time"

rm -rf venv
python3.6 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

new_fileName=$current_time
echo "New FileName: " "$new_fileName"

mv ~/artifacts/issue-manager-pro/current ~/artifacts/issue-manager-pro/$new_fileName
mkdir ~/artifacts/issue-manager-pro/current
cp -r ./*  ~/artifacts/issue-manager-pro/current/