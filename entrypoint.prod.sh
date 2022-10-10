#!/bin/sh

if [ "$DB_NAME" != "" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --noinput
echo "from account.models import User;
if User.objects.filter(email = '$DJANGO_SUPERUSER_EMAIL').exists():User.objects.get(email='$DJANGO_SUPERUSER_EMAIL').delete();" | python manage.py shell
python manage.py createsuperuser --noinput --name $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --tc True

exec "$@"
