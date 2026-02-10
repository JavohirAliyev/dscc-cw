#!/bin/bash
# Deployment script for Library Management System

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Pull latest code
echo "📦 Pulling latest code from repository..."
git pull origin main

# Pull latest Docker images
echo "🐳 Pulling latest Docker images..."
docker-compose pull

# Stop existing containers
echo "⏹️  Stopping existing containers..."
docker-compose down

# Build and start new containers
echo "🔨 Building and starting new containers..."
docker-compose up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T web python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional)
# docker-compose exec -T web python manage.py createsuperuser --noinput || true

# Show running containers
echo "✅ Deployment complete! Running containers:"
docker-compose ps

echo "🎉 Deployment successful!"
