### Workflow status
![foodgram_workflow](https://github.com/solilov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Дипломный проект курса Python разработчик Yandex Practicum

### <a name="Описание_проекта">Описание</a>

 «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

 - Проект доступен по адресу http://178.154.252.235/recipes


### <a name="Технолигии в проекте">Технолигии в проекте</a>

- **Python 3**,
- **Django REST Framework**, 
- **Git**, 
- **Simple JWT** ,
- **PostgreSQL**,
- **Docker**, 
- **Nginx**,
- **Gunicorn**

### <a name="Workflow">Workflow</a>

- **Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)**,
- **Сборка и доставка докер-образов на Docker Hub**,
- **Автоматический деплой проекта на боевой сервер**,
- **Отправка уведомления в Telegram**


### <a name="Инструкции для развертывания проекта на сервере">Инструкции для развертывания проекта на сервере:</a>

#### <a name="Настройка сервера">Настройка сервера</a>

- Установить Docker и Docker-compose
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
- Проверить установку 
```
sudo  docker-compose --version
```

#### <a name="Подготовка для запуска workflow">Подготовка для запуска workflow</a>

- Выполнить форк проекта в свой аккаунт github
- Клонировать репозиторий и перейти в него в командной строке:
```
https://github.com/solilov/foodgram-project-react.git
```
```
cd foodgram-project-react/
```
- Cоздать и активировать виртуальное окружение, обновить pip:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```
- Локальный запуск автотестов
```
pytest
```
- Скопировать подготовленные файлы docker-compose.yml и nginx.conf из папки infra проекта на сервер
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
```
```
scp nginx.conf <username>@<host>/home/<username>/nginx.conf
```
- В репозитории github добавьте данные для переменных в secrets
```
DOCKER_PASSWORD
SSH_KEY
DOCKER_REPO
DOCKER_USERNAME
USER
HOST
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
POSTGRES_PASSWORD
POSTGRES_USER
TELEGRAM_TO
TELEGRAM_TOKEN
DEBAG
SECRET_KEY
```
- Выполнить push в репозиторий для запуска workflow

#### <a name="После успешного деплоя выполнить на сервере">После успешного деплоя выполнить на сервере</a>
-  Собрать статические файлы:
```
  docker-compose exec backend python manage.py collectstatic --no-input
```
- Применить миграции
```
  docker-compose exec backend python manage.py migrate --noinput
```
- Создать суперпользователя
```
  docker-compose exec backend python manage.py createsuperuser
```
- При необходимости наполнить базу тестовыми данными
```
 docker-compose exec backend python manage.py load_data 
```

### <a name="Автор">Автор</a>
```
Солилов Александр https://github.com/solilov
```