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
> [!TIP]
> Можно задавать значения по умолчанию:
> ```python
> DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
> ```

> [!TIP]
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
Создадим базу данных и пользователя в Postgres.
```sql
CREATE DATABASE call_helper;
CREATE USER call_helper WITH PASSWORD 'meg@superp@ssW0rd';
GRANT ALL PRIVILEGES ON DATABASE call_helper TO call_helper;ALTER DATABASE call_helper OWNER TO call_helper;
ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO call_helper;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO call_helper;
GRANT CREATE ON SCHEMA public TO call_helper;
```
И в заключении выполним миграции и создадим суперпользователя.
```bash
python manage.py migrate
python manage.py createsuperuser
```
## 4. Cors Headers
Ставим пакет:
```bash
pip install django-cors-headers
pip freeze | grep cors-headers >> requirements.txj
```
В фал `.env` добавляем переменую:
```bash
CORS_ALLOW_HEADERS="*"
```
А `settings.py` следует доработать следующим образом:
```python
# packages
INSTALLED_APPS += [
    ...
    'corsheaders',
]

...
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    # дьюолжно быть размещено перед CommonMiddleware и подобным
    ...
    'django.middleware.common.CommonMiddleware',
    ...
]

##############################
# CORS HEADERS
##############################
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = os.getenv('CORS_ALLOW_HEADERS').split(' ')
CORS_COOKIE_SECURE = False
```
## 5. Настройка static/media
```python
##############################
# STATIC AND MEDIA
##############################
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```
## 6. Настройка локализации
```python
##############################
# LOCALIZATION
##############################
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')
TIME_ZONE = os.getenv('TIME_ZONE')
USE_I18N = True
USE_TZ = True
```
## 7. Создание базовых приложений
Создаем два основных приложений. `api` и `core`.
```bash
python manage.py startapp core
python manage.py startapp api
```
После этого добавляем директории с миграциями в `.gitignore`.
Во вновь созданной директории `api/` создадим файл `urls.py` со следующим содержимым:
```python
app_name = "api"

urlpatterns = []
```
В основном файле путей (`app/urls.py`) подключаем api:
```python
...
from django.urls import path, include

urlpatterns = [
    ...
    path('api/', include('api.urls')),
]
```
## 8. Настройка REST FRAMEWORK
Добавляем в `settings.py`.
```python
###########################
# DJANGO REST FRAMEWORK
###########################
REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.IsAuthenticated',),

        'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_simplejwt.authentication.JWTAuthentication',
                'rest_framework.authentication.BasicAuthentication',
            ],

        'DEFAULT_PARSER_CLASSES': [
                'rest_framework.parsers.JSONParser',
                'rest_framework.parsers.FormParser',
                'rest_framework.parsers.MultiPartParser',
                'rest_framework.parsers.FileUploadParser',
            ],
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
}
```
## 9. Настройка spectacular
```bash
pip install drf_spectacular
pip freeze | grep spectacular >> requirements.txt
```
В `settings.py`, после всех приложенийнеобходимо добавить spectacular.
```python
# after apps
INSTALLED_APPS += [
    'drf_spectacular',
]
```
> [!IMPORTANT]
> `spectacular` нужно добавлять именно в конце перечня приложений. В КОНЦЕ - иначе всей мультивселенной наступит фиолетовый Танос.
И настройки `spectacular`:
```python
##############################
# DRF_SPECTACULAR
##############################
SPECTACULAR_SETTINGS = {
    'TITLE': 'Call Helper',
        'DESCRIPTION': 'Call Helper',
    'VERSION': '0.0.1',

    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.BasicAuthentication',
    ],

    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        "displayOperationId": True,
        "syntaxHighlight.active": True,
        "syntaxHighlight.theme": "arta",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,

    'ENABLE_DJANGO_DEPLOY_CHECK': False,
    'DISABLE_ERRORS_AND_WARNINGS': True,
}
```
Затем в директории `api` создаём поддиректорию `specular` и ещё несколько файлов.
```bash
md -p api/spectacular
touch {config,urls}.py
```
В файле `urls.py` подключаем api `scema`.
```python
from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView


urlpatterns = [
    path('',
         SpectacularSwaggerView.as_view(
         url_name='schema'), name='swagger-ui'),
]
```
В созданном на 7 шаге `api\urls.py` добавляем ю
```python
from api.spectacular.urls import urlpatterns as doc_url

...

urlpatterns += doc_url
```
Основной файл урлов (`app/urls.py`) приводим к виду:
```python
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('schema/',
         SpectacularAPIView.as_view(),
         name='schema'),
]
```
Таким образом по адресу `http://<IP>/api` можем наблюдать документированную api. По мере расширения функционала проекта буем и документацию пополнять.
## 10. Настройка Djoser
Устанавливаем и добавляем в INSTALLED_APPS
```bash
pip install djoser
pip freeze | grep djoser >> requirements.txt
```
```python
# packages
INSTALLED_APPS += [
    ...
    'djoser',
]
```
Затем добавляем настройки djoser.
```python
from datetime import timedelta

...

##############################
# DJANGO REST FRAMEWORK
##############################
REST_FRAMEWORK = {
    ...

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],

    ...
}

...

##############################
# DJOSER
##############################
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {},
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}
```
## 11. Настройка кастомной пагинации

## Check-list
- [x] Установка Django.
- [x] Создание .env файла, вынос констант и подключение к пртекту.
- [x] Создание БД в PostgreSQL, подключение в проект.
- [x] Разрешить корсы.
- [x] Настроить static и media.
- [x] Настройка локализации.
- [x] Создание приложений api и common.
- [x] Настройка REST FRAMEWORK.
- [x] Настройка spectacular.
- [x] Настройка Djoser.
