# Создание основы РЕАЛЬНОГО проекта:
## 1. Установка Django
Установка базы - Django + DRFB:
- Django - проект;
- Djangorestframework - drf;
- django-filter - фильтры для drf.
```bash
pip install Django djangorestframework django-filter
```
Сохраняем зависимости в файл.
```bash
pip freeze > requirements.txt
```
Создаеиюм проект в текущей директории.
```bash
django-admin startproject apl .
```
Регистрируем DRF в проекте (`app/settings.py`):
```python
INSTALLED_APPS = [
    ...
]

# добавляем к системным сторонние пакеты:
INSTALLED_APPS += [
    'rest_framework',
    'django_filters',
]
# добавляем свои приллюожения:
INSTALLED_APPS += [
    ...
]
```

## 2. Создание .env файла
Создаём файл `.env` и `example.env`. Первый заносим в `.gitignore`, если его там нет, т.к. в нём будут секретные данные, такие как токены, пароли и т.п.:

```bash
touch .env
echo '.env' >> .gitignore
```
Сам файл для начала заполняем стартовыми настройками ориентируясь на переменные, указанные в `settings.py`:
```bash
SECRET_KEY='super_secret_key'
DEBUG=True
ALLOWED_HOSTS="127.0.0.1 localhost"
LANGUAGE_CODE='en-en'
TIME_ZONE='UTC'
```
И с помощью модуля [python-dotenv](https://pypi.org/project/python-dotenv/) и системного модуля `os' подключаем и используем переменрые окружения в нашем проекте.
```python
import os
from dotenv import load_dotenv


# Загружаем .env в корне проекта
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')
```
> [!INFO] DEFAULT VALUES
> Можно задавать значения по умолчанию:
> ```python
> DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
> ```

> [!INFO] МАССИВЫ
> Массивы значений организуем с помощью метода `split()`:
> ```python
> ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')
> ```
> Таким образом строка будет поделена на части и преобразована в массив.
## 3. Создание БД в PostgreSQL
В настройках приводим раздел _DATABASES_ к следующему виду:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_DB_NAME', 'postgres'),
        'USER': os.getenv('PG_USERNAME', 'postgres'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'postgres'),
        'HOST': os.getenv('PG_HOST', 'localhost'),
        'PORT': os.getenv('PG_PORT', 5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
```
Такая конфигурация будет по умолчанию подключаться к базе проекта на PostgreSQL, а если это не удастся - проект запустится на sqlite3.
Не забываем добавить соответствующие переменные в `.env`-файл:
```bash
...
# DB
PG_DB_NAME='call_helper'
PG_USERNAME='call_helper'
PG_PASSWORD='meg@superp@ssW0rd'
PG_HOST='postgresql'
PG_PORT=5432
```
## 4. Corse Headers
## 5. Настройка static/media
## 6. Настройка локализации
## 7. Создание базовых приложений
## 8. Настройка REST FRAMEWORK 
## 9. Настройка spectacular
## 10. Настройка Joser
## 11. Настройка кастомной пагинации

## Check-list
- [ ] Установка Django.
- [ ] Создание .env файла, вынос констант и подключение к пртекту.
- [ ] Определение BASE_DIR.
- [ ] Создание БД в PostgreSQL, подключение в проект.
- [ ] Разрешить корсы.
- [ ] Настроить static и media.
- [ ] Настройка локализации.
- [ ] Создание приложений api и common.
- [ ] Настройка REST FRAMEWORK.
- [ ] Настройка spectacular.
- [ ] Настройка Joser.
