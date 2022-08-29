#!/usr/bin/env sh
echo "Migrating database..."
python manage.py migrate

echo "Preparing translations.."
python manage.py compilemessages -l pl -l de
