# -- BUILD STAGE --
# Define image used as builder
FROM python:3.11 AS builder

# Define working directory
WORKDIR /app

# Define environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install linux dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install python dependencies from requirements.txt
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# -- FINAL STAGE --
FROM python:3.11

# Install needed dependencies
RUN apt-get update && apt-get install -y netcat-openbsd --no-install-recommends

# Creates non-root user to run the app
RUN addgroup --system app && adduser --system --group app

# Define working directory
WORKDIR /app

# Copy pre-compiled wheels from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy and install pyyhon dependencies
COPY . .

# Expose port 8000 (Gunicorn)
EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]