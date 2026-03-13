#!/bin/bash

set -e

echo "🚀 Starting MedConnect setup..."

if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before starting services!"
    exit 1
fi

echo "🐳 Building Docker images..."
docker-compose build

echo "🔧 Starting services..."
docker-compose up -d postgres redis

echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

echo "📊 Running database migrations..."
docker-compose run --rm api alembic upgrade head

echo "✅ Starting all services..."
docker-compose up -d

echo ""
echo "🎉 MedConnect is ready!"
echo ""
echo "📍 Available services:"
echo "   - API:      http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Chatwoot: http://localhost:3000"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
