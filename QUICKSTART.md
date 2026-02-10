# ⚡ Quick Start Guide

Get the Library Management System running in 5 minutes!

## Prerequisites
- Docker and Docker Compose installed
- Git installed

## 🚀 Quick Start (Docker)

```bash
# 1. Clone repository
git clone <your-repo-url>
cd library-management

# 2. Create environment file
cp .env.example .env
# Edit .env if needed (default values work for local testing)

# 3. Start all services
docker-compose -f docker-compose.dev.yml up -d

# 4. Run migrations
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# 5. Create superuser
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# 6. Access application
# Open browser: http://localhost:8000
```

## 🔧 Development Commands

```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down

# Restart services
docker-compose -f docker-compose.dev.yml restart

# Run tests
docker-compose -f docker-compose.dev.yml exec web pytest

# Access Django shell
docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Create new app
docker-compose -f docker-compose.dev.yml exec web python manage.py startapp myapp
```

## 📝 Adding Sample Data

```bash
# Access Django shell
docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Then run:
from library.models import Author, Category, Book
from datetime import date

# Create author
author = Author.objects.create(
    name="J.K. Rowling",
    bio="British author, best known for the Harry Potter series",
    nationality="British"
)

# Create category
category = Category.objects.create(
    name="Fantasy",
    description="Fantasy fiction books"
)

# Create book
book = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    author=author,
    isbn="9780747532699",
    description="First book in the Harry Potter series",
    publication_date=date(1997, 6, 26),
    pages=223,
    available_copies=5,
    total_copies=5
)
book.categories.add(category)
```

## 🌐 Production Deployment

For production deployment, see:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [README.md](README.md) - Full documentation

## 🆘 Troubleshooting

**Container won't start?**
```bash
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d --build
```

**Database issues?**
```bash
docker-compose -f docker-compose.dev.yml exec db psql -U library_user -d library_db
```

**Permission issues?**
```bash
sudo chown -R $USER:$USER .
```

## 📚 Next Steps

1. ✅ Application is running
2. 📖 Read the [README.md](README.md) for full documentation
3. 🚀 Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production
4. 🎥 Check [VIDEO_GUIDE.md](VIDEO_GUIDE.md) for demo recording
5. 📝 Use [TECHNICAL_REPORT_TEMPLATE.md](TECHNICAL_REPORT_TEMPLATE.md) for report

Enjoy your Library Management System! 📚
