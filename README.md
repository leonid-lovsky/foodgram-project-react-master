# Продуктовый помощник

## Описание

«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

## Автор

Леонид Ловский, студент Яндекс.Практикум

## Технологии

* Django Rest Framework
* Docker Compose
* Яндекс.Облако

## Установка

1. Клонируйте проект:

```
git clone git@github.com:leonid-lovsky/foodgram-project-react-master.git
```

2. Перейдите в директорию `infra`:

```
cd infra
```

2. Создайте файл с переменными окружения:

```
touch .env
```

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=FALSE
SECRET_KEY='django-insecure-@sqk$b&6+$w67#iaa$8a+76zf=z=xc---739#d54ws5=q=a&t='
ALLOWED_HOSTS=localhost
```

3. Запустите Docker Compose:

```
docker-compose up -d --build
```

4. Выполните по очереди команды:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```

5. Загрузите список ингредиентов:

```
docker-compose exec backend python manage.py load_data
```


## Примеры запросов


Интерфейс администратора:

```
http://locahost/admin/
```

Пользовательский интерфейс:

```
http://locahost/
```

Документация API:

```
http://locahost/api/docs/
```
