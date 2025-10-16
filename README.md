# Telegram Bot

Telegram бот с асинхронной архитектурой на Python. MVP версия с базовым функционалом.

## 🚀 Быстрый старт

### Требования
- Python 3.10+
- PostgreSQL база данных
- Telegram Bot Token (от @BotFather)

### Установка

1. **Клонируйте репозиторий и перейдите в директорию проекта**

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env файл с вашими настройками
   ```

5. **Создайте базу данных:**
   ```sql
   CREATE DATABASE your_db_name;
   ```

6. **Запустите бота:**
   ```bash
   python main.py
   ```

## 📋 Структура проекта

```
├── core/                   # Конфигурация и база данных
│   ├── __init__.py
│   ├── config.py          # Настройки и переменные окружения
│   └── db.py              # Модели БД и подключение
├── handlers/              # Обработчики Telegram команд
│   ├── __init__.py        # Регистрация роутеров
│   ├── start.py           # Команда /start и главное меню
│   ├── connect.py         # Подключение внешних API
│   ├── subscription.py    # Управление подпиской
│   └── report.py          # Генерация отчетов
├── services/              # Внешние API сервисы
│   ├── __init__.py
│   ├── api_service.py     # Внешний API сервис
│   ├── payment_service.py # Платежный сервис
│   └── report_generator.py # Генерация отчетов
├── main.py                # Точка входа приложения
├── requirements.txt       # Зависимости Python
├── Amverafile            # Конфигурация Amvera
└── .env.example          # Шаблон переменных окружения
```

## ⚙️ Конфигурация

### Основные переменные окружения

| Переменная | Описание | Пример |
|------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `DATABASE_URL` | URL PostgreSQL базы | `postgresql+asyncpg://user:pass@localhost/db_name` |
| `DEBUG` | Режим отладки | `true` / `false` |
| `TELEGRAM_WEBHOOK_URL` | URL для вебхуков (production) | `https://your-domain.amvera.io` |

## 🔧 Развертывание

### Amvera (рекомендуется)

1. **Зарегистрируйтесь на [Amvera.io](https://amvera.io)**
2. **Создайте новое приложение**
3. **Загрузите код проекта**
4. **Настройте переменные окружения в панели Amvera**
5. **Разверните приложение**

### Локальная разработка 

Бот запускается в режиме polling для разработки:
```bash
python main.py
```

Для production используйте вебхуки через переменную `TELEGRAM_WEBHOOK_URL`.

## 🔧 Развертывание

### Amvera (рекомендуется)

1. **Зарегистрируйтесь на [Amvera.io](https://amvera.io)**
2. **Создайте новое приложение**
3. **Загрузите код проекта**
4. **Настройте переменные окружения в панели Amvera**
5. **Разверните приложение**

### Локальная разработка

Бот запускается в режиме polling для разработки:
```bash
python main.py
```

Для production используйте вебхуки через переменную `TELEGRAM_WEBHOOK_URL`.

## 🛠️ Разработка

### Добавление новых функций

1. **Handlers**: Добавьте новый файл в `handlers/` и зарегистрируйте в `__init__.py`
2. **Services**: Создайте сервис в `services/` для внешних API
3. **Database**: Добавьте модели в `core/db.py`

### Тестирование

```bash
# Запустите бота локально
python main.py

# Проверьте основные команды в Telegram
/start
# и т.д.
```