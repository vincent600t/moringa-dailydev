# Deployment Guide - Moringa Daily.dev Backend

This guide covers different deployment options for the Moringa Daily.dev backend API.

## Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Configuration](#environment-configuration)
- [Deployment Options](#deployment-options)
  - [Docker Deployment](#docker-deployment)
  - [Heroku Deployment](#heroku-deployment)
  - [AWS EC2 Deployment](#aws-ec2-deployment)
  - [DigitalOcean Deployment](#digitalocean-deployment)
- [Post-Deployment](#post-deployment)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying to production:

- [ ] All tests pass (`pytest`)
- [ ] Code is linted (`flake8`, `black`)
- [ ] Security vulnerabilities checked
- [ ] Environment variables configured
- [ ] Database backup strategy in place
- [ ] SSL/TLS certificates ready
- [ ] Domain name configured
- [ ] Monitoring tools setup
- [ ] Logging configured
- [ ] CI/CD pipeline tested
- [ ] Documentation updated

---

## Environment Configuration

### Production Environment Variables

Create a `.env.production` file:

```bash
# Application
FLASK_ENV=production
SECRET_KEY=<strong-secret-key>
JWT_SECRET_KEY=<strong-jwt-secret>

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# CORS (Frontend URL)
CORS_ORIGINS=https://yourfrontend.com

# File Upload
MAX_CONTENT_LENGTH=104857600  # 100MB
UPLOAD_FOLDER=/var/www/uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/moringa-dailydev/app.log
```

### Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Deployment Options

### 1. Docker Deployment

#### Using Docker Compose (Recommended for Production)

**Step 1: Prepare Environment**

```bash
# Create production environment file
cp .env.example .env.production
# Edit .env.production with production values
```

**Step 2: Build and Run**

```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
```

**Step 3: Initialize Database**

```bash
# Run migrations
docker-compose exec app flask db upgrade

# Create admin user (optional)
docker-compose exec app python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@example.com', password='SecurePass123!', role='admin')
    db.session.add(admin)
    db.session.commit()
    print('Admin created!')
"
```

**Step 4: Verify Deployment**

```bash
# Test health endpoint
curl http://localhost/health

# Check logs
docker-compose logs app
```

#### Using Docker Standalone

```bash
# Build image
docker build -t moringa-dailydev:latest .

# Run container
docker run -d \
  --name moringa-app \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-key \
  moringa-dailydev:latest

# Check logs
docker logs -f moringa-app
```

---

### 2. Heroku Deployment

**Step 1: Install Heroku CLI**

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh
```

**Step 2: Login and Create App**

```bash
heroku login
heroku create moringa-dailydev-api
```

**Step 3: Add PostgreSQL**

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

**Step 4: Set Environment Variables**

```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

**Step 5: Create Procfile**

```bash
# Create Procfile in project root
echo "web: gunicorn 'app:create_app()' --bind 0.0.0.0:$PORT" > Procfile
```

**Step 6: Deploy**

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Run migrations
heroku run flask db upgrade

# Create admin user
heroku run python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); admin = User(username='admin', email='admin@example.com', password='Admin123!', role='admin'); db.session.add(admin); db.session.commit()"
```

**Step 7: Open App**

```bash
heroku open
heroku logs --tail
```

---

### 3. AWS EC2 Deployment

**Step 1: Launch EC2 Instance**

1. Choose Ubuntu 22.04 LTS
2. Instance type: t2.small or larger
3. Configure security group:
   - SSH (22) from your IP
   - HTTP (80) from anywhere
   - HTTPS (443) from anywhere

**Step 2: Connect to Instance**

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**Step 3: Setup Server**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx

# Install certbot for SSL
sudo apt install -y certbot python3-certbot-nginx
```

**Step 4: Setup PostgreSQL**

```bash
sudo -u postgres psql

CREATE DATABASE moringa_dailydev;
CREATE USER moringa_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE moringa_dailydev TO moringa_user;
\q
```

**Step 5: Deploy Application**

```bash
# Create application directory
sudo mkdir -p /var/www/moringa-dailydev
sudo chown ubuntu:ubuntu /var/www/moringa-dailydev
cd /var/www/moringa-dailydev

# Clone repository
git clone https://github.com/yourusername/moringa-dailydev.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Setup environment
cp .env.example .env
nano .env  # Edit with production values

# Run migrations
flask db upgrade
```

**Step 6: Create Systemd Service**

```bash
sudo nano /etc/systemd/system/moringa-dailydev.service
```

```ini
[Unit]
Description=Moringa Daily.dev API
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/moringa-dailydev
Environment="PATH=/var/www/moringa-dailydev/venv/bin"
ExecStart=/var/www/moringa-dailydev/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 'app:create_app()'
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable moringa-dailydev
sudo systemctl start moringa-dailydev
sudo systemctl status moringa-dailydev
```

**Step 7: Configure Nginx**

```bash
sudo nano /etc/nginx/sites-available/moringa-dailydev
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        alias /var/www/moringa-dailydev/uploads/;
        expires 30d;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/moringa-dailydev /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 8: Setup SSL with Let's Encrypt**

```bash
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

---

### 4. DigitalOcean Deployment

**Using DigitalOcean App Platform:**

**Step 1: Create App**

1. Go to DigitalOcean App Platform
2. Connect your GitHub repository
3. Select branch: `main`

**Step 2: Configure Build Settings**

```yaml
name: moringa-dailydev
services:
- name: api
  github:
    repo: yourusername/moringa-dailydev
    branch: main
  build_command: pip install -r requirements.txt
  run_command: gunicorn -w 4 'app:create_app()'
  environment_slug: python
  http_port: 5000
  
databases:
- name: postgres
  engine: PG
  version: "15"
```

**Step 3: Set Environment Variables**

Add in App Platform dashboard:
- `FLASK_ENV=production`
- `SECRET_KEY=...`
- `JWT_SECRET_KEY=...`

**Step 4: Deploy**

Click "Deploy" and wait for build to complete.

---

## Post-Deployment

### 1. Database Migration

```bash
# Run migrations
flask db upgrade

# Seed initial data (if needed)
python seed_data.py
```

### 2. Create Admin User

```bash
# Using Flask shell
flask shell

>>> from app.models import User
>>> from app import db
>>> admin = User(username='admin', email='admin@yourdomain.com', password='SecurePass123!', role='admin')
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

### 3. Test Endpoints

```bash
# Health check
curl https://your-domain.com/health

# API info
curl https://your-domain.com/api

# Register test user
curl -X POST https://your-domain.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Test@123"}'
```

### 4. Setup Monitoring

#### Using Uptime Robot

1. Go to uptimerobot.com
2. Add new monitor
3. Type: HTTPS
4. URL: `https://your-domain.com/health`
5. Interval: 5 minutes

#### Using New Relic

```bash
pip install newrelic
newrelic-admin generate-config YOUR-LICENSE-KEY newrelic.ini
```

---

## Monitoring and Maintenance

### Log Management

```bash
# View logs (systemd)
sudo journalctl -u moringa-dailydev -f

# View logs (Docker)
docker-compose logs -f app

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Backups

```bash
# Manual backup
pg_dump -U moringa_user moringa_dailydev > backup_$(date +%Y%m%d).sql

# Automated backup (crontab)
0 2 * * * pg_dump -U moringa_user moringa_dailydev > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Performance Monitoring

```bash
# Check server resources
htop

# Check database performance
sudo -u postgres psql moringa_dailydev
\timing on
SELECT * FROM users LIMIT 10;

# Monitor application
gunicorn --access-logfile - --error-logfile - 'app:create_app()'
```

### SSL Certificate Renewal

```bash
# Certbot auto-renewal (should work automatically)
sudo certbot renew --dry-run

# Manual renewal
sudo certbot renew
sudo systemctl reload nginx
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u moringa-dailydev -n 50

# Check if port is in use
sudo lsof -i :5000

# Test application manually
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 'app:create_app()'
```

### Database Connection Issues

```bash
# Test database connection
psql -U moringa_user -d moringa_dailydev -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### 502 Bad Gateway

```bash
# Check nginx configuration
sudo nginx -t

# Check if application is running
sudo systemctl status moringa-dailydev

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### High Memory Usage

```bash
# Check memory
free -h

# Reduce gunicorn workers
# Edit systemd service file
ExecStart=.../gunicorn -w 2 ...  # Reduce from 4 to 2

sudo systemctl daemon-reload
sudo systemctl restart moringa-dailydev
```

### Slow API Responses

```bash
# Check database query performance
sudo -u postgres psql moringa_dailydev
EXPLAIN ANALYZE SELECT * FROM content WHERE status='approved';

# Add database indexes if needed
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_category ON content(category_id);
```

---

## Security Best Practices

1. **Keep secrets secret**: Never commit `.env` files
2. **Use HTTPS**: Always use SSL certificates
3. **Update dependencies**: Regularly update packages
4. **Firewall**: Configure UFW or security groups
5. **Rate limiting**: Implement in nginx or app level
6. **Backups**: Regular automated backups
7. **Monitoring**: Setup alerts for downtime
8. **Access control**: Limit SSH access
9. **Database**: Use strong passwords, limit connections
10. **Logging**: Monitor for suspicious activity

---

## Scaling Strategies

### Horizontal Scaling

```bash
# Add more application servers
# Use load balancer (nginx, AWS ALB, etc.)

upstream flask_app {
    server app1:5000;
    server app2:5000;
    server app3:5000;
}
```

### Database Scaling

```bash
# Read replicas for queries
# Connection pooling
# Caching layer (Redis)
```

### CDN for Static Files

Use CloudFlare, AWS CloudFront, or similar for:
- Uploaded images
- Static assets
- API caching

---

## Rollback Procedure

If deployment fails:

```bash
# Git rollback
git revert HEAD
git push

# Docker rollback
docker-compose down
docker-compose up -d --build

# Database rollback
flask db downgrade

# Systemd service
sudo systemctl stop moringa-dailydev
# Fix issues
sudo systemctl start moringa-dailydev
```

---

## Support

For deployment issues:
- Check logs first
- Review this guide
- Open GitHub issue
- Contact DevOps team

---

**Happy Deploying! 🚀**