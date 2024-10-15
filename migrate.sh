#!/bin/sh

# Migrate the database
python manage.py migrate

# Success message
echo "Migrating to Supabase's Postgre => Completed Successfully"