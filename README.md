# API Yamdb
������ YaMDb �������� ������ ������������� �� ��������� ������������.

���������� ������ ������� � `REST API` ��� ����.

## ��������� � ������ �������

����������� ����������� � ������� � ���� � ��������� ������:

```
git clone https://github.com/Nezhinskiy/api_yamdb

cd api_yamdb
```

C������ � ������������ ����������� ���������:

```
python -m venv venv

.venv/Scripts/Activate.ps1
```

���������� �����������:

```
pip install -r requirements.txt
```

��������� ��������:

```
cd api_yamdb

python manage.py migrate
```

��������� ���� ������:

```
python manage.py loaddb
```

��������� ������:

```
python manage.py runserver
```

## ������� �������� � API

��� ����������� ������������ � ��������� ������ ���������� ������� ������ � `json` �����  
```
{
    "email": "string",
    "username": "string"
}
```
�� ��������:
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
����� ����� � ����� `sent_emails` ����� ������� ������ � ����� �������������, ������� ����� ��������� � �������
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
�� ��������:
```
http://127.0.0.1:8000/api/v1/auth/token/
```

��������� ������ ���� ������������
```
GET http://127.0.0.1:8000/api/v1/titles/
```
���������� ������ ������ � ������������.
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

������ �������� �������� � API ����� �������� �� ��������� `redoc`
```
http://127.0.0.1:8000/redoc
```

## ������������ ����������
```
Python 3.9, Django 2.2 (django rest framework + simplejwt)
```

## ������
- [������ ���������](https://github.com/Nezhinskiy)
- [���������� �����������](https://github.com/sidelkin1)
- [������� �������](https://github.com/SankakuSpace)