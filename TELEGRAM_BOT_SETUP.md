# 🤖 Telegram Bot + Chatwoot Integration для MedGPT

## ✅ Что сделано

1. **Создан Telegram бот** (`telegram-bot/bot.py`)
   - Обработка команды `/start` с приветственным сообщением
   - Пересылка всех сообщений в Chatwoot
   - Создание контактов и бесед автоматически

2. **Добавлен Chatwoot** в `docker-compose.yml`
   - Chatwoot Web (порт 3001)
   - Chatwoot Sidekiq (фоновые задачи)
   - Redis (для очередей)

3. **Настроен Telegram бот токен**: `8496809509:AAFiyMpRpUIMLIH1V3uXldCbllmayB9P8Hs`

## 🚨 Текущая проблема

Chatwoot не запускается из-за того, что нужно:
1. Сначала запустить миграции базы данных
2. Создать супер-администратора
3. Создать API токен для бота

## 💡 Решение

### Вариант 1: Использовать существующий Chatwoot (РЕКОМЕНДУЕТСЯ)

У вас уже запущен Chatwoot на порту 3000 из другого проекта (MedConnect). Можно:

1. Подключить бот к нему:
```bash
# В .env файле установите:
CHATWOOT_URL=http://localhost:3000
CHATWOOT_API_TOKEN=<получите из MedConnect Chatwoot>
CHATWOOT_ACCOUNT_ID=1
CHATWOOT_INBOX_ID=<ID Telegram inbox>
```

2. Создать новый Telegram Inbox в существующем Chatwoot:
   - Откройте http://localhost:3000
   - Settings → Inboxes → Add Inbox → API
   - Имя: "MedGPT Telegram"
   - Скопируйте Inbox ID

3. Запустить только бот:
```bash
docker-compose up -d telegram-bot
```

### Вариант 2: Настроить Chatwoot с нуля

Если хотите отдельный Chatwoot для MedGPT:

1. Остановить старый Chatwoot:
```bash
cd "/Users/timur/Downloads/medconnect"
docker-compose stop chatwoot
```

2. Настроить новый:
```bash
cd "/Users/timur/Downloads/medlift (2)"

# Создать БД и мигр� через Rails console
docker-compose run --rm chatwoot bundle exec rails db:create db:migrate

# Создать админа
docker-compose run --rm chatwoot bundle exec rails runner "
u = User.create!(email: 'admin@medgpt.ru', password: 'MedGPT2026!', name: 'Admin')
account = Account.create!(name: 'MedGPT')
AccountUser.create!(account: account, user: u, role: :administrator)
token = u.create_access_token
puts 'API Token: ' + token.token
"
```

## 📝 Следующие шаги

После настройки Chatwoot:

1. Обновите `.env` с правильными значениями
2. Перезапустите бот: `docker-compose restart telegram-bot`
3. Напишите боту `/start` в Telegram
4. Проверьте что сообщения приходят в Chatwoot

## 🔗 Полезные ссылки

- Telegram Bot: https://t.me/<ваш_бот>
- Chatwoot (MedConnect): http://localhost:3000
- Chatwoot (MedGPT): http://localhost:3001
- MedGPT API: http://localhost:8000

## 📖 Документация

Подробная инструкция в `telegram-bot/README.md`
