FROM python:3.11

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema e do Python
RUN apt-get update && apt-get install -y build-essential libpq-dev
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8000

# ENTRYPOINT ["/app/entrypoint.sh"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
