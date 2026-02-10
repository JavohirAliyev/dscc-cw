#!/bin/bash
# SSL Certificate initialization script using Let's Encrypt

if [ -z "$1" ]; then
    echo "Usage: ./init_ssl.sh yourdomain.uz"
    exit 1
fi

DOMAIN=$1
EMAIL="admin@${DOMAIN}"  # Change this to your email

echo "🔐 Initializing SSL certificate for ${DOMAIN}..."

# Create directories
mkdir -p ./certbot/conf
mkdir -p ./certbot/www

# Get SSL certificate
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

echo "✅ SSL certificate obtained successfully!"
echo "🔄 Restarting nginx..."
docker-compose restart nginx

echo "🎉 SSL setup complete!"
