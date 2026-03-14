# ✅ Telegram Bot + Chatwoot - Настройка завершена!

## 🎉 Что работает

### 1. Telegram Bot
- **Username**: @rumedconnectbot
- **Token**: `8496809509:AAFiyMpRpUIMLIH1V3uXldCbllmayB9P8Hs`
- **Статус**: 🟢 Запущен и работает

### 2. Chatwoot
- **URL**: http://localhost:3000
- **Login**: admin@medconnect.ru
- **Password**: MedConnect2026!
- **Account**: MedConnect (ID: 1)
- **Inbox**: "MedGPT Telegram" (ID: 2)
- **API Token**: `2SH7ye8toXRUr3GBZULdKQbF`

### 3. Интеграция
- ✅ Бот подключен к Chatwoot
- ✅ Все сообщения из Telegram синхронизируются с Chatwoot
- ✅ Автоматическое создание контактов
- ✅ Автоматическое создание бесед

## 📱 Как использовать

### Для пользователей

1. Найдите бота в Telegram: **@rumedconnectbot**
2. Отправьте `/start`
3. Начните общаться - все сообщения будут видны операторам в Chatwoot

### Для операторов

1. Откройте **http://localhost:3000**
2. Войдите с учетными данными выше
3. Перейдите в **Conversations** → **MedGPT Telegram**
4. Все сообщения из Telegram появятся здесь
5. Отвечайте прямо из Chatwoot

## 🔧 Управление

### Проверить статус бота
```bash
cd "/Users/timur/Downloads/medlift (2)"
docker-compose ps telegram-bot
```

### Посмотреть логи
```bash
docker-compose logs -f telegram-bot
```

### Перезапустить бота
```bash
docker-compose restart telegram-bot
```

### Остановить бота
```bash
docker-compose stop telegram-bot
```

## 🌐 Русский интерфейс Chatwoot

Чтобы переключить Chatwoot на русский язык:

1. Откройте http://localhost:3000
2. Войдите в систему
3. Нажмите на свой профиль (правый верхний угол)
4. Выберите **Profile Settings**
5. В разделе **Language** выберите **Русский**
6. Сохраните изменения

## 📊 Архитектура

```
Telegram User
     ↓
@rumedconnectbot (8496809509:...)
     ↓
Docker Container: medgpt-telegram-bot
     ↓
Chatwoot API (http://localhost:3000)
     ↓
Inbox: "MedGPT Telegram" (ID: 2)
     ↓
Operators в Chatwoot Dashboard
```

## 🎯 Следующие шаги (опционально)

### 1. Двусторонняя синхронизация
Сейчас сообщения идут только Telegram → Chatwoot.  
Чтобы операторы могли отвечать через Chatwoot:
- Добавьте webhook в Chatwoot
- Настройте отправку ответов обратно в Telegram

### 2. Webhook для Chatwoot
```python
# В server/main.py добавьте endpoint:
@app.post("/api/chatwoot/webhook")
async def chatwoot_webhook(data: dict):
    # Обработка ответов от операторов
    # Отправка в Telegram через bot API
    pass
```

### 3. Улучшения бота
- Добавить больше команд (`/help`, `/about`)
- Добавить кнопки quick replies
- Интеграция с MedGPT AI для автоответов

## 📞 Поддержка

Если бот не работает:

1. Проверьте что контейнер запущен: `docker-compose ps telegram-bot`
2. Проверьте логи: `docker-compose logs telegram-bot`
3. Убедитесь что Chatwoot доступен: `curl http://localhost:3000`
4. Проверьте токен бота в `.env` файле

## 🔐 Безопасность

⚠️ **Важно для продакшн:**
- Смените пароль администратора Chatwoot
- Используйте HTTPS для Chatwoot
- Храните API токены в секретах
- Настройте rate limiting для бота

---

**Готово!** Ваш Telegram бот синхронизирован с Chatwoot. 🚀
