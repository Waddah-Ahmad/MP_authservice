#!/bin/sh
DATABASE=postgres
SQL_HOST=db
SQL_PORT=5432
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi
python manage.py makemigrations
python manage.py migrate
exec "$@"