#!/bin/sh

echo "----------Применение миграций---------"
python manage.py migrate --noinput

echo "----------Загрузка ингредиентов в базу данных----------"
python manage.py load_csv 

echo "----------Сбор статики бэкенда----------"
python manage.py collectstatic --no-input

echo "----------Запуск Gunicorn---------"
exec gunicorn foodgram.wsgi --bind 0:8000 --workers 3