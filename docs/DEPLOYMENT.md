# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- AWS CLI configured
- GitHub account with repository access
- Domain name (production)
- SSL certificate

## Development Deployment (Docker Compose)

### Setup

```bash
# Clone repository
git clone https://github.com/AkhilMadesh/Busibot.git
cd Busibot

# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# PgAdmin: http://localhost:5050
```

### Monitoring

```bash
# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check service health
docker-compose ps

# Run tests
docker-compose exec backend pytest tests/ -v
```

## Production Deployment (AWS)

### Architecture

```
Route 53 (DNS)
    ↓
CloudFront (CDN)
    ↓
Application Load Balancer (ALB)
    ├─ Frontend: CloudFront + S3
    └─ Backend: ECS Fargate Cluster
        ├─ Auto Scaling Group
        ├─ ECS Tasks
        └─ Load Balanced

Data Layer:
├─ RDS PostgreSQL (Multi-AZ)
├─ ElastiCache Redis
└─ S3 (File Storage)
```

### Step 1: Prepare AWS Account

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets (public & private)
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.2.0/24

# Create security groups
aws ec2 create-security-group \
  --group-name busibot-alb \
  --description "ALB Security Group" \
  --vpc-id vpc-xxx
```

### Step 2: Create RDS Database

```bash
aws rds create-db-instance \
  --db-instance-identifier busibot-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password 'SecurePassword123!' \
  --allocated-storage 100 \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name default \
  --multi-az \
  --storage-encrypted
```

### Step 3: Create ElastiCache Redis

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id busibot-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --vpc-security-group-ids sg-xxx
```

### Step 4: Create ECR Repositories

```bash
# Create backend repository
aws ecr create-repository \
  --repository-name busibot-backend \
  --region us-east-1

# Create frontend repository
aws ecr create-repository \
  --repository-name busibot-frontend \
  --region us-east-1

# Build and push images
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin xxxxx.dkr.ecr.us-east-1.amazonaws.com

docker build -t busibot-backend ./backend
docker tag busibot-backend:latest xxxxx.dkr.ecr.us-east-1.amazonaws.com/busibot-backend:latest
docker push xxxxx.dkr.ecr.us-east-1.amazonaws.com/busibot-backend:latest
```

### Step 5: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name busibot-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster busibot-cluster \
  --service-name busibot-backend \
  --task-definition busibot-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=backend,containerPort=8000
```

### Step 6: Setup ALB

```bash
# Create load balancer
aws elbv2 create-load-balancer \
  --name busibot-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx

# Create target group
aws elbv2 create-target-group \
  --name busibot-backend \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxx

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

### Step 7: Deploy Frontend

```bash
# Build frontend
cd frontend
npm run build

# Deploy to S3
aws s3 sync .next/static s3://busibot-frontend-prod/static --delete

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id XXXXX \
  --paths "/*"
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/ -v
      
      - name: Run frontend tests
        run: |
          cd frontend
          npm install
          npm run test
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Build backend image
        run: |
          docker build -t busibot-backend:${{ github.sha }} ./backend
          docker tag busibot-backend:${{ github.sha }} busibot-backend:latest
      
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
          docker push ${{ secrets.ECR_REGISTRY }}/busibot-backend:latest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster busibot-cluster \
            --service busibot-backend \
            --force-new-deployment
```

## Monitoring & Logging

### CloudWatch Setup

```bash
# Create log groups
aws logs create-log-group --log-group-name /busibot/backend
aws logs create-log-group --log-group-name /busibot/frontend

# Setup alarms
aws cloudwatch put-metric-alarm \
  --alarm-name busibot-cpu-high \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### Application Monitoring

```python
# Sentry Setup
import sentry_sdk

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1,
)
```

## Backup Strategy

```bash
# Enable automated backups
aws rds modify-db-instance \
  --db-instance-identifier busibot-db \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00"

# Enable RDS Enhanced Monitoring
aws rds modify-db-instance \
  --db-instance-identifier busibot-db \
  --enable-cloudwatch-logs-exports postgresql
```

## Disaster Recovery

```bash
# Create database snapshot
aws rds create-db-snapshot \
  --db-instance-identifier busibot-db \
  --db-snapshot-identifier busibot-db-snapshot-$(date +%Y-%m-%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier busibot-db-restore \
  --db-snapshot-identifier busibot-db-snapshot-2024-01-15
```

## Cost Optimization

1. **Auto Scaling**
   - Scale down during low traffic
   - Reserved instances for baseline

2. **Storage Optimization**
   - Lifecycle policies for S3
   - Archive old data to Glacier

3. **Database Optimization**
   - Query optimization
   - Connection pooling
   - Read replicas only when needed

---

**Last Updated**: June 2024
**Version**: 1.0.0
