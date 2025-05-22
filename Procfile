release: bash -c "python manage.py migrate && python manage.py collectstatic --noinput"
web: gunicorn quote_mvp.wsgi:application --log-file -