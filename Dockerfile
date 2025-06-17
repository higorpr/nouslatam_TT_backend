# Usamos a imagem padrão do Python 3.11, que é mais completa e simples de usar.
FROM python:3.11

# Define variáveis de ambiente para otimizar o Python em um ambiente de contêiner.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Instala dependências do sistema Linux necessárias para pacotes como psycopg2.
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copia o arquivo de dependências primeiro.
# Isso aproveita o cache do Docker: se o requirements.txt não mudar,
# o passo de instalação de dependências não será executado novamente.
COPY ./requirements.txt .

# Instala as dependências Python.
RUN pip install --no-cache-dir -r requirements.txt

# Agora, copia todo o resto do código do seu projeto para o contêiner.
COPY . .

# Garante que nosso script de inicialização seja executável.
RUN chmod +x /app/entrypoint.sh

# Expõe a porta que o Gunicorn vai usar, para que o Render possa se conectar a ela.
EXPOSE 8000

# Define o script de entrypoint que será executado quando o contêiner iniciar.
# Ele cuidará das migrações e de coletar os arquivos estáticos.
ENTRYPOINT ["/app/entrypoint.sh"]