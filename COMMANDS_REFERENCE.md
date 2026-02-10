# 🔧 Commands Reference Guide

Quick reference for all commonly used commands in this project.

---

## 📦 Docker Commands

### Building and Starting

```bash
# Build images
docker-compose build

# Start all services (detached)
docker-compose up -d

# Start with build
docker-compose up -d --build

# Start specific service
docker-compose up -d web

# Development mode
docker-compose -f docker-compose.dev.yml up -d
```

### Stopping and Removing

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop web

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# View specific service logs
docker-compose logs web
docker-compose logs nginx
docker-compose logs db

# Last 100 lines
docker-compose logs --tail=100 -f
```

### Container Management

```bash
# List running containers
docker-compose ps

# Execute command in container
docker-compose exec web python manage.py shell

# Access container shell
docker-compose exec web bash
docker-compose exec db psql -U library_user -d library_db

# View container stats
docker stats
```

### Image Management

```bash
# List images
docker images

# Remove unused images
docker image prune -a

# Check image size
docker images | grep library

# Pull latest images
docker-compose pull
```

---

## 🐍 Django Management Commands

### Database

```bash
# Make migrations
docker-compose exec web python manage.py makemigrations

# Run migrations
docker-compose exec web python manage.py migrate

# Show migrations
docker-compose exec web python manage.py showmigrations

# Reset database (careful!)
docker-compose exec web python manage.py flush
```

### User Management

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Change user password
docker-compose exec web python manage.py changepassword username
```

### Static Files

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic

# Collect static files (no input)
docker-compose exec web python manage.py collectstatic --noinput

# Clear static files
docker-compose exec web python manage.py collectstatic --clear --noinput
```

### Django Shell

```bash
# Open Django shell
docker-compose exec web python manage.py shell

# Example: Create sample data
docker-compose exec web python manage.py shell
>>> from library.models import Author, Book, Category
>>> author = Author.objects.create(name="Test Author")
>>> category = Category.objects.create(name="Fiction")
>>> book = Book.objects.create(title="Test Book", author=author, isbn="1234567890123", publication_date="2024-01-01", pages=200)
>>> book.categories.add(category)
```

### Development Server

```bash
# Run development server (inside container)
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Testing Commands

### Running Tests

```bash
# Run all tests
docker-compose exec web pytest

# Run with verbose output
docker-compose exec web pytest -v

# Run specific test file
docker-compose exec web pytest library/tests.py

# Run specific test class
docker-compose exec web pytest library/tests.py::TestModels

# Run specific test method
docker-compose exec web pytest library/tests.py::TestModels::test_author_creation

# Run with coverage
docker-compose exec web pytest --cov=library

# Generate HTML coverage report
docker-compose exec web pytest --cov=library --cov-report=html
```

### Code Quality

```bash
# Run Flake8 linting
docker-compose exec web flake8 .

# Run Flake8 on specific file
docker-compose exec web flake8 library/views.py

# Check specific error codes
docker-compose exec web flake8 --select=E9,F63,F7,F82
```

---

## 🗄️ Database Commands

### PostgreSQL Access

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U library_user -d library_db

# Common PostgreSQL commands (inside psql):
\dt                 # List tables
\d table_name       # Describe table
\l                  # List databases
\du                 # List users
\q                  # Quit
```

### Database Backup

```bash
# Backup database
docker-compose exec -T db pg_dump -U library_user library_db > backup.sql

# Using backup script
./scripts/backup.sh

# Restore database
docker-compose exec -T db psql -U library_user library_db < backup.sql

# Using restore script
./scripts/restore.sh TIMESTAMP
```

### Database Queries

```bash
# Count records
docker-compose exec db psql -U library_user -d library_db -c "SELECT COUNT(*) FROM library_book;"

# View recent books
docker-compose exec db psql -U library_user -d library_db -c "SELECT title, author_id FROM library_book LIMIT 5;"
```

---

## 🚀 Deployment Commands

### Initial Deployment

```bash
# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or manual steps:
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

### Update Deployment

```bash
# Run deploy script
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# Or manual steps:
git pull origin main
docker-compose pull
docker-compose down
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### SSL Certificate

```bash
# Initial SSL setup
chmod +x scripts/init_ssl.sh
./scripts/init_ssl.sh yourdomain.uz

# Renew certificate
docker-compose exec certbot certbot renew

# Check certificate
docker-compose exec certbot certbot certificates
```

---

## 🔐 Server Commands

### Firewall (UFW)

```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow OpenSSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status

