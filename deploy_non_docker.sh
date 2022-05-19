#!/bin/sh
current_time=$(date "+%Y%m%d_%H%M%S")

new_fileName=deploy_$current_time

echo "Creating new artifact dir: ~/artifacts/issue-manager-pro/$new_fileName"
mkdir ~/artifacts/issue-manager-pro/$new_fileName

echo "Copying project to ~/artifacts/issue-manager-pro/$new_fileName"
cp -r ./*  ~/artifacts/issue-manager-pro/$new_fileName/

cd ~/artifacts/issue-manager-pro/$new_fileName/

echo "Copying ../local_settings.py to artifact dir"
cp ../local_settings.py ./

echo "Preparing venv"
python3.6 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip

echo "Installing requirements"
pip install -r requirements.txt

echo "Migrating DB"
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Removing old link and creating new link to ~/artifacts/issue-manager-pro/$new_fileName"
rm ~/artifacts/issue-manager-pro/current
ln -s ~/artifacts/issue-manager-pro/$new_fileName ~/artifacts/issue-manager-pro/current