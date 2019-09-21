release: python manage.py migrate && python manage.py compilemessages -l pl -l de
web: gunicorn jiaoge.wsgi:application
