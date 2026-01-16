#!/bin/bash
set -e

echo "Waiting for database..."
python << 'PYEOF'
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
            dbname='prompthub',
            connect_timeout=3
        )
        conn.close()
        print("Database is ready!")
        break
    except:
        if i == 29:
            print("Database connection failed!")
            sys.exit(1)
        print(f"Waiting for database... ({i+1}/30)")
        time.sleep(1)
PYEOF

echo "Starting server..."
exec "$@"
