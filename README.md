# 📚 Library Management System

## 🎯 Project Overview

This Library Management System is a comprehensive web application built as part of a DSCC coursework project. It demonstrates modern software development practices including containerization, cloud deployment, and automated CI/CD pipelines.

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
git clone https://github.com/JavohirAliyev/library-management.git
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
CREATE USER library_user WITH PASSWORD;
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q
```

5. **Configure environment variables**
```bash
cp .env.example .env
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
git clone https://github.com/JavohirAliyev/library-management.git
cd library-management
```

2. **Create environment file**
```bash
cp .env.example .env
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

### **Recommended: Azure Container Apps** (Serverless)

Deploy to Azure Container Apps for a modern, serverless experience with automatic scaling.

**📖 Complete Guide:** [AZURE_DEPLOYMENT_GUIDE.md](AZURE_DEPLOYMENT_GUIDE.md)

**Quick Steps:**
1. Create Azure account (free trial available)
2. Set up Azure Container Apps + PostgreSQL database
3. Configure GitHub secrets
4. Push to main branch → Automatic deployment! 🚀

**Required GitHub Secrets:**
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- `AZURE_CREDENTIALS` (service principal JSON)
- `AZURE_RESOURCE_GROUP`
- `AZURE_CONTAINER_APP_NAME`

---

### **Alternative: Traditional Server Deployment**

For VPS/VM deployment with SSH access:

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
git clone https://github.com/JavohirAliyev/library-management.git
cd library-management
```

4. **Configure environment variables**
```bash
nano .env
```

5. **Setup SSL certificate**
```bash
chmod +x scripts/init_ssl.sh
./scripts/init_ssl.sh (Azure domain name)
```

6. **Update Nginx configuration**
```bash
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

## 🔄 CI/CD Pipeline

The project includes a complete GitHub Actions workflow for automated testing and building Docker images.

### Pipeline Stages

Every push to `main` triggers:

1. **Code Quality Checks** - Flake8 linting for syntax and style
2. **Automated Tests** - Pytest with PostgreSQL test database
3. **Build Docker Image** - Containerize application
4. **Push to Docker Hub** - Publish with `latest` tag

**Azure Container Apps automatically pulls the latest image from Docker Hub.**

### Required GitHub Secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret Name | Description | How to Get It |
|-------------|-------------|---------------|
| `LIBRARYMANAGEMENT_REGISTRY_USERNAME` | Docker Hub username | Your Docker Hub account |
| `LIBRARYMANAGEMENT_REGISTRY_PASSWORD` | Docker Hub password/token | Docker Hub → Security → New Access Token |

✅ **These secrets are already configured** by Azure Portal auto-deploy setup.

### How It Works

```bash
# Push your code
git add .
git commit -m "Add new feature"
git push origin main

# Pipeline runs automatically:
# 1. ✅ Code quality checks
# 2. ✅ Tests with PostgreSQL
# 3. ✅ Build Docker image
# 4. ✅ Push to Docker Hub (latest tag)
# 5. 🔄 Azure automatically pulls and deploys new image
```

**Total Time:** ~3-5 minutes from push to Docker Hub. Azure pulls the image automatically.

## 🧪 Running Tests

### Local Testing
```bash
pytest

pytest --cov=library

pytest library/tests.py

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

## 🔗 Live Demo

- **Application**: https://
- **Docker Hub**: https://hub.docker.com/r/javohiraliyev/library-management
#   T e s t i n g   C I / C D   d e p l o y m e n t 
 
 