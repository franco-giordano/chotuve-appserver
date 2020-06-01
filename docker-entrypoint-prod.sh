python manage.py db init
python manage.py db migrate
python manage.py db upgrade

gunicorn -b :$PORT run:app --log-file=- --log-level=debug