# Disable firewall (not recommended)
sudo ufw disable
```

### System Updates

```bash
# Update packages
sudo apt update
sudo apt upgrade -y

# Clean up
sudo apt autoremove -y
sudo apt autoclean
```

### Service Management

```bash
# Check Docker status
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Enable Docker on boot
sudo systemctl enable docker
```

---

## 🐙 Git Commands

### Basic Operations

```bash
# Initialize repository
git init

# Add files
git add .
git add filename

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# Check status
git status

# View commit history
git log
git log --oneline
```

### Branch Management

```bash
# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main

# List branches
git branch

# Merge branch
git checkout main
git merge feature-name

# Delete branch
git branch -d feature-name
```

### Remote Repository

```bash
# Add remote
git remote add origin https://github.com/username/repo.git

# View remotes
git remote -v

# Change remote URL
git remote set-url origin https://github.com/username/new-repo.git
```

---

## 🐳 Docker Hub Commands

### Login and Push

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag library-management:latest username/library-management:latest

# Push image
docker push username/library-management:latest

# Pull image
docker pull username/library-management:latest
```

---

## 🔍 Debugging Commands

### View Container Details

```bash
# Inspect container
docker inspect library_django

# View container processes
docker top library_django

# View container resource usage
docker stats library_django
```

### Network Debugging

```bash
# List networks
docker network ls

# Inspect network
docker network inspect library_network

# Test connectivity
docker-compose exec web ping db
docker-compose exec web curl http://nginx
```

### File System

```bash
# Copy file from container
docker cp library_django:/app/logs/error.log ./error.log

# Copy file to container
docker cp local-file.txt library_django:/app/

# View container file system
docker-compose exec web ls -la /app
```

---

## 📊 Monitoring Commands

### System Resources

```bash
# Disk usage
df -h

# Docker disk usage
docker system df

# Memory usage
free -h

# CPU usage
top
htop
```

### Application Logs

```bash
# Nginx access logs
docker-compose exec nginx tail -f /var/log/nginx/access.log

# Nginx error logs
docker-compose exec nginx tail -f /var/log/nginx/error.log

# Django logs (if configured)
docker-compose exec web tail -f logs/django.log
```

---

## 🧹 Cleanup Commands

### Docker Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Clean everything (careful!)
docker system prune -a --volumes
```

### Application Cleanup

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove static files
rm -rf staticfiles/*

# Remove media files (careful!)
rm -rf media/*
```

---

## 🔄 CI/CD Commands

### GitHub Actions

```bash
# Trigger workflow manually (if configured)
gh workflow run deploy.yml

# View workflow runs
gh run list

# View specific run
gh run view RUN_ID

# Download artifacts
gh run download RUN_ID
```

### Local CI/CD Testing

```bash
# Run linting locally
flake8 .

# Run tests locally
pytest

# Build Docker image locally
docker build -t test-image .

# Test deployment script
./scripts/deploy.sh
```

---

## 📝 Quick Troubleshooting

### Container won't start
```bash
docker-compose down -v
docker-compose up -d --build
docker-compose logs
```

### Database connection issues
```bash
docker-compose exec db pg_isready -U library_user
docker-compose restart db
docker-compose logs db
```

### Static files not loading
```bash
docker-compose exec web python manage.py collectstatic --clear --noinput
docker-compose restart nginx
```

### Permission issues
```bash
sudo chown -R $USER:$USER .
chmod +x scripts/*.sh
```

### Port already in use
```bash
# Find process using port
sudo lsof -i :8000
sudo lsof -i :80

# Kill process
sudo kill -9 PID
```

---

## 🎯 Most Used Commands

For quick reference, here are the most commonly used commands:

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web pytest

# Stop everything
docker-compose down

# Deploy updates
./scripts/deploy.sh

# Backup database
./scripts/backup.sh
```

---

## 💡 Pro Tips

1. **Alias common commands** (add to ~/.bashrc or ~/.zshrc):
```bash
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dce='docker-compose exec'
alias dcr='docker-compose restart'
```

2. **Use docker-compose exec -T** for non-interactive commands in scripts

3. **Always check logs** when something doesn't work: `docker-compose logs`

4. **Use health checks** to ensure services are ready before connecting

5. **Backup before major changes**: `./scripts/backup.sh`

---

**Need more help?** Check the documentation files:
- README.md - Full documentation
- DEPLOYMENT_GUIDE.md - Deployment instructions
- PROJECT_SUMMARY.md - Project overview
- QUICKSTART.md - Quick start guide

---

**Last Updated**: February 2026
