# MedConnect

**White-label платформа для медицинских центров**

Система автоматизации записи пациентов с Telegram-ботом, ИИ-менеджером, SMS уведомлениями и биллингом по подтверждённым записям.

## Технологический стек

- **Backend:** Python 3.11 + FastAPI
- **Bot:** aiogram 3.x + Anthropic Claude API
- **БД:** PostgreSQL 15 + SQLAlchemy
- **Очереди:** Celery + Redis
- **Панель:** Chatwoot (self-hosted)
- **SMS:** СМСЦентр API
- **Деплой:** Docker Compose

## Основные возможности

- 📅 **Синхронизация с 1С** - автоматическая загрузка записей
- 🤖 **Telegram бот** - напоминания с кнопками подтверждения
- 🧠 **ИИ-менеджер** - Claude отвечает на типовые вопросы
- 📱 **SMS дублирование** - если пациент не подтвердил в Telegram
- 💬 **Chatwoot панель** - менеджеры видят сложные вопросы
- 💰 **Биллинг** - оплата только за подтверждённые записи
- 📊 **Отчёты** - ежемесячные PDF с детализацией

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/sdtimur7-rgb/medconnect.git
cd medconnect
```

### 2. Настроить переменные окружения

```bash
cp .env.example .env
# Отредактируйте .env файл с вашими ключами
```

### 3. Запустить через Docker Compose

```bash
docker-compose up -d
```

### 4. Применить миграции БД

```bash
docker-compose exec api alembic upgrade head
```

## Сервисы

После запуска доступны:

- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Chatwoot:** http://localhost:3000
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

## Структура проекта

```
medconnect/
├── bot/                    # Telegram бот
│   ├── main.py            # Запуск бота
│   ├── handlers/          # Обработчики сообщений
│   ├── keyboards.py       # Inline кнопки
│   └── ai_manager.py      # ИИ-менеджер Claude
├── api/                   # FastAPI приложение
│   ├── main.py           # API сервер
│   └── routes/           # Эндпоинты
├── scheduler/            # Celery задачи
│   ├── celery_app.py    # Конфигурация
│   ├── tasks.py         # Периодические задачи
│   └── reminders.py     # Логика напоминаний
├── integrations/        # Внешние API
│   ├── onec.py         # 1С REST API
│   ├── sms.py          # СМСЦентр
│   └── chatwoot.py     # Chatwoot API
├── db/                  # База данных
│   ├── models.py       # SQLAlchemy модели
│   ├── crud.py         # Операции с БД
│   └── migrations/     # Alembic миграции
├── billing/            # Биллинг
│   ├── counter.py     # Счётчик подтверждений
│   └── reports.py     # PDF отчёты
└── core/              # Общие модули
    ├── config.py     # Настройки
    ├── logging.py    # Логирование
    └── exceptions.py # Исключения
```

## Конфигурация

Основные переменные окружения в `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://medconnect:password@postgres/medconnect

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_TELEGRAM_ID=your_telegram_id

# Anthropic Claude
ANTHROPIC_API_KEY=your_api_key

# SMS
SMSC_LOGIN=your_login
SMSC_PASSWORD=your_password

# Chatwoot
CHATWOOT_API_URL=http://chatwoot:3000
CHATWOOT_API_TOKEN=your_token
```

## Архитектура

```
┌─────────────┐
│  Пациент    │──> Telegram Bot ──> ИИ-менеджер (Claude)
└─────────────┘           │
                         ↓
                   ┌──────────┐
                   │   БД     │
                   └──────────┘
                         ↑
                         │
    ┌──────────┐    Celery    ┌──────────┐
    │   1С     │──> Sync ──────│ Redis    │
    └──────────┘              └──────────┘
                         │
                         ↓
                   Напоминания ──> SMS
                         │
                         ↓
                   ┌──────────┐
                   │ Chatwoot │<── Менеджер
                   └──────────┘
```

## Разработка

### Создание миграции

```bash
docker-compose exec api alembic revision --autogenerate -m "description"
docker-compose exec api alembic upgrade head
```

### Просмотр логов

```bash
docker-compose logs -f bot
docker-compose logs -f api
docker-compose logs -f celery_worker
```

### Тестирование бота

```bash
# Отправьте /start вашему боту в Telegram
```

## Планировщик задач

Celery Beat выполняет:

- **Каждые 15 минут** - синхронизация с 1С
- **Каждые 30 минут** - отправка напоминаний за 24ч
- **Каждые 30 минут** - отправка напоминаний за 2ч
- **1го числа в 3:00** - генерация месячных счетов
- **Каждые 10 минут** - проверка здоровья системы

## Мониторинг

Health check endpoint:

```bash
curl http://localhost:8000/health
```

Ответ:

```json
{
  "status": "ok",
  "timestamp": "2026-03-14T12:00:00",
  "services": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

## Биллинг

Платформа создаёт `billing_event` при каждом подтверждении записи:

1. Пациент нажимает "✅ Подтверждаю"
2. Статус записи → `confirmed`
3. Создаётся `billing_event` с суммой `center.price_per_confirmation`
4. В конце месяца генерируется счёт (invoice)

## Документация API

После запуска доступна по адресам:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Лицензия

MIT

## Поддержка

По вопросам: [Issues](https://github.com/sdtimur7-rgb/medconnect/issues)
