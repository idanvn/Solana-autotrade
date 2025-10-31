# 🐋 הפעלת הבוט עם Docker - מדריך מהיר

## ⚡ התחלה מהירה (3 שלבים)

### 1️⃣ וודא ש-Docker רץ
- פתח **Docker Desktop**
- חכה שיהיה "Docker Desktop is running"

### 2️⃣ בדוק שיש `.env`
הקובץ `.env` חייב להכיל:
```
RPC_URL=https://your-quicknode-url...
WALLET_PRIVATE_KEY_JSON=[1,2,3,...]
```

### 3️⃣ הרץ!
```powershell
.\docker_start.ps1
```

**זהו! הבוט רץ! 🚀**

---

## 📋 פקודות שימושיות

### **התחל את הבוט**
```powershell
.\docker_start.ps1
```
או
```powershell
docker-compose up -d
```

### **עצור את הבוט**
```powershell
.\docker_stop.ps1
```
או
```powershell
docker-compose down
```

### **צפה בלוגים**
```powershell
.\docker_logs.ps1 -Follow
```
או
```powershell
docker-compose logs -f
```

### **בדוק סטטוס**
```powershell
docker-compose ps
```

### **אתחל מחדש**
```powershell
docker-compose restart
```

---

## 🔄 עדכון הבוט

אם שינית קוד:

```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 מה קורה בפנים?

הבוט:
- ✅ בודק מחיר של SOL כל **20 שניות**
- ✅ מחפש הזדמנויות לקנות/למכור
- ✅ שומר לוגים ב-`logs/`
- ✅ מתאושש אוטומטית אם קורסס
- ✅ משתמש ב-**מחירים חיים** מ-Binance

---

## ⚙️ הגדרות

### שינוי זמן בדיקה:
ערוך `scripts/run_live_bot.py`:
```python
time.sleep(20)  # שנה ל-30, 60, וכו'
```

אחר כך:
```powershell
docker-compose down
docker-compose build
docker-compose up -d
```

### שינוי אסטרטגיה:
ערוך `scripts/run_live_bot.py`:
```python
self.buy_dip_pct = 2.0       # אחוז ירידה לקנייה
self.sell_rise_pct = 2.0     # אחוז עלייה למכירה
self.position_size_usd = 5.0  # גודל עסקה
```

---

## 🔍 פתרון בעיות

### הבוט לא מתחיל:
```powershell
# בדוק לוגים
docker-compose logs

# בדוק ש-.env קיים
Test-Path .env
```

### רוצה לראות מה קורה:
```powershell
# הרץ בחזית (לא ברקע)
docker-compose up
```

### רוצה להתחיל מחדש מאפס:
```powershell
docker-compose down -v
docker rmi solana_autotrade-sol-trading-bot
docker-compose build --no-cache
docker-compose up -d
```

---

## 💾 גיבוי

הלוגים נשמרים ב-`logs/` על המחשב שלך.

לגבות:
```powershell
Copy-Item -Recurse logs\ backup_logs_$(Get-Date -Format 'yyyy-MM-dd')\
```

---

## 🚀 הפעלה אוטומטית עם Windows

Docker Desktop יכול להתחיל אוטומטית:
1. פתח Docker Desktop Settings
2. General → Start Docker Desktop when you log in ✅
3. הרץ את הפקודה:
```powershell
docker update --restart=always sol_trader
```

עכשיו הבוט יתחיל אוטומטית כל פעם שהמחשב נדלק! 🎉

---

## ⚠️ זכור!

- 🔴 הבוט ב-**SIMULATION MODE** - לא מבצע עסקאות אמיתיות
- 🔴 בדוק את הלוגים כל יום
- 🔴 אל תחשוף את ה-`.env` file!

---

**לתיעוד מלא:** ראה `DOCKER_GUIDE.md`

**בהצלחה! 💰🚀**
