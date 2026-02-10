#!/bin/bash
# Initial setup script for Library Management System

set -e

echo "🚀 Library Management System - Initial Setup"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your settings before proceeding"
    echo "   Important: Change SECRET_KEY, DB_PASSWORD, and ALLOWED_HOSTS"
    read -p "Press enter to continue after editing .env file..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p certbot/conf certbot/www
mkdir -p media staticfiles
mkdir -p logs

# Build Docker images
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for database
echo "⏳ Waiting for database to be ready..."
sleep 15

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T web python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

# Create superuser
echo ""
echo "👤 Create a superuser account:"
docker-compose exec web python manage.py createsuperuser

# Load sample data (optional)
read -p "Do you want to load sample data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Loading sample data..."
    docker-compose exec web python manage.py loaddata sample_data.json || echo "Sample data file not found, skipping..."
fi

# Show status
echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Application URLs:"
echo "   - Main site: http://localhost (via Nginx)"
echo "   - Direct Django: http://localhost:8000"
echo "   - Admin panel: http://localhost/admin"
echo ""
echo "📊 Check service status:"
docker-compose ps

echo ""
echo "🎉 Library Management System is ready!"
echo ""
echo "📝 Next steps:"
echo "   1. Access the application at http://localhost"
echo "   2. Log in with your superuser account"
echo "   3. Start adding books, authors, and categories!"
echo ""
echo "🛑 To stop services: docker-compose down"
echo "🔄 To restart services: docker-compose restart"
echo "📋 To view logs: docker-compose logs -f"
