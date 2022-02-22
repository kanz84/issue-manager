#!/bin/sh
current_time=$(date "+%Y%m%d_%H%M%S")
echo "Current Time : $current_time"

mkdir ~/artifacts/issue-manager-pro/deploy_$new_fileName
cp -r ./*  ~/artifacts/issue-manager-pro/deploy_$new_fileName/

cd ~/artifacts/issue-manager-pro/deploy_$new_fileName/
python3.6 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

new_fileName=$current_time
echo "New FileName: " "$new_fileName"

rm ~/artifacts/issue-manager-pro/current
ln -s ~/artifacts/issue-manager-pro/$new_fileName ~/artifacts/issue-manager-pro/current