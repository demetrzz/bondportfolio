# BondPortfolio API

API по корпоративным облигациям.

## Возможности:

- Выдача данных по корпоративным облигациям, включает все основные параметры.
- Регистрация и аутентификация.
- Регистрация сделок покупки/продажи, вывод стоимости портфеля по пользователю.
- Возможность генерировать изображение с g-curve ОФЗ.

## Стек технологий

- Django 4+
- DjangoRestFramework
- Python 3+
- Docker
- Postgres

## Docker

Клонировать проект и создать контейнер:
```sh
git clone https://github.com/demetrzz/bondportfolio
cd bondportfolio
sudo docker compose build
```
Подключиться к контейнеру web:
```sh
docker exec -t -i <ID контейнера> bash
```
Мигрировать базу данных:
```sh
python manage.py migrate
```
Запустить тесты:
```sh
python manage.py test
```
## Заполнение базы данных
```sh
python manage.py db_updater
python manage.py db_rating_fill
python manage.py db_fake_rating_fill
```
Берутся актуальные данные с московской биржи.

## TODO
- обновлять базу данных регулярно используя celery+redis
- полностью покрыть тестами
