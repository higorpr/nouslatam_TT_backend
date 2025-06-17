FROM python:3.11

# Define environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define working directory
WORKDIR /app

# Install linux dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd --no-install-recommends

# Install python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy env to container
COPY . .

# Expose port 8000 (Gunicorn)
EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]