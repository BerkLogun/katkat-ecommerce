#!/usr/bin/env python3
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_poc")
django.setup()

if len(sys.argv) != 2:
    print("Usage: create_tenant.py <tenant_slug>")
    sys.exit(1)

tenant = sys.argv[1]

with connection.cursor() as cur:
    cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{tenant}";')

# Run all migrations in the new schema
call_command("migrate", "--schema", tenant, "--noinput")
print(f"✅  Tenant '{tenant}' created.") 