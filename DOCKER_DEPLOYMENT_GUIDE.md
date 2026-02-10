# 🐳 DOCKER PRODUCTION DEPLOYMENT GUIDE

## 📋 Overview

Complete production Docker setup for Nurothon AI SMB system with:
- ✅ **PostgreSQL Database** - Production-grade database
- ✅ **FastAPI Backend** - Python API with AI capabilities
- ✅ **Nginx Frontend** - Static file serving with reverse proxy
- ✅ **One-Command Deployment** - Automated setup script
- ✅ **Health Checks** - Automatic service monitoring
- ✅ **Volume Persistence** - Data survives container restarts

---

## 🚀 QUICK START

### **Windows (PowerShell)**
```powershell
# 1. Copy environment file
Copy-Item .env.production .env

# 2. Edit .env and update passwords
notepad .env

# 3. Deploy
.\deploy.ps1
```

### **Linux/Mac (Bash)**
```bash
# 1. Copy environment file
cp .env.production .env

# 2. Edit .env and update passwords
nano .env

# 3. Deploy
chmod +x deploy.sh
./deploy.sh
```

### **Manual Deployment**
```bash
# Build and start
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 📁 FILES CREATED

```
Dockerfile.backend           # Backend container definition
Dockerfile.frontend          # Frontend container definition
docker-compose.prod.yml      # Production orchestration
nginx.conf                   # Nginx configuration
.env.production              # Environment variables template
.dockerignore                # Docker build exclusions
deploy.sh                    # Linux/Mac deployment script
deploy.ps1                   # Windows deployment script
```

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│                    INTERNET                         │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Nginx Frontend       │
        │   Port: 80, 443        │
        │   (Static Files)       │
        └────────┬───────────────┘
                 │
                 │ /api/* → Proxy
                 ▼
        ┌────────────────────────┐
        │   FastAPI Backend      │
        │   Port: 8000           │
        │   (AI + Business Logic)│
        └────────┬───────────────┘
                 │
                 │ SQL Queries
                 ▼
        ┌────────────────────────┐
        │   PostgreSQL Database  │
        │   Port: 5432           │
        │   (Data Storage)       │
        └────────────────────────┘
```

---

## 🐳 CONTAINERS

### **1. Database (PostgreSQL)**
- **Image**: `postgres:15-alpine`
- **Port**: `5432`
- **Volume**: `postgres_data` (persistent)
- **Health Check**: `pg_isready`
- **Auto-init**: Runs `demo_data.sql` on first start

### **2. Backend (FastAPI)**
- **Build**: `Dockerfile.backend`
- **Port**: `8000`
- **Volumes**: 
  - `invoice_data` - Generated invoices
  - `upload_data` - Uploaded files
- **Health Check**: `/health` endpoint
- **Features**:
  - Tesseract OCR included
  - AI intent detection
  - Invoice generation
  - Multi-language support

### **3. Frontend (Nginx)**
- **Build**: `Dockerfile.frontend`
- **Port**: `80` (HTTP), `443` (HTTPS)
- **Features**:
  - Static file serving
  - Reverse proxy to backend
  - Gzip compression
  - Security headers
  - Caching

---

## ⚙️ ENVIRONMENT VARIABLES

### **Required (Update in .env)**
```bash
# Database
POSTGRES_PASSWORD=CHANGE_THIS_IN_PRODUCTION_123!@#

# Application
SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY_IN_PRODUCTION

# CORS
ALLOWED_ORIGINS=http://localhost,https://yourdomain.com
```

### **Optional**
```bash
# AI Configuration
AI_CONFIDENCE_THRESHOLD=0.7

# Application
APP_ENV=production
DEBUG=false

# Database
POSTGRES_DB=nurothon_db
POSTGRES_USER=nurothon_user
```

---

## 📊 SERVICE URLS

After deployment:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost | Main application |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Database** | localhost:5432 | PostgreSQL |

---

## 🔧 MANAGEMENT COMMANDS

### **View Logs**
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f database
```

### **Stop Services**
```bash
docker-compose -f docker-compose.prod.yml down
```

### **Restart Services**
```bash
# All services
docker-compose -f docker-compose.prod.yml restart

# Specific service
docker-compose -f docker-compose.prod.yml restart backend
```

### **View Status**
```bash
docker-compose -f docker-compose.prod.yml ps
```

### **Execute Commands in Container**
```bash
# Backend shell
docker-compose -f docker-compose.prod.yml exec backend bash

