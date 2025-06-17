#!/bin/sh
DB_HOST_TO_CHECK=${DB_HOST:-db}
DB_PORT_TO_CHECK=${DB_PORT:-5432}

echo "Awaiting PostgreSQL at ${DB_HOST_TO_CHECK}:${DB_PORT_TO_CHECK}..."

while ! nc -z $DB_HOST_TO_CHECK $DB_PORT_TO_CHECK; do
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