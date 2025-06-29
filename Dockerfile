FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

RUN python manage.py collectstatic --noinput

# Run migrations, collectstatic, and start the server
CMD ["sh", "-c", "python manage.py makemigrations && \
                  python manage.py migrate && \
                  gunicorn boundarybahira.wsgi:application --bind 0.0.0.0:8000"]
