#!/bin/sh

# Lê as variáveis de ambiente, com fallbacks (valores padrão) para o ambiente local.
# Se DB_HOST não existir, ele usa 'db'. Se DB_PORT não existir, usa '5432'.
DB_HOST_TO_CHECK=${DB_HOST:-db}
DB_PORT_TO_CHECK=${DB_PORT:-5432}

echo "Aguardando o PostgreSQL em ${DB_HOST_TO_CHECK}:${DB_PORT_TO_CHECK}..."

# O loop de verificação que agora usa as variáveis dinâmicas.
while ! nc -z $DB_HOST_TO_CHECK $DB_PORT_TO_CHECK; do
  sleep 0.1
done

echo "PostgreSQL iniciado com sucesso!"

# Comandos de setup do Django
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Aplicando migrações do banco de dados..."
python manage.py migrate

# Inicia o servidor Gunicorn. O comando final do CMD não é mais necessário.
echo "Iniciando o servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application
