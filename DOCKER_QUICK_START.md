# 🐳 DOCKER QUICK START

## ⚡ ONE-COMMAND DEPLOYMENT

### **Windows**
```powershell
.\deploy.ps1
```

### **Linux/Mac**
```bash
chmod +x deploy.sh && ./deploy.sh
```

---

## 📋 PREREQUISITES

- ✅ Docker Desktop installed
- ✅ Docker Compose installed
- ✅ 4GB RAM minimum
- ✅ 10GB disk space

---

## 🚀 DEPLOYMENT STEPS

### **1. Setup Environment**
```bash
# Copy template
cp .env.production .env

# Edit passwords (IMPORTANT!)
# - POSTGRES_PASSWORD
# - SECRET_KEY
# - ALLOWED_ORIGINS
```

### **2. Deploy**
```bash
# Windows
.\deploy.ps1

# Linux/Mac
./deploy.sh
```

### **3. Access**
```
Frontend:  http://localhost
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
```

---

## 📊 WHAT GETS DEPLOYED

```
✅ PostgreSQL Database (Port 5432)
✅ FastAPI Backend (Port 8000)
✅ Nginx Frontend (Port 80)
✅ Demo Data Pre-loaded
✅ Health Checks Enabled
✅ Auto-restart Configured
```

---

## 🔧 COMMON COMMANDS

### **View Logs**
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### **Stop All**
```bash
docker-compose -f docker-compose.prod.yml down
```

### **Restart**
```bash
docker-compose -f docker-compose.prod.yml restart
```

### **Status**
```bash
docker-compose -f docker-compose.prod.yml ps
```

---

## 🔒 SECURITY CHECKLIST

Before production:
- [ ] Update `POSTGRES_PASSWORD` in `.env`
- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `ALLOWED_ORIGINS` to your domain
- [ ] Set `DEBUG=false`
- [ ] Enable HTTPS/SSL

---

## 💾 BACKUP DATABASE

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec database pg_dump -U nurothon_user nurothon_db > backup.sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T database psql -U nurothon_user nurothon_db < backup.sql
```

---

## 🚨 TROUBLESHOOTING

### **Port Already in Use**
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### **Container Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs [service]

# Rebuild
docker-compose -f docker-compose.prod.yml build --no-cache
```

### **Database Connection Failed**
```bash
# Check database
docker-compose -f docker-compose.prod.yml exec database pg_isready -U nurothon_user
```

---

## 📁 FILES

```
Dockerfile.backend          # Backend container
Dockerfile.frontend         # Frontend container
docker-compose.prod.yml     # Orchestration
nginx.conf                  # Web server config
.env.production             # Environment template
deploy.sh / deploy.ps1      # Deployment scripts
```

---

## 🎯 QUICK TEST

After deployment:

1. **Open**: http://localhost
2. **Try AI Chat**: "Order 2 laptops for Rahul"
3. **Check Dashboard**: http://localhost/dashboard.html
4. **View API**: http://localhost:8000/docs

---

## 📚 FULL DOCUMENTATION

See `DOCKER_DEPLOYMENT_GUIDE.md` for:
- Architecture details
- Advanced configuration
- Production deployment
- Monitoring & scaling
- Security hardening

---

**DEPLOY IN 1 COMMAND!** 🚀

```powershell
# Windows
.\deploy.ps1

# Linux/Mac
./deploy.sh
```
