FROM python:3

WORKDIR /app
RUN apt-get update && apt-get install -y curl && apt-get clean
COPY . /app/

RUN pip install -r requirements.txt

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && gunicorn config.wsgi:application --bind 0.0.0.0:8000