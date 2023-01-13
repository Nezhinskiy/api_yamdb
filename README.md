## API Yamdb
![example workflow](https://github.com/Nezhinskiy/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект YaMDb собирает отзывы пользователей на различные произведения.

Реализован бэкенд проекта и `REST API` для него.

[Развёрнутый проект](http://51.250.108.30/api/v1/)

## Установка и запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Nezhinskiy/api_yamdb
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
.venv/Scripts/Activate.ps1
```

Установить зависимости:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd api_yamdb
python manage.py migrate
```

Заполнить базу данных:

```
python manage.py loaddb
```

Запустить проект:

```
python manage.py runserver
```

## Примеры запросов к API

Для регистрации пользователя и получения токена необходимо сделать запрос с `json` телом  
```
{
    "email": "string",
    "username": "string"
}
```
на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
После этого в папке `sent_emails` будет создано письмо с кодом подтверждения, который нужно отправить в формате
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/token/
```

Получение списка всех произведений
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Добавление нового отзыва к произведению.
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Полный перечень запросов к API можно получить по эндпоинту `redoc`
```
http://127.0.0.1:8000/redoc
```

## Используемые технологии
```
Python 3.9, Django 2.2 (django rest framework + simplejwt)
```

### Документация API YaMDb 

Документация доступна по эндпойнту: http://localhost/redoc/ 

 

### Авторы: 

 Работа выполнялась в команде, я (Nezhinskiy) был выбран в роли "Тимлида", распределял задачи между коллегами, разбирался и фиксил недочеты с ошибками. 

- [Михаил Нежинский](https://github.com/Nezhinskiy)
- [Константин Сидельников](https://github.com/sidelkin1)
- [Виталий Аксенов](https://github.com/SankakuSpace)
