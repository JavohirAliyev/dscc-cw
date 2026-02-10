# 📚 Library Management System

A modern, fully containerized Django web application for managing library operations with complete CI/CD pipeline implementation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Overview

This Library Management System is a comprehensive web application built as part of a DevOps coursework project. It demonstrates modern software development practices including containerization, cloud deployment, and automated CI/CD pipelines.

### Key Features

✨ **User Management**
- User registration and authentication
- Login/logout functionality
- User profile management with customizable information
- Role-based access control

📚 **Book Management**
- Complete CRUD operations for books
- Advanced search and filtering capabilities
- Category-based organization
- ISBN tracking and validation
- Cover image uploads

👥 **Author Management**
- Author profiles with biographical information
- Books by author listing
- Nationality and birth date tracking

📖 **Borrowing System**
- Book borrowing and return functionality
- Due date tracking
- Borrowing history
- Availability status checking
- Overdue book notifications

🎨 **Modern UI/UX**
- Responsive Bootstrap 5 design
- Intuitive navigation
- Mobile-friendly interface
- Real-time status updates

## 🛠 Technologies Used

### Backend
- **Django 4.2** - Python web framework
- **PostgreSQL 15** - Relational database
- **Gunicorn** - WSGI HTTP server
- **Python 3.11** - Programming language

### Frontend
- **Bootstrap 5** - CSS framework
- **Bootstrap Icons** - Icon library
- **HTML5/CSS3** - Markup and styling

### DevOps & Infrastructure
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server and reverse proxy
- **GitHub Actions** - CI/CD automation
- **Let's Encrypt** - SSL/TLS certificates

### Testing & Quality
- **pytest-django** - Testing framework
- **Flake8** - Code linting
- **Coverage** - Code coverage reporting

## 📋 Database Schema

### Models and Relationships

**Author Model** (One-to-Many with Book)
- name, bio, birth_date, nationality
- Related books via `books` relationship

**Category Model** (Many-to-Many with Book)
- name, description
- Related books via `books` relationship

**Book Model**
- title, isbn, description, pages
- Foreign Key to Author (Many-to-One)
- Many-to-Many with Categories
- publication_date, available_copies, total_copies
- cover_image (optional)

**BorrowRecord Model** (Many-to-Many: User-Book)
- Foreign Key to User
- Foreign Key to Book
- borrow_date, due_date, return_date
- status (borrowed/returned/overdue)

**UserProfile Model** (One-to-One with User)
- phone_number, address, date_of_birth
- profile_picture (optional)

## 🚀 Local Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Docker and Docker Compose (for containerized setup)
- Git

### Method 1: Local Development (Without Docker)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL database**
```bash
# Create database and user
psql -U postgres
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Collect static files**
```bash
python manage.py collectstatic
```

9. **Run development server**
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

### Method 2: Docker Setup (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

2. **Create environment file**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Build and start containers**
```bash
# Development
docker-compose -f docker-compose.dev.yml up -d

# Production
docker-compose up -d --build
```

4. **Run migrations**
```bash
docker-compose exec web python manage.py migrate
```

5. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Collect static files**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

Access the application:
- Development: `http://localhost:8000`
- Production: `http://localhost` (via Nginx)

## 🌐 Deployment Instructions

### Prerequisites for Deployment

- Ubuntu 20.04+ server (Eskiz Cloud or any VPS)
- Domain name pointed to server IP
- SSH access to server
- Docker and Docker Compose installed on server

### Server Setup

1. **Update system and install Docker**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

2. **Configure firewall**
```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

3. **Clone repository on server**
```bash
cd /home/$USER
git clone https://github.com/yourusername/library-management.git
cd library-management
```

4. **Configure environment variables**
```bash
nano .env
# Set production values:
# - Strong SECRET_KEY
# - DEBUG=False
# - Production ALLOWED_HOSTS
# - Secure database credentials
```

5. **Setup SSL certificate**
```bash
chmod +x scripts/init_ssl.sh
./scripts/init_ssl.sh yourdomain.uz
```

6. **Update Nginx configuration**
```bash
# Edit nginx/conf.d/default.conf
# Replace 'localhost' with your domain name
nano nginx/conf.d/default.conf
```

7. **Deploy application**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

8. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

Your application should now be accessible at `https://yourdomain.uz`

## 🔄 CI/CD Pipeline

The project includes a complete GitHub Actions workflow for automated testing and deployment.

### Pipeline Stages

1. **Code Quality** - Flake8 linting
2. **Testing** - Pytest with PostgreSQL
3. **Build & Push** - Docker image to Docker Hub
4. **Deploy** - Automatic deployment to production server

### Required GitHub Secrets

Configure these secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

| Secret Name | Description |
|------------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SSH_PRIVATE_KEY` | Private SSH key for server access |
| `SSH_HOST` | Production server IP/domain |
| `SSH_USERNAME` | SSH username for server |

### Triggering Deployment

Deployment is automatically triggered on push to the `main` branch:

```bash
git add .
git commit -m "Update application"
git push origin main
```

The workflow will:
1. ✅ Run code quality checks
2. ✅ Execute all tests
3. ✅ Build Docker image
4. ✅ Push to Docker Hub
5. ✅ Deploy to production server
6. ✅ Run migrations
7. ✅ Restart services with zero downtime

## 📝 Environment Variables Documentation

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.uz

# Database Settings
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=strong_password
DB_HOST=db
DB_PORT=5432
```

**Important:** Never commit `.env` file to version control. Use `.env.example` as a template.

## 🧪 Running Tests

### Local Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=library

# Run specific test file
pytest library/tests.py

# Verbose output
pytest -v
```

### Docker Testing
```bash
docker-compose exec web pytest
docker-compose exec web pytest --cov=library
```

## 📸 Application Screenshots

### Home Page
![Home Page](docs/screenshots/home.png)

### Book List
![Book List](docs/screenshots/books.png)

### Book Detail
![Book Detail](docs/screenshots/book_detail.png)

### User Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Admin Panel
![Admin](docs/screenshots/admin.png)

## 🔐 Security Features

- HTTPS enforcement in production
- CSRF protection enabled
- XSS protection headers
- Secure cookie settings
- Non-root user in Docker containers
- Environment variable management
- SQL injection prevention (Django ORM)
- Password hashing (Django built-in)

## 📊 Project Statistics

- **Total Lines of Code**: ~2500+
- **Models**: 5 (Author, Category, Book, BorrowRecord, UserProfile)
- **Views**: 15+ functional views
- **Templates**: 10+ HTML templates
- **Tests**: 15+ test cases
- **API Endpoints**: 14+ URL patterns

## 🤝 Contributing

This is an academic project, but suggestions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- Student ID: Your ID
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django Documentation
- Docker Documentation
- Bootstrap Framework
- PostgreSQL Community
- GitHub Actions Documentation

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: your.email@example.com

## 🔗 Live Demo

- **Application**: https://yourdomain.uz
- **GitHub**: https://github.com/yourusername/library-management
- **Docker Hub**: https://hub.docker.com/r/yourusername/library-management

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Built with ❤️ for DevOps Coursework 2026**
