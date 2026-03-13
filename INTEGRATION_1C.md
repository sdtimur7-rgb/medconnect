# Интеграция с 1С

Инструкция для настройки синхронизации записей с 1С:Медицина.

## Что нужно от айтишника центра

### 1. Доступ к 1С REST API

Попросите предоставить:

- **URL REST API:** `https://your-center.ru/medical/hs/api/v1`
- **Метод аутентификации:** Basic Auth или Bearer Token
- **Логин/пароль** или **API ключ**

### 2. Формат данных

Попросите пример JSON ответа для одной записи:

```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "patient": {
    "id": "patient_id_123",
    "full_name": "Иванов Иван Иванович",
    "phone": "+79001234567"
  },
  "doctor": {
    "name": "Петров П.П.",
    "specialty": "Терапевт"
  },
  "appointment_time": "2026-03-15T14:30:00",
  "status": "scheduled"
}
```

### 3. Доступные эндпоинты

Необходимые методы API:

```
GET /api/appointments?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
GET /api/patients/{id}
```

### 4. Тестовая среда

Попросите доступ к тестовой базе 1С для разработки.

## Настройка в MedConnect

### 1. Добавить центр через API

```bash
curl -X POST http://localhost:8000/admin/centers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Центр семьи",
    "slug": "center-semyi",
    "telegram_bot_token": "your_bot_token",
    "onec_api_url": "https://your-center.ru/medical/hs/api/v1",
    "onec_api_key": "your_api_key",
    "sms_enabled": true,
    "price_per_confirmation": 50.00,
    "center_info": "Адрес: г. Москва, ул. Примерная, д. 1\nТелефон: +7 (495) 123-45-67"
  }'
```

### 2. Адаптировать код синхронизации

Отредактируйте `integrations/onec.py` под формат API вашего центра:

```python
async def get_appointments(self, date_from: datetime, date_to: datetime):
    response = await self.client.get(
        f"{self.api_url}/api/appointments",  # ваш endpoint
        params={
            "date_from": date_from.strftime("%Y-%m-%d"),  # ваш формат
            "date_to": date_to.strftime("%Y-%m-%d")
        },
        headers={"Authorization": f"Bearer {self.api_key}"}  # ваш метод auth
    )
    
    data = response.json()
    
    # Маппинг полей под вашу структуру
    appointments = []
    for item in data:
        appointments.append({
            "onec_appointment_id": item["id"],
            "patient_phone": item["patient"]["phone"],
            "patient_name": item["patient"]["full_name"],
            "doctor_name": item["doctor"]["name"],
            "specialty": item["doctor"]["specialty"],
            "appointment_time": item["appointment_time"]
        })
    
    return appointments
```

### 3. Проверить синхронизацию

```bash
# Запустить задачу вручную
docker-compose exec celery_worker celery -A scheduler.celery_app call scheduler.tasks.sync_onec_appointments

# Проверить логи
docker-compose logs -f celery_worker
```

## Частые проблемы

### CORS ошибки

Попросите айтишника добавить ваш IP в whitelist 1С HTTP-сервисов.

### Формат даты/времени

1С может возвращать даты в разных форматах:
- `2026-03-15T14:30:00`
- `2026-03-15 14:30:00`
- `15.03.2026 14:30`

Адаптируйте парсинг в `onec.py`:

```python
from dateutil import parser

appointment_time = parser.parse(item["appointment_time"])
```

### Отсутствие телефона

Если у пациента нет телефона в 1С:
- Запись создастся с `phone = None`
- Напоминание не будет отправлено
- В Chatwoot попадёт алерт

### Дубликаты записей

Используем `onec_appointment_id` как уникальный ключ:

```sql
-- В БД уже есть UNIQUE constraint
onec_appointment_id VARCHAR(100) UNIQUE
```

## Тестирование

### 1. Создать тестовую запись в 1С

Попросите создать запись на завтра в 14:00.

### 2. Дождаться синхронизации

Задача запускается каждые 15 минут. Или запустите вручную:

```bash
docker-compose exec celery_worker celery -A scheduler.celery_app call scheduler.tasks.sync_onec_appointments
```

### 3. Проверить в БД

```bash
docker-compose exec postgres psql -U medconnect -d medconnect -c "SELECT * FROM appointments ORDER BY created_at DESC LIMIT 5;"
```

### 4. Проверить напоминание

Должно прийти за 24 часа до записи.

## Поддержка

При проблемах с интеграцией:

1. Проверьте логи: `docker-compose logs -f celery_worker`
2. Проверьте доступность API: `curl https://your-center.ru/medical/hs/api/v1/api/appointments`
3. Проверьте формат ответа
4. Создайте issue в GitHub с примером JSON ответа от 1С
