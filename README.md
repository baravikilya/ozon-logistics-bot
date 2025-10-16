# Ozon Logistics Bot

Telegram бот для анализа логистики Ozon продавцов. MVP версия Этапа 1.

## 🚀 Быстрый старт

### Требования
- Python 3.10+
- PostgreSQL база данных
- Telegram Bot Token (от @BotFather)

### Установка

1. **Клонируйте репозиторий и перейдите в директорию:**
   ```bash
   cd ozon_bot/
   ```

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
   CREATE DATABASE ozon_bot_db;
   ```

6. **Запустите бота:**
   ```bash
   python main.py
   ```

## 📋 Структура проекта

```
ozon_bot/
├── core/                   # Конфигурация и база данных
│   ├── __init__.py
│   ├── config.py          # Настройки и переменные окружения
│   └── db.py              # Модели БД и подключение
├── handlers/              # Обработчики Telegram команд
│   ├── __init__.py        # Регистрация роутеров
│   ├── start.py           # Команда /start и главное меню
│   ├── connect.py         # Подключение Ozon API
│   ├── subscription.py    # Управление подпиской
│   └── report.py          # Генерация отчетов
├── services/              # Внешние API сервисы
│   ├── __init__.py
│   ├── ozon_api.py        # Ozon Seller API (заглушка)
│   ├── yookassa.py        # YooKassa платежи (заглушка)
│   └── excel_gen.py       # Генерация Excel отчетов
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
| `DATABASE_URL` | URL PostgreSQL базы | `postgresql+asyncpg://user:pass@localhost/ozon_bot_db` |
| `DEBUG` | Режим отладки | `true` / `false` |
| `TELEGRAM_WEBHOOK_URL` | URL для вебхуков (production) | `https://your-domain.amvera.io` |

### Полные настройки подписки

```bash
# Период trial (дни)
TRIAL_PERIOD_DAYS=7

# Цены подписки (руб)
SUBSCRIPTION_PRICE_1M=919
SUBSCRIPTION_PRICE_6M=4590
SUBSCRIPTION_PRICE_1Y=9190
```

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

## 📱 Использование бота

1. **Запустите бота командой `/start`**
2. **Выберите "Подключить Ozon" для настройки API**
3. **Перейдите к управлению подпиской**
4. **Генерируйте отчеты о логистике**

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

## 📊 Этапы разработки

- **✅ Этап 1 (MVP)**: Базовый каркас с UI и заглушками
- **🔄 Этап 2**: Интеграция с Ozon API
- **🔄 Этап 3**: Платежи через YooKassa
- **🔄 Этап 4**: Генерация реальных Excel отчетов

## 🤝 Поддержка

Для вопросов и поддержки:
- Создайте Issue в репозитории
- Напишите в Telegram: [@support](https://t.me/support)

## 📄 Лицензия

Этот проект является закрытым и предназначен только для внутреннего использования.