# Database shell
docker-compose -f docker-compose.prod.yml exec database psql -U nurothon_user -d nurothon_db

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head
```

---

## 💾 DATA PERSISTENCE

### **Volumes**
```
postgres_data    # Database files
invoice_data     # Generated invoices
upload_data      # Uploaded files
```

### **Backup Database**
```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec database pg_dump -U nurothon_user nurothon_db > backup.sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T database psql -U nurothon_user nurothon_db < backup.sql
```

### **Backup Volumes**
```bash
# Backup invoices
docker run --rm -v nurothon_invoice_data:/data -v $(pwd):/backup alpine tar czf /backup/invoices_backup.tar.gz -C /data .

# Restore invoices
docker run --rm -v nurothon_invoice_data:/data -v $(pwd):/backup alpine tar xzf /backup/invoices_backup.tar.gz -C /data
```

---

## 🔒 SECURITY CHECKLIST

### **Before Production:**
- [ ] Update `SECRET_KEY` in `.env`
- [ ] Update `POSTGRES_PASSWORD` in `.env`
- [ ] Configure `ALLOWED_ORIGINS` for your domain
- [ ] Set `DEBUG=false`
- [ ] Enable HTTPS (add SSL certificates)
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Enable monitoring/logging
- [ ] Review nginx security headers
- [ ] Implement rate limiting

### **SSL/HTTPS Setup**
```yaml
# Add to frontend service in docker-compose.prod.yml
volumes:
  - ./ssl/cert.pem:/etc/nginx/ssl/cert.pem:ro
  - ./ssl/key.pem:/etc/nginx/ssl/key.pem:ro
```

Update `nginx.conf`:
```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of config
}
```

---

## 🚨 TROUBLESHOOTING

### **Container Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs [service-name]

# Check status
docker-compose -f docker-compose.prod.yml ps

# Rebuild
docker-compose -f docker-compose.prod.yml build --no-cache [service-name]
```

### **Database Connection Issues**
```bash
# Check database is running
docker-compose -f docker-compose.prod.yml exec database pg_isready -U nurothon_user

# Check connection from backend
docker-compose -f docker-compose.prod.yml exec backend python -c "from app.database import engine; print(engine)"
```

### **Port Already in Use**
```bash
# Find process using port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Change port in docker-compose.prod.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### **Permission Issues**
```bash
# Fix volume permissions
docker-compose -f docker-compose.prod.yml exec backend chown -R 1000:1000 /app/invoices
```

---

## 📈 MONITORING

### **Health Checks**
All services have built-in health checks:
```bash
# Check health status
docker-compose -f docker-compose.prod.yml ps
```

### **Resource Usage**
```bash
# View stats
docker stats
```

### **Logs**
```bash
# Follow logs
docker-compose -f docker-compose.prod.yml logs -f --tail=100
```

---

## 🔄 UPDATES & MAINTENANCE

### **Update Application**
```bash
# 1. Pull latest code
git pull

# 2. Rebuild containers
docker-compose -f docker-compose.prod.yml build

# 3. Restart with new images
docker-compose -f docker-compose.prod.yml up -d
```

### **Database Migrations**
```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### **Clean Up**
```bash
# Remove stopped containers
docker-compose -f docker-compose.prod.yml down

# Remove volumes (WARNING: deletes data!)
docker-compose -f docker-compose.prod.yml down -v

# Remove unused images
docker image prune -a
```

---

## 🌐 PRODUCTION DEPLOYMENT

### **Cloud Platforms**

#### **AWS EC2**
```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# 3. Clone repository
git clone your-repo-url
cd Nurothon

# 4. Configure .env
cp .env.production .env
nano .env

# 5. Deploy
./deploy.sh
```

#### **DigitalOcean Droplet**
```bash
# Use Docker Marketplace image
# SSH into droplet
# Clone and deploy as above
```

#### **Google Cloud Run**
```bash
# Build and push images
docker build -f Dockerfile.backend -t gcr.io/PROJECT_ID/nurothon-backend .
docker push gcr.io/PROJECT_ID/nurothon-backend

# Deploy
gcloud run deploy nurothon-backend --image gcr.io/PROJECT_ID/nurothon-backend
```

---

## 📝 NOTES

- **First Run**: Database auto-initializes with `demo_data.sql`
- **Health Checks**: Services wait for dependencies before starting
- **Restart Policy**: Containers auto-restart unless stopped
- **Networking**: All services on isolated `nurothon-network`
- **Volumes**: Data persists across container restarts

---

## 🎯 NEXT STEPS

1. **Deploy**: Run `deploy.ps1` or `deploy.sh`
2. **Access**: Open http://localhost
3. **Test**: Try AI chat features
4. **Monitor**: Check logs and health
5. **Secure**: Update passwords and secrets
6. **Backup**: Set up automated backups
7. **Scale**: Add load balancer if needed

---

**PRODUCTION DOCKER SETUP COMPLETE!** 🐳
