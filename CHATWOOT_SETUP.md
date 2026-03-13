# 🎉 Chatwoot настроен и работает!

## 🔐 Вход в систему

**URL:** http://localhost:3000

**Учётные данные:**
```
Email: admin@medconnect.local
Password: MedConnect2026!
```

## ✅ Что настроено:

- ✅ **Название аккаунта:** MedConnect
- ✅ **Inbox:** MedConnect Сайт
- ✅ **Приветствие:** "Добро пожаловать в MedConnect"
- ✅ **Sidekiq:** для фоновых задач
- ✅ **PostgreSQL с pgvector:** для AI функций

## 📝 Следующие шаги:

### 1. Войдите в Chatwoot
Откройте http://localhost:3000 и войдите с указанными выше данными.

### 2. Настройте профиль
- Измените пароль
- Загрузите аватар
- Укажите ваше имя

### 3. Добавьте агентов (менеджеров)
Settings → Agents → Add Agent

### 4. Настройте Telegram inbox
Для интеграции с вашим Telegram ботом:
- Settings → Inboxes → Add Inbox
- Выберите "Telegram"
- Укажите ваш Bot Token

### 5. Настройте автоответы
Settings → Automation → Canned Responses

## 🔧 Полезные команды:

```bash
# Перезапустить Chatwoot
docker-compose restart chatwoot chatwoot_sidekiq

# Логи Chatwoot
docker-compose logs -f chatwoot

# Логи Sidekiq
docker-compose logs -f chatwoot_sidekiq

# Создать нового администратора через Rails console
docker-compose exec chatwoot bundle exec rails console
```

## 📚 Документация Chatwoot:

- [Официальная документация](https://www.chatwoot.com/docs)
- [API Reference](https://www.chatwoot.com/developers/api)
- [Webhooks](https://www.chatwoot.com/docs/product/channels/api/webhooks)

## 🎨 Кастомизация:

Все настройки можно изменить через веб-интерфейс:
- Settings → Account Settings
- Settings → Inboxes
- Settings → Team Settings

---

**Теперь у вас полноценная панель для менеджеров!** 🚀
