# Building the dependencies
FROM python:3.11-slim as builder

# no buffered output and no pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.11-slim

# set this again
WORKDIR /app

# copy the dependencies from the builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# copy the rest of the application code
COPY . .

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Run app as a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Daphne runs on port 8000
EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "bodhibot.asgi:application"]
