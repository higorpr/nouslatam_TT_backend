FROM python:3.11

# Define environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho
WORKDIR /app

# Instala as dependências do sistema, incluindo netcat
RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd --no-install-recommends

# Instala as dependências Python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expõe a porta
EXPOSE 8000

# PONTO CHAVE: Define nosso script como o ponto de entrada, executado via shell.
# Isso garante que a sintaxe do shell ($VAR, while, etc.) funcione.
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
