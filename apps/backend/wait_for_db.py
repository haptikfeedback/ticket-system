import os, time, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Django so we can use its DB config
import django
django.setup()

from django.db import connections
from django.db.utils import OperationalError

attempts = 0
while True:
    try:
        connections["default"].cursor()
        print("Database is ready.")
        sys.exit(0)
    except OperationalError as e:
        attempts += 1
        print(f"DB not ready (attempt {attempts}): {e}. Sleeping 1s...")
        time.sleep(1)
        if attempts >= 60:
            print("Gave up waiting for the database.")
            sys.exit(1)
