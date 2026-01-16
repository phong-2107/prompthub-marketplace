#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL..."
python << END
import time
import psycopg2
import sys

for i in range(30):
    try:
        conn = psycopg2.connect(
            host='db',
            port=5432,
            user='postgres',
            password='postgres',
            dbname='prompthub'
        )
        conn.close()
        print("PostgreSQL is ready!")
        sys.exit(0)
    except psycopg2.OperationalError:
        print(f"PostgreSQL is unavailable - sleeping (attempt {i+1}/30)")
        time.sleep(1)

print("PostgreSQL failed to start")
sys.exit(1)
END

echo "Waiting for Redis..."
python << END
import time
import redis
import sys

for i in range(30):
    try:
        r = redis.Redis(host='redis', port=6379)
        r.ping()
        print("Redis is ready!")
        sys.exit(0)
    except redis.exceptions.ConnectionError:
        print(f"Redis is unavailable - sleeping (attempt {i+1}/30)")
        time.sleep(1)

print("Redis failed to start")
sys.exit(1)
END

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if not exists
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"
