#!/bin/bash
python manage.py migrate
echo "Starting server"
gunicorn -w 3 -b :8010 config.wsgi:application --reload
