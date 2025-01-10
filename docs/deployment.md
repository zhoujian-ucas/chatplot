# Deployment Guide

## Overview

This guide covers deploying ChatPlot in various environments, from development to production.

## Prerequisites

- Python 3.10+
- Node.js 20+
- Ollama
- PostgreSQL (for production)
- Nginx (for production)
- Docker (optional)

## Development Deployment

### Local Development

1. Set up environment:
```bash
# Create and activate Conda environment
conda env create -f environment.yml
conda activate chatplot

# Install frontend dependencies
cd frontend
npm install
cd ..
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start services:
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### Docker Development

1. Build and run with Docker Compose:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. Access services:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Production Deployment

### Server Requirements

- 2+ CPU cores
- 4GB+ RAM
- 20GB+ storage
- Ubuntu 20.04 LTS or similar

### System Setup

1. Update system:
```bash
sudo apt update
sudo apt upgrade -y
```

2. Install dependencies:
```bash
# System packages
sudo apt install -y python3-pip nodejs npm nginx postgresql

# Python packages
pip install -r requirements.txt

# Frontend packages
cd frontend
npm install --production
npm run build
cd ..
```

### Database Setup

1. Create PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE chatplot;
CREATE USER chatplot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE chatplot TO chatplot_user;
```

2. Configure database:
```bash
# Update .env
DATABASE_URL=postgresql://chatplot_user:your_password@localhost/chatplot

# Run migrations
alembic upgrade head
```

### Nginx Configuration

1. Create Nginx config:
```nginx
# /etc/nginx/sites-available/chatplot
server {
    listen 80;
    server_name your_domain.com;

    # Frontend
    location / {
        root /path/to/chatplot/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

2. Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/chatplot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL Configuration

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d your_domain.com
```

### Process Management

1. Create systemd service for backend:
```ini
# /etc/systemd/system/chatplot.service
[Unit]
Description=ChatPlot Backend
After=network.target

[Service]
User=chatplot
Group=chatplot
WorkingDirectory=/path/to/chatplot/backend
Environment="PATH=/path/to/conda/envs/chatplot/bin"
ExecStart=/path/to/conda/envs/chatplot/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Enable and start service:
```bash
sudo systemctl enable chatplot
sudo systemctl start chatplot
```

### Docker Production Deployment

1. Build production images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Deploy with Docker Compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring

### Application Monitoring

1. Set up logging:
```bash
# Configure logging
mkdir -p /var/log/chatplot
touch /var/log/chatplot/app.log
```

2. Monitor logs:
```bash
# View logs
tail -f /var/log/chatplot/app.log

# Monitor system resources
htop
```

### Health Checks

1. Configure monitoring:
```bash
# Set up health check endpoint
curl http://localhost:8000/health

# Run comprehensive health check
python utils/health_check.py
```

2. Set up alerts (optional):
```bash
# Configure monitoring service
# Set up email alerts
# Set up Slack notifications
```

## Backup and Recovery

### Database Backup

1. Automated backups:
```bash
# Create backup script
#!/bin/bash
pg_dump chatplot > /backup/chatplot_$(date +%Y%m%d).sql

# Schedule with cron
0 0 * * * /path/to/backup_script.sh
```

2. Manual backup:
```bash
pg_dump chatplot > backup.sql
```

### Application Backup

1. Back up application files:
```bash
tar -czf chatplot_backup.tar.gz /path/to/chatplot
```

2. Back up configuration:
```bash
cp .env .env.backup
cp nginx.conf nginx.conf.backup
```

## Security

### Firewall Configuration

```bash
# Allow necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
```

### Security Best Practices

1. Application security:
- Use secure environment variables
- Implement rate limiting
- Enable CORS protection
- Use secure sessions

2. Server security:
- Keep system updated
- Use strong passwords
- Configure firewall
- Enable SSL/TLS
- Regular security audits

## Troubleshooting

### Common Issues

1. Database connection issues:
```bash
# Check database status
sudo systemctl status postgresql

# Check connection
psql -U chatplot_user -d chatplot
```

2. Nginx issues:
```bash
# Check nginx status
sudo nginx -t
sudo systemctl status nginx

# Check logs
tail -f /var/log/nginx/error.log
```

3. Application issues:
```bash
# Check application logs
tail -f /var/log/chatplot/app.log

# Check system resources
htop
```

## Updates and Maintenance

### Updating Application

1. Pull updates:
```bash
git pull origin main
```

2. Update dependencies:
```bash
conda env update -f environment.yml
cd frontend && npm install && npm run build
```

3. Restart services:
```bash
sudo systemctl restart chatplot
sudo systemctl restart nginx
```

### Database Maintenance

1. Regular maintenance:
```bash
# Vacuum database
vacuumdb -d chatplot

# Analyze tables
analyze chatplot
```

2. Index maintenance:
```sql
REINDEX DATABASE chatplot;
``` 