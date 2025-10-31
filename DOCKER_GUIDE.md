# Docker Management Scripts for SOL Trading Bot

## 🚀 Quick Start

### 1. Build the Docker image
```powershell
docker-compose build
```

### 2. Start the bot
```powershell
docker-compose up -d
```

### 3. View logs
```powershell
docker-compose logs -f sol-trading-bot
```

### 4. Stop the bot
```powershell
docker-compose down
```

---

## 📋 All Commands

### **Build**
```powershell
# Build the image
docker-compose build

# Rebuild without cache (if something changed)
docker-compose build --no-cache
```

### **Start/Stop**
```powershell
# Start in background (detached mode)
docker-compose up -d

# Start in foreground (see logs live)
docker-compose up

# Stop the bot
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### **Logs**
```powershell
# View live logs
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# View logs for specific service
docker-compose logs -f sol-trading-bot
```

### **Status**
```powershell
# Check if running
docker-compose ps

# Check resource usage
docker stats sol_trader

# Health check
docker inspect sol_trader --format='{{.State.Health.Status}}'
```

### **Restart**
```powershell
# Restart the bot
docker-compose restart

# Restart with fresh build
docker-compose down && docker-compose build && docker-compose up -d
```

### **Shell Access**
```powershell
# Open shell inside container
docker exec -it sol_trader /bin/bash

# Run Python command
docker exec -it sol_trader python -c "print('Hello from container!')"

# Check environment
docker exec -it sol_trader env
```

---

## 📊 Monitoring

### **Check Health**
```powershell
docker inspect sol_trader --format='{{json .State.Health}}' | ConvertFrom-Json
```

### **View Resource Usage**
```powershell
docker stats sol_trader --no-stream
```

### **Check Logs Directory**
```powershell
ls .\logs\
Get-Content .\logs\bot.log -Tail 50
```

---

## 🔧 Troubleshooting

### Bot won't start:
```powershell
# Check logs
docker-compose logs sol-trading-bot

# Check if .env exists
Test-Path .env

# Verify build
docker-compose build --no-cache
```

### Container keeps restarting:
```powershell
# Check logs
docker logs sol_trader

# Check health
docker inspect sol_trader

# Run in foreground to see errors
docker-compose up
```

### Update code and restart:
```powershell
# Stop, rebuild, start
docker-compose down
docker-compose build
docker-compose up -d
```

### Clear everything and start fresh:
```powershell
# Stop and remove everything
docker-compose down -v

# Remove image
docker rmi solana_autotrade-sol-trading-bot

# Rebuild and start
docker-compose build --no-cache
docker-compose up -d
```

---

## 📁 File Structure

```
.
├── Dockerfile              # Container definition
├── docker-compose.yml      # Orchestration config
├── .env                    # Environment variables (NEVER commit!)
├── requirements.txt        # Python dependencies
├── logs/                   # Bot logs (mounted volume)
│   ├── heartbeat.txt      # Health check file
│   └── bot.log            # Application logs
├── data/                   # Persistent data (mounted volume)
└── backend/               # Application code
    └── scripts/
```

---

## ⚙️ Configuration

### Change check interval:
Edit `scripts/run_live_bot.py`:
```python
time.sleep(20)  # Change to desired seconds
```

Then rebuild:
```powershell
docker-compose down
docker-compose build
docker-compose up -d
```

### Change resource limits:
Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'    # Increase if needed
      memory: 512M   # Increase if needed
```

Then restart:
```powershell
docker-compose down
docker-compose up -d
```

---

## 🔐 Security Notes

### ⚠️ IMPORTANT:
- `.env` file contains your **private key**
- **NEVER** commit `.env` to Git
- Docker image contains sensitive data
- **NEVER** push image to public registry

### Safe practices:
```powershell
# Check what's being tracked by Git
git status

# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

---

## 🎯 Production Deployment

### Run as Windows Service:
```powershell
# Set restart policy
docker update --restart=always sol_trader
```

### Auto-start with Windows:
1. Install Docker Desktop
2. Enable "Start Docker Desktop when you log in"
3. Set restart policy to "always"

### Backup:
```powershell
# Backup logs
Copy-Item -Recurse logs\ backup_logs_$(Get-Date -Format 'yyyy-MM-dd')\

# Backup .env
Copy-Item .env .env.backup
```

---

## 📈 Advanced Features

### Add monitoring (Prometheus):
Uncomment monitoring section in `docker-compose.yml`

### Multiple bots:
```yaml
# In docker-compose.yml, duplicate service with different name
sol-trading-bot-2:
  extends: sol-trading-bot
  container_name: sol_trader_2
  env_file:
    - .env.bot2  # Different wallet
```

---

**Happy Trading! 🚀💰**
