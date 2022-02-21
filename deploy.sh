rm -rf venv
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate