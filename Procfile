release: python manage.py migrate && python manage.py compilemessages -l pl
web: gunicorn jiaoge.wsgi:application
