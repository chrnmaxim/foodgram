# Foodgram

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

`Foodgram` — проект, созданный во время обучения в Яндекс Практикуме. Этот проект — часть учебного курса, но он создан полностью самостоятельно.

Цель проекта — дать возможность пользователям создавать и хранить рецепты на онлайн-платформе. Кроме того, можно скачать список продуктов, необходимых для приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.

Проект доступен для ознакомления по ссылке — https://foodgram-practicum.ddns.net/.

Документация `API` проекта в формате `Swagger UI` — https://foodgram-practicum.ddns.net/api/swagger/.

## Технологии:
* Python 3.11
* Django 5.0
* Django REST framework 3.15
* CI/CD  с использованием `GitHub Actions` и `Docker`

## Установка и запуск проекта

Склонируйте проект:
```bash
git clone git@github.com:chrnmaxim/foodgram.git
```
### Запуск проекта в режиме разработки
1. В корневой директории проекта создайте `.env` на основе `.env.example`:
```bash
cp -r .env.example .env
```
2. Запустите базу данных PostgreSQL в Docker контейнере:
```bash
docker compose -f docker-compose.localdb.yml up -d
```
3. Перейдите в директорию `/backend`:
```bash
cd backend/
```
4. Создайте виртуальное окружение:
```bash
python -m venv venv
```
5. Активируйте виртуальное окружениe:
```bash
. venv/Scripts/activate
```
6. Обновите менеджер пакетов pip:
```bash
python -m pip install --upgrade pip
```
7. Установите зависимости из `requirements.txt`:
```bash
pip install -r requirements.txt
```
8. Примените миграции:
```bash
python manage.py migrate
```
9. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```
10. Запустите сервер разработки (виртуальное окружение должно быть активно):
```
python manage.py runserver 
```
### Запуск проекта в `Docker` контейнерах
1. В корневой директории проекта создайте `.env` на основе `.env.example`:
> [!NOTE]
> Измените значение параметра `POSTGRES_HOST` для корректного запуска в контейнере c `localhost` на `db`.
```bash
cp -r .env.example .env
```
2. Запустите проект в `Docker` контейнерах:
```bash
docker compose up -d
```
## Документация API и доступные эндпоинты в формате `Swagger UI`:
* http://127.0.0.1:8000/api/swagger/

