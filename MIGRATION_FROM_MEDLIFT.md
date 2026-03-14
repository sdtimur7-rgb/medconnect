# Миграция Telegram Bot интеграции из MedGPT в MedConnect

## Дата: 14 марта 2026

## Выполненные действия

### 1. Копирование файлов
Все компоненты Telegram Bot интеграции были успешно перенесены из `/Users/timur/Downloads/medlift (2)` в `/Users/timur/Downloads/medconnect`:

```
telegram-bot/
├── bot.py               # Основной код бота с интеграцией Chatwoot API
├── Dockerfile           # Docker образ для бота
├── requirements.txt     # Зависимости: aiogram, aiohttp, python-dotenv
└── README.md           # Документация по работе бота

TELEGRAM_BOT_SETUP.md    # Инструкция по первичной настройке
TELEGRAM_BOT_READY.md    # Финальный отчёт о готовности
setup-chatwoot.sh        # Скрипт инициализации Chatwoot
```

### 2. Обновление конфигурации

#### docker-compose.yml
Добавлен новый сервис `telegram-bot`:
```yaml
telegram-bot:
  build: ./telegram-bot
  container_name: medconnect_telegram_bot
  restart: unless-stopped
  environment:
    - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    - CHATWOOT_URL=http://chatwoot:3000
    - CHATWOOT_API_TOKEN=${CHATWOOT_API_TOKEN}
    - CHATWOOT_ACCOUNT_ID=${CHATWOOT_ACCOUNT_ID}
    - CHATWOOT_INBOX_ID=${CHATWOOT_INBOX_ID}
  volumes:
    - ./telegram-bot/logs:/logs
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy
    chatwoot:
      condition: service_started
```

#### .env
Обновлены переменные окружения для Chatwoot:
```bash
TELEGRAM_BOT_TOKEN=8496809509:AAFiyMpRpUIMLIH1V3uXldCbllmayB9P8Hs
CHATWOOT_API_TOKEN=Y3QdoZz5GECciX4r7Z3Fa4vd
CHATWOOT_ACCOUNT_ID=4
CHATWOOT_INBOX_ID=3
```

### 3. Запуск и проверка
- Бот успешно собран и запущен
- После остановки конфликтующего экземпляра в MedGPT, бот подключился к Telegram API (попытка 21)
- Контейнер работает стабильно и готов к приёму сообщений

### 4. Коммит и push
Все изменения закоммичены и запушены в репозиторий:
```
Commit: 4060577
Сообщение: feat: добавлена полная интеграция Telegram бота с Chatwoot
Репозиторий: github.com/sdtimur7-rgb/medconnect
```

## Ключевые особенности бота

### Функциональность
1. **Приветственное сообщение**: Отправляет welcome текст при команде `/start`
2. **Создание контактов**: Автоматически создаёт контакты в Chatwoot по Telegram user_id
3. **Управление диалогами**: Ищет существующие открытые диалоги перед созданием новых
4. **Отправка сообщений**: Пересылает все сообщения из Telegram в Chatwoot

### Технические детали
- **Фреймворк**: aiogram 3.x (асинхронный)
- **API**: Chatwoot REST API v1
- **Логирование**: Детальные логи в `/logs/debug.log` и `/logs/bot.log`
- **Обработка ошибок**: Полное логирование всех API запросов и ответов

### Настройка welcome текста
Текущий текст в `bot.py`:
```python
welcome_text = """👋 Добро пожаловать в MEDLIFT connect!

Семья Медицинский центр приветствует вас! 

Я помогу вам:
• Записаться на приём
• Получить информацию об услугах
• Узнать стоимость процедур
• Связаться с администратором

Просто напишите ваш вопрос, и я постараюсь помочь!"""
```

## Текущий статус сервисов

### MedConnect (порт 3000)
```
✅ medconnect_postgres          - Running (healthy)
✅ medconnect_redis             - Running (healthy)
✅ medconnect_chatwoot          - Running (5 min ago)
✅ medconnect_chatwoot_sidekiq  - Running
✅ medconnect_telegram_bot      - Running (5 min ago)
✅ medconnect_celery_worker     - Running
✅ medconnect_celery_beat       - Running
```

### MedGPT (остановлен)
Все сервисы MedGPT остановлены для избежания конфликтов по портам и Telegram API.

## Доступ к сервисам

| Сервис | URL | Порт | Примечание |
|--------|-----|------|------------|
| Chatwoot | http://localhost:3000 | 3000 | MedConnect Chatwoot |
| PostgreSQL | localhost:5432 | 5432 | Общая БД для обоих проектов |
| Redis | localhost:6379 | 6379 | Общий Redis |
| API | localhost:8000 | 8000 | MedConnect API (не запущен) |

## Следующие шаги

1. ✅ Бот работает и принимает сообщения
2. 📝 Протестировать полный цикл: Telegram → Bot → Chatwoot
3. 📝 Проверить работу с несколькими пользователями одновременно
4. 📝 Настроить ответы из Chatwoot обратно в Telegram (webhook)
5. 📝 Добавить обработку вложений (фото, документы)

## Решённые проблемы

### TelegramConflictError
**Проблема**: Несколько экземпляров бота пытались подключиться к одному токену  
**Решение**: Остановлен старый бот в MedGPT проекте

### Port conflicts
**Проблема**: Конфликты портов между MedConnect и MedGPT  
**Решение**: Полная остановка MedGPT сервисов

### Chatwoot API токены
**Проблема**: Использовались токены от неправильного Account ID  
**Решение**: Создан новый токен для Account ID 4

## Контакты для связи

- **Telegram Bot**: @rumedconnectbot
- **Bot Token**: `8496809509:AAFiyMpRpUIMLIH1V3uXldCbllmayB9P8Hs`
- **Chatwoot Account ID**: 4
- **Chatwoot Inbox ID**: 3

---

*Документ создан автоматически при миграции*
