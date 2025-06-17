FROM python:3.11

# Define variáveis de ambiente para otimizar o Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema Linux, incluindo o netcat
RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd --no-install-recommends

# Instala as dependências Python diretamente
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8000

# Define nosso script como o ponto de entrada, executado via shell.
# Isso garante que a sintaxe do shell ($VAR, while, etc.) funcione corretamente.
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
