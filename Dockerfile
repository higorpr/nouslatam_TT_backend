# Dockerfile de Diagnóstico

FROM python:3.11

WORKDIR /app

# Apenas copiamos o script de teste
COPY ./hello.py .