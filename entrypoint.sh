#!/bin/sh

# Pausa estratégica para garantir que o banco de dados esteja pronto
echo "Waiting 10 seconds for database to start..."
sleep 10

# Aplica as migrações do banco de dados.
echo "Applying database migrations..."
python manage.py migrate

# Coleta os arquivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Executa o comando principal passado pelo Dockerfile (CMD)
echo "Starting Gunicorn server..."
exec "$@"