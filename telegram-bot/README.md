# MedConnect Telegram Bot + Chatwoot Integration

## 🚀 Быстрый старт

### 1. Запуск всех сервисов

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (база данных)
- Redis (кеш и очереди)
- Backend API (FastAPI)
- Frontend (React)
- Chatwoot (платформа для общения)
- Chatwoot Sidekiq (фоновые задачи)
- Telegram Bot (ваш бот)

### 2. Настройка Chatwoot

После запуска сервисов выполните:

```bash
./setup-chatwoot.sh
```

Этот скрипт:
- Создаст базу данных для Chatwoot
- Выполнит миграции
- Создаст администратора
- Создаст API ключ
- Создаст Telegram Inbox
- Настроит приветственное сообщение

**ВАЖНО!** Скопируйте из вывода скрипта:
- `API Token`
- `Account ID`
- `Inbox ID`

### 3. Обновление конфигурации

Откройте файл `.env` и обновите:

```env
CHATWOOT_API_TOKEN=<ваш_api_token>
CHATWOOT_ACCOUNT_ID=<ваш_account_id>
CHATWOOT_INBOX_ID=<ваш_inbox_id>
```

### 4. Перезапуск Telegram бота

```bash
docker-compose restart telegram-bot
```

## 📱 Использование

### Для пользователей

1. Откройте Telegram и найдите вашего бота
2. Отправьте `/start`
3. Начните общение - все сообщения будут синхронизироваться с Chatwoot

### Для операторов

1. Откройте Chatwoot: http://localhost:3000
2. Войдите:
   - Email: `admin@medconnect.ru`
   - Password: `MedConnect2026!`
3. Все сообщения из Telegram будут появляться в inbox "Telegram Bot"
4. Отвечайте на сообщения прямо из Chatwoot

## 🔧 Настройка русского интерфейса Chatwoot

1. Войдите в Chatwoot
2. Нажмите на свой профиль (правый верхний угол)
3. Выберите "Profile Settings"
4. В разделе "Language" выберите "Русский"
5. Сохраните изменения

## 🔌 API Endpoints

### Backend API
- URL: http://localhost:8000
- Docs: http://localhost:8000/docs

### Chatwoot API
- URL: http://localhost:3000/api/v1
- Docs: https://www.chatwoot.com/developers/api/

## 📊 Мониторинг

### Логи всех сервисов
```bash
docker-compose logs -f
```

### Логи конкретного сервиса
```bash
docker-compose logs -f telegram-bot
docker-compose logs -f chatwoot
```

### Статус сервисов
```bash
docker-compose ps
```

## 🛠 Troubleshooting

### Telegram бот не отвечает

1. Проверьте токен бота в `.env`
2. Проверьте логи: `docker-compose logs telegram-bot`
3. Убедитесь что Chatwoot запущен

### Сообщения не появляются в Chatwoot

1. Проверьте `CHATWOOT_API_TOKEN` в `.env`
2. Проверьте `CHATWOOT_INBOX_ID`
3. Проверьте логи бота на ошибки

### Chatwoot не запускается

1. Проверьте что PostgreSQL запущен: `docker-compose ps postgres`
2. Проверьте логи: `docker-compose logs chatwoot`
3. Попробуйте пересоздать: `docker-compose up -d --force-recreate chatwoot`

## 📝 Полезные команды

```bash
# Перезапуск всех сервисов
docker-compose restart

# Остановка всех сервисов
docker-compose down

# Полная очистка (удалит все данные!)
docker-compose down -v

# Обновление образов
docker-compose pull

# Пересборка образов
docker-compose build --no-cache
```

## 🔐 Безопасность

**ВАЖНО!** Перед продакшн деплоем:

1. Смените пароль администратора Chatwoot
2. Сгенерируйте новый `CHATWOOT_SECRET_KEY`
3. Используйте сильный `POSTGRES_PASSWORD`
4. Настройте HTTPS
5. Настройте firewall

## 📚 Дополнительная информация

- [Документация Chatwoot](https://www.chatwoot.com/docs/)
- [Документация aiogram](https://docs.aiogram.dev/)
- [API Telegram Bot](https://core.telegram.org/bots/api)
