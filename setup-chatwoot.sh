#!/bin/bash

# Скрипт для настройки Chatwoot с Telegram ботом

echo "🚀 Настройка Chatwoot и Telegram бота..."

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ждем запуска Chatwoot
echo -e "${YELLOW}⏳ Ожидание запуска Chatwoot...${NC}"
sleep 15

# Создаем базу данных для Chatwoot
echo -e "${YELLOW}📦 Создание базы данных Chatwoot...${NC}"
docker-compose exec -T postgres psql -U medgpt -d postgres -c "CREATE DATABASE chatwoot;" 2>/dev/null || echo "База данных уже существует"

# Запускаем миграции
echo -e "${YELLOW}🔄 Запуск миграций Chatwoot...${NC}"
docker-compose exec -T chatwoot bundle exec rails db:prepare

# Создаем администратора
echo -e "${YELLOW}👤 Создание администратора...${NC}"
docker-compose exec -T chatwoot bundle exec rails runner "
u = User.find_or_create_by!(email: 'admin@medconnect.ru') do |user|
  user.password = 'MedConnect2026!'
  user.password_confirmation = 'MedConnect2026!'
  user.name = 'Admin'
end
puts 'Admin created: admin@medconnect.ru'
puts 'Password: MedConnect2026!'

# Создаем аккаунт
account = Account.find_or_create_by!(name: 'MedConnect')
AccountUser.find_or_create_by!(account: account, user: u) do |au|
  au.role = :administrator
end

puts 'Account ID: ' + account.id.to_s

# Создаем API ключ
access_token = u.create_access_token
puts 'API Token: ' + access_token.token

# Создаем Telegram Inbox
inbox = Inbox.find_or_create_by!(account: account, channel_type: 'Channel::Api') do |i|
  i.name = 'Telegram Bot'
  i.channel = Channel::Api.create!(account: account)
end

puts 'Inbox ID: ' + inbox.id.to_s
puts 'Inbox Identifier: ' + inbox.channel.identifier if inbox.channel

# Настраиваем приветственное сообщение
inbox.update!(
  greeting_enabled: true,
  greeting_message: 'Привет! 👋 Добро пожаловать в MedConnect'
)
"

echo -e "${GREEN}✅ Настройка завершена!${NC}"
echo ""
echo -e "${GREEN}🔗 Ссылки:${NC}"
echo -e "  Chatwoot Admin: ${YELLOW}http://localhost:3000${NC}"
echo -e "  Email: ${YELLOW}admin@medconnect.ru${NC}"
echo -e "  Password: ${YELLOW}MedConnect2026!${NC}"
echo ""
echo -e "${YELLOW}⚠️  Скопируйте API Token и обновите .env файл:${NC}"
echo -e "  CHATWOOT_API_TOKEN=<token from above>"
echo -e "  CHATWOOT_ACCOUNT_ID=<account_id from above>"
echo -e "  CHATWOOT_INBOX_ID=<inbox_id from above>"
echo ""
echo -e "${GREEN}Затем перезапустите telegram-bot:${NC}"
echo -e "  docker-compose restart telegram-bot"
