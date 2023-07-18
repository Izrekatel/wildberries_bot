# wildberries_bot

# Автор проекта
Гельруд Борис (https://github.com/Izrekatel/)

## Описание проекта:
"wildberries_bot" - это телеграм бот, с помощью которого подписчик целевого канала
может отслеживать позиции на сайте wildberries.ru, формировать отчет остатков по позициям и складам,
Проект состоит из telegram-бота, бэкенда на Django, базы данных на postgresql. Все управляется через
сервер NGNIX.

## Стек:
- Python
- PostgreSQL
- Nginx
- Django
- Git
- Docker
- Poetry
- Pre-commit
- Python-telegram-bot
- Aiohttp
- Asyncio
- Selenium

### 1. Запуск проекта в контейнерах Docker

#### 1. Создать .env файл из env.example (в папках bot, expert_system и в корневой)

#### 2. Запустить Docker

#### 4. Поднимаем контейнеры:
```bash
docker-compose up -d --build
```
#### 5. Локальные адреса проекта:
Главная страница
```
http://127.0.0.1/
```
Админка Django
```
http://127.0.0.1/admin/
```
Адрес API
```
http://127.0.0.1/api/
```

### 2. Установка для локальной разработки

1. Установите Poetry

Для Linux, macOS, Windows (WSL):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Для Windows (Powershell):
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
Чтобы скрипты выполнялись, PowerShell может попросить у вас поменять политики.

В macOS и Windows сценарий установки предложит добавить папку с исполняемым файлом poetry в переменную PATH. Сделайте это, выполнив следующую команду:

macOS (не забудьте поменять borisgelrud на имя вашего пользователя)
```bash
export PATH="/Users/borisgelrud/.local/bin:$PATH"
```

Windows
```bash
$Env:Path += ";C:\Users\borisgelrud\AppData\Roaming\Python\Scripts"; setx PATH "$Env:Path"
```

Для проверки установки выполните следующую команду:
```bash
poetry --version
```
Опционально! Изменить местонахождение окружения в папке проекта
```bash
poetry config virtualenvs.in-project true
```

Установка автодополнений bash (опцонально)
```bash
poetry completions bash >> ~/.bash_completion
```

Создание виртуально окружения
```bash
poetry env use python3.11
```

2. Установите виртуальное окружение
Важно: poetry ставится и запускается для каждого сервиса отдельно.

Перейти в одну из папок сервиса, например:
```bash
cd bot
```

Установка зависимостей (для разработки)
```bash
poetry install
```

Запуск оболочки и активация виртуального окружения

```bash
your@device:~/your_project_pwd/your_service$ poetry shell
```

Проверка активации виртуального окружения
```bash
poetry env list
```


* Полная документация: https://python-poetry.org/docs/#installation
* Настройка для pycharm: https://www.jetbrains.com/help/pycharm/poetry.html


3. Установка pre-commit

Модуль pre-commit уже добавлен в lock, таким образом после настройки виртуального окружения, должен установится автоматически.
Проверить установку pre-commit можно командой (при активированном виртуальном окружении):
```bash
pre-commit --version
```

Если pre-commit не найден, то его нужно установить по документации https://pre-commit.com/#install

```bash
poetry add pre-commit
```

4. Установка hook

Установка осуществляется hook командой
```bash
pre-commit install --all
```

В дальнейшем при выполнении команды `git commit` будут выполняться проверки перечисленные в файле `.pre-commit-config.yaml`.


5. Запуск backend сервера expert_system (после запуска всего проекта в контейнерах Docker)

#### 1. Изменить значение DB_HOST на "localhost" в expert_system/.env

#### 2. Войти в папку expert_system
```bash
cd expert_system
```
#### 3. Войти в оболочку виртуального окружения poetry
```bash
poetry shell
```

#### 4. Запустить локальный backend сервер expert_system
```poetry
python manage.py runserver
```
#### 5. Адреса API локального backend сервера expert_system

Локальные адреса проекта:

Главная страница
```
http://127.0.0.1:8000/
```
Админка Django
```
http://127.0.0.1/admin:8000/
```
Адрес API
```
http://127.0.0.1/api:8000/
```


6. Запуск telegram-bot (после запуска всего проекта в контейнерах Docker)

#### 1. Остановите контейнер "bot_container" в Docker
```bash
docker stop bot_container
```

#### 2. Войти в папку bot
```bash
cd bot
```

#### 3. Войти в оболочку виртуального окружения poetry
```bash
poetry shell
```

#### 4. Войти в оболочку виртуального окружения poetry
```poetry
python telegram_bot.py
```
