#!/bin/sh

# --- Seção de Depuração ---
# Imprime as variáveis de ambiente para que possamos vê-las nos logs do Railway.
echo "--- Verificando variáveis de ambiente ---"
echo "Valor de DB_HOST recebido: [${DB_HOST}]"
echo "Valor de DB_PORT recebido: [${DB_PORT}]"
echo "--- Fim da verificação ---"

# Lê as variáveis de ambiente, com fallbacks para o ambiente local
DB_HOST_TO_CHECK=${DB_HOST:-db}
DB_PORT_TO_CHECK=${DB_PORT:-5432}

echo "Aguardando o PostgreSQL em ${DB_HOST_TO_CHECK}:${DB_PORT_TO_CHECK}..."

# O loop de verificação
while ! nc -z $DB_HOST_TO_CHECK $DB_PORT_TO_CHECK; do
  sleep 0.1
done

echo "PostgreSQL iniciado com sucesso!"

# Comandos de setup
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Aplicando migrações do banco de dados..."
python manage.py migrate

# PONTO CHAVE: O script agora inicia o Gunicorn diretamente.
echo "Iniciando o servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 core.wsgi:application
