# LexShield AI - Deployment Guide

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [AWS Deployment](#aws-deployment)
5. [SSL/TLS Configuration](#ssltls-configuration)
6. [Database Migration](#database-migration)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)

---

## Pre-Deployment Checklist

### Security
- [ ] Change all default passwords and secrets
- [ ] Generate strong SECRET_KEY and ENCRYPTION_KEY
- [ ] Configure SSL/TLS certificates
- [ ] Enable HTTPS only
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Enable CSRF protection
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable security headers
- [ ] Configure CSP headers

### Infrastructure
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Set up log aggregation
- [ ] Configure load balancer
- [ ] Set up CDN for static assets
- [ ] Configure DNS
- [ ] Set up health checks
- [ ] Configure auto-scaling policies

### Application
- [ ] Update API documentation
- [ ] Configure API rate limits
- [ ] Set up error tracking (Sentry)
- [ ] Configure analytics
- [ ] Test all API endpoints
- [ ] Verify database migrations
- [ ] Test file upload functionality
- [ ] Test voice processing
- [ ] Verify email notifications

### Compliance
- [ ] Review data retention policies
- [ ] Ensure GDPR compliance
- [ ] Document security measures
- [ ] Set up audit logging
- [ ] Configure data encryption
- [ ] Test disaster recovery

---

## Local Development Setup

### Prerequisites
```bash
# System requirements
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
```

### Clone and Setup
```bash
# Clone repository
git clone <repository-url>
cd lexshield-ai

# Create environment file
cp .env.example .env

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload

# Frontend setup (in new terminal)
cd frontend
npm install
npm run dev
```

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Docker Deployment

### Build Images
```bash
# Build all services
docker-compose build

# Or build specific service
docker-compose build backend
docker-compose build frontend
```

### Start Services
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (careful!)
docker-compose down -v
```

### Production Deployment
```bash
# Export environment variables
export ENVIRONMENT=production
export DEBUG=false
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Start services with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Check health
docker-compose ps
docker-compose exec backend curl http://localhost:8000/health
```

---

## AWS Deployment

### Using ECS (Elastic Container Service)

#### 1. Create ECR Repositories
```bash
# Create repositories for backend and frontend
aws ecr create-repository --repository-name lexshield-api --region us-east-1
aws ecr create-repository --repository-name lexshield-web --region us-east-1
```

#### 2. Build and Push Images
```bash
# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t lexshield-api:latest backend/
docker tag lexshield-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/lexshield-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/lexshield-api:latest

# Build and push frontend
docker build -t lexshield-web:latest frontend/
docker tag lexshield-web:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/lexshield-web:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/lexshield-web:latest
```

#### 3. Create RDS Instance
```bash
aws rds create-db-instance \
  --db-instance-identifier lexshield-db \
  --db-instance-class db.t4g.micro \
  --engine postgres \
  --master-username admin \
  --allocated-storage 100 \
  --storage-encrypted \
  --enable-cloudwatch-logs-exports postgresql
```

#### 4. Create ECS Cluster
```bash
# Create cluster
aws ecs create-cluster --cluster-name lexshield-prod

# Create task definitions from JSON files
aws ecs register-task-definition --cli-input-json file://backend-task-def.json
aws ecs register-task-definition --cli-input-json file://frontend-task-def.json

# Create services
aws ecs create-service --cluster lexshield-prod \
  --service-name lexshield-api \
  --task-definition lexshield-api:1 \
  --desired-count 2 \
  --load-balancers targetGroupArn=...,containerName=api,containerPort=8000
```

---

## SSL/TLS Configuration

### Generate Self-Signed Certificate (Development)
```bash
# Generate private key and certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Move to ssl directory
mkdir -p ssl
mv cert.pem key.pem ssl/
```

### Using Let's Encrypt (Production)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Configure Nginx
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

---

## Database Migration

### Create Migration
```bash
cd backend

# Auto-generate migration
alembic revision --autogenerate -m "Description of changes"

# Review migration file in migrations/versions/

# Apply migration
alembic upgrade head
```

### Backup Before Migration
```bash
# Backup database
pg_dump -U lexshield_user lexshield_ai > backup_$(date +%Y%m%d).sql

# Restore if needed
psql -U lexshield_user lexshield_ai < backup_20240101.sql
```

---

## Monitoring & Logging

### Cloudwatch Logs (AWS)
```bash
# View logs
aws logs tail /aws/ecs/lexshield-api --follow

# Create log group
aws logs create-log-group --log-group-name /lexshield/api
```

### Log Aggregation (ELK Stack)
```bash
# Docker Compose for ELK
docker-compose -f docker-compose.elk.yml up -d

# Access Kibana: http://localhost:5601
```

### Monitoring with Prometheus
```bash
# Configure Prometheus scrape config
scrape_configs:
  - job_name: 'lexshield-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Alerting
```bash
# Configure PagerDuty integration for critical alerts
# Configure Slack notifications for warnings
```

---

## Backup & Recovery

### Automated Backups
```bash
# Database backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/lexshield_db_${TIMESTAMP}.sql"

pg_dump -U lexshield_user -h localhost lexshield_ai | \
  gzip > "${BACKUP_FILE}.gz"

# Upload to S3
aws s3 cp "${BACKUP_FILE}.gz" s3://lexshield-backups/
```

### Recovery Procedure
```bash
# Restore from backup
gunzip backup_20240101.sql.gz
psql -U lexshield_user lexshield_ai < backup_20240101.sql

# Verify integrity
psql -U lexshield_user -c "SELECT COUNT(*) FROM users;"
```

### File Storage Backup
```bash
# Sync S3 uploads to local backup
aws s3 sync s3://lexshield-uploads ./uploads-backup/

# Backup all data
rsync -av /data/uploads/ /backup/uploads/
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
psql -U lexshield_user -h localhost -c "SELECT version();"

# Check connection string
echo $DATABASE_URL

# Test connection
pg_isready -h localhost -U lexshield_user
```

### API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Verify API health
curl http://localhost:8000/health

# Check port binding
netstat -tulpn | grep 8000
```

### High Memory Usage
```bash
# Check container memory
docker stats

# Limit container memory
docker-compose down
# Edit docker-compose.yml - add memory limits
docker-compose up -d
```

---

## Performance Optimization

### Database
```sql
-- Create indexes for common queries
CREATE INDEX idx_document_user_status ON documents(user_id, status);
CREATE INDEX idx_analysis_risk_level ON analyses(risk_level);

-- Vacuum and analyze
VACUUM ANALYZE;
```

### Caching
```python
# Redis caching for API responses
@cache.cached(timeout=3600)
def get_user_documents(user_id: str):
    return ...
```

### CDN Configuration
```bash
# Configure CloudFront for static assets
# Map domain to CloudFront distribution
# Configure cache behaviors
```

---

## Support & Maintenance

For issues or questions, contact the development team.

**Last Updated**: 2024
**Version**: 1.0.0