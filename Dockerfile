FROM python:3.11

# Define variáveis de ambiente para otimizar o Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema Linux
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copia e instala as dependências Python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta para a rede interna do Render
EXPOSE 8000