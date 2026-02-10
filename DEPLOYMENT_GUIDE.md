# 🚀 Deployment Guide - Library Management System

This guide provides detailed instructions for deploying the Library Management System to a production server.

## 📋 Prerequisites

- Ubuntu 20.04+ server (Eskiz Cloud recommended)
- Domain name (e.g., yourdomain.uz)
- SSH access to server
- Minimum 2GB RAM, 20GB storage
- Root or sudo access

## 🔧 Server Preparation

### Step 1: Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common git

# Set timezone (optional)
sudo timedatectl set-timezone Asia/Tashkent
```

### Step 2: Install Docker

```bash
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again for group changes to take effect
```

### Step 3: Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 4: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw --force enable

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow OpenSSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check firewall status
sudo ufw status
```

## 🌐 Domain Configuration

### Configure DNS Records

Add the following DNS records for your domain:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_SERVER_IP | 3600 |
| A | www | YOUR_SERVER_IP | 3600 |

Wait for DNS propagation (can take 5-60 minutes).

Verify with:
```bash
nslookup yourdomain.uz
ping yourdomain.uz
```

## 📦 Application Deployment

### Step 1: Clone Repository

```bash
cd /home/$USER
git clone https://github.com/yourusername/library-management.git
cd library-management
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
```

**Required .env configurations for production:**

```env
SECRET_KEY=GENERATE_A_STRONG_SECRET_KEY_HERE
DEBUG=False
ALLOWED_HOSTS=yourdomain.uz,www.yourdomain.uz

DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=STRONG_DATABASE_PASSWORD
DB_HOST=db
DB_PORT=5432
```

**Generate a strong SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 3: Update Nginx Configuration

```bash
# Edit Nginx config
nano nginx/conf.d/default.conf

# Replace 'localhost' with your domain name in:
# - server_name directives
# - SSL certificate paths
```

Example:
```nginx
server_name yourdomain.uz www.yourdomain.uz;
ssl_certificate /etc/letsencrypt/live/yourdomain.uz/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.uz/privkey.pem;
```

### Step 4: Initial Deployment

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run initial setup
./scripts/setup.sh
```

This will:
- Create necessary directories
- Build Docker images
- Start all services
- Run database migrations
- Collect static files
- Prompt for superuser creation

### Step 5: SSL Certificate Setup

```bash
# Obtain SSL certificate
./scripts/init_ssl.sh yourdomain.uz

# This will:
# - Request certificate from Let's Encrypt
# - Configure automatic renewal
# - Restart Nginx with SSL enabled
```

## ✅ Verification

### Check Services Status

```bash
# View running containers
docker-compose ps

# All services should show "Up" status
```

### Test Application

1. **HTTP Access** (should redirect to HTTPS):
   ```bash
   curl -I http://yourdomain.uz
   ```

2. **HTTPS Access**:
   ```bash
   curl -I https://yourdomain.uz
   ```

3. **Browser Test**:
   - Navigate to `https://yourdomain.uz`
   - Should see library homepage with valid SSL certificate

### Check Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs nginx
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f
```

## 🔄 CI/CD Setup

### Step 1: Generate SSH Key for GitHub Actions

```bash
# On your server
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys

# Display private key (to add to GitHub Secrets)
cat ~/.ssh/github_actions
```

### Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SSH_PRIVATE_KEY` | Content of ~/.ssh/github_actions |
| `SSH_HOST` | Your server IP or domain |
| `SSH_USERNAME` | Your SSH username |

### Step 3: Test CI/CD Pipeline

```bash
# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add README.md
git commit -m "Test CI/CD pipeline"
git push origin main

# Watch GitHub Actions workflow execute
# Go to: GitHub Repository → Actions tab
```

## 🔐 Security Hardening

### 1. Secure SSH Access

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Recommended settings:
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes

# Restart SSH
sudo systemctl restart sshd
```

### 2. Setup Fail2Ban

```bash
# Install Fail2Ban
sudo apt install -y fail2ban

# Start and enable
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### 3. Regular Updates

```bash
# Create update script
cat > ~/update_system.sh << 'EOF'
#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
docker system prune -af
EOF

chmod +x ~/update_system.sh
```

### 4. Backup Setup

```bash
# Add to crontab for automatic backups
crontab -e

# Add this line (daily backup at 2 AM):
0 2 * * * cd /home/$USER/library-management && ./scripts/backup.sh
```

## 📊 Monitoring

### View Application Metrics

```bash
# Container stats
docker stats

# Disk usage
df -h

# Memory usage
free -h

# Docker disk usage
docker system df
```

### Setup Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/docker-containers

# Add:
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=10M
    missingok
    delaycompress
    copytruncate
}
```

## 🔧 Maintenance Commands

### Update Application

```bash
cd /home/$USER/library-management
git pull origin main
docker-compose pull
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### Restart Services

```bash
docker-compose restart        # Restart all
docker-compose restart web    # Restart Django only
docker-compose restart nginx  # Restart Nginx only
```

### View Real-time Logs

```bash
docker-compose logs -f --tail=100
```

### Database Backup

```bash
# Manual backup
./scripts/backup.sh

# Restore from backup
./scripts/restore.sh TIMESTAMP
```

### Clean Up

```bash
# Remove unused Docker resources
docker system prune -a

# Remove old images
docker image prune -a
```

## 🆘 Troubleshooting

### Application Not Accessible

1. Check if containers are running:
   ```bash
   docker-compose ps
   ```

2. Check Nginx logs:
   ```bash
   docker-compose logs nginx
   ```

3. Check Django logs:
   ```bash
   docker-compose logs web
   ```

4. Verify firewall:
   ```bash
   sudo ufw status
   ```

### SSL Certificate Issues

```bash
# Check certificate expiry
docker-compose exec certbot certbot certificates

# Renew certificate manually
docker-compose exec certbot certbot renew

# Check Nginx configuration
docker-compose exec nginx nginx -t
```

### Database Connection Issues

```bash
# Check database status
docker-compose exec db pg_isready -U library_user

# Access database
docker-compose exec db psql -U library_user -d library_db
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a --volumes

# Clean old backups
rm -rf backups/backup_*
```

## 📞 Support

If you encounter issues:

1. Check logs: `docker-compose logs`
2. Review this guide
3. Check GitHub Issues
4. Contact: your.email@example.com

## 🎉 Deployment Complete!

Your Library Management System should now be:
- ✅ Accessible via HTTPS
- ✅ Running in production mode
- ✅ Automatically deploying via CI/CD
- ✅ Secured with SSL certificate
- ✅ Protected by firewall
- ✅ Backed up automatically

Next steps:
1. Add sample books and authors
2. Configure email settings (optional)
3. Setup monitoring (optional)
4. Invite users to test the system

---

**Last Updated**: February 2026
