#!/bin/sh
echo "Awaiting PostgreSQL"

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL initiated successfully!"

# Aplica as migrações do banco de dados
echo "Applying DB migrations"
python manage.py collectstatic --noinput
python manage.py migrate

# Inicia o servidor Gunicorn
echo "Initiating gunicorn"
exec "$@"