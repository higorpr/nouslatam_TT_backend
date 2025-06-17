# --- ESTÁGIO 1: BUILDER ---
# Usamos uma imagem completa para instalar dependências que precisam de compilação.
FROM python:3.11-slim as builder

# Define variáveis de ambiente para otimizar o Python e o pip.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes como psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copia apenas o arquivo de dependências para aproveitar o cache do Docker
COPY . /requirements.txt.

# Instala as dependências Python
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# --- ESTÁGIO 2: FINAL ---
# Começamos com uma imagem limpa e enxuta para produção.
FROM python:3.11-slim

# Define as mesmas variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cria um usuário não-root para rodar a aplicação (melhor prática de segurança)
RUN addgroup --system app && adduser --system --group app

# Copia as dependências pré-compiladas do estágio builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instala as dependências a partir das "wheels" locais, o que é muito mais rápido
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copia o código da aplicação e o script de entrypoint
COPY . .

# Garante que o script de entrypoint seja executável
RUN chmod +x /app/entrypoint.sh

# Muda a propriedade de todos os arquivos para o nosso usuário não-root
RUN chown -R app:app /app

# Muda para o usuário não-root
USER app

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8000

# Define o entrypoint que será executado quando o contêiner iniciar
ENTRYPOINT ["/app/entrypoint.sh"]