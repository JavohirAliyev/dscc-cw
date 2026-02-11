# Library Management System

Django web application for managing library books, authors, and borrowing records.

## Features

- User authentication and profiles
- Book CRUD operations with search/filter
- Author and category management
- Book borrowing and return system
- Responsive Bootstrap UI

## Tech Stack

- Django 4.2, PostgreSQL 15
- Docker, Nginx, Gunicorn
- GitHub Actions CI/CD

## Quick Start

```bash
# Docker (recommended)
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Local
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Testing

```bash
pytest
pytest --cov=library
```

## Database Schema

- Author (1:N) → Books
- Category (M:N) ↔ Books
- Book → has Author and Categories
- BorrowRecord → links Users and Books
- UserProfile (1:1) → User

## Performance Optimizations

- Connection pooling (10+10 overflow)
- Query optimization (select_related/prefetch_related)
- Database indexes
- Gevent async workers
- Nginx proxy buffering

## License

MIT
