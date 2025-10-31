# 🚀 Solana SOL Trading Bot (2025)

**בוט מסחר אוטומטי לסולנה** עם מחירים חיים, אסטרטגיית קנה-נמוך-מכור-גבוה, ותמיכה ב-Docker.

## ⚡ התחלה מהירה

### אופציה 1: הפעלה רגילה
```powershell
# 1. הגדר .env
Copy-Item .env.example .env
# ערוך .env עם QuickNode RPC + Solflare wallet

# 2. הפעל
python .\scripts\run_live_bot.py
```

### אופציה 2: Docker (מומלץ) 🐋
```powershell
# 1. ודא שDocker Desktop רץ
# 2. הרץ
.\docker_start.ps1
```

📖 **למדריך מפורט:** ראה [SETUP.md](SETUP.md) או [DOCKER_README.md](DOCKER_README.md)

---

## 📦 מה כלול בפרויקט

### 🎯 **קוד ליבה:**
- `backend/core/wallet_manager.py` — ניהול ארנק Solflare + חתימת טרנזקציות
- `backend/core/dynamic_price_feed.py` — **מחירים חיים** מ-Binance/CoinGecko (לא cache!)
- `backend/core/orca_client.py` — אינטגרציה עם Orca DEX
- `backend/core/price_monitor.py` — זיהוי סיגנלים (volume spikes, momentum)
- `scripts/run_live_bot.py` — **הבוט הראשי** - בדיקה כל 20 שניות

### 🐋 **Docker:**
- `Dockerfile` — הגדרת קונטיינר
- `docker-compose.yml` — תזמון הרצה
- `docker_start.ps1` / `docker_stop.ps1` — סקריפטי ניהול

### 📚 **תיעוד:**
- `SETUP.md` — הגדרת QuickNode + Solflare
- `DOCKER_README.md` — הפעלה עם Docker (מדריך מהיר)
- `DOCKER_GUIDE.md` — Docker מתקדם
- `HOW_TO_RUN.md` — כל דרכי ההפעלה
- `CRITICAL_FIXES_2025.md` — תיקונים חשובים ל-solana-py 2025

### ⚙️ **הגדרות:**
- `.env.example` — תבנית להגדרות (העתק ל-`.env`)
- `requirements.txt` — תלויות Python
- `.gitignore` — הגנה מפני commit של סודות

---

## 🎯 איך זה עובד?

הבוט מריץ אסטרטגיה פשוטה אבל יעילה:

```
1. 🔄 מושך מחיר חי של SOL כל 20 שניות
2. 📊 משווה למחירים האחרונים (30 דקות)
3. 📉 קנייה: אם המחיר ירד 2% מהשיא
4. 📈 מכירה: אם המחיר עלה 2% מהקנייה
5. 🛑 Stop Loss: אם המחיר ירד 5% מהקנייה
```

### 💡 **דוגמה:**
```
שיא אחרון: $200
מחיר נוכחי: $196 (ירידה של 2%)
→ 🟢 קנה 1 SOL ב-$196

מחיר עלה ל-$200 (עלייה של 2%)
→ 🔴 מכור 1 SOL ב-$200

רווח: $4 💰
```

---

## 📊 פרמטרים

ניתן לשנות ב-`scripts/run_live_bot.py`:

```python
self.buy_dip_pct = 2.0           # אחוז ירידה לקנייה
self.sell_rise_pct = 2.0         # אחוז עלייה למכירה  
self.stop_loss_pct = 5.0         # Stop loss
self.position_size_usd = 5.0     # גודל עסקה ($5)
self.max_daily_trades = 10       # מקס' עסקאות ביום
```

זמן בדיקה:
```python
time.sleep(20)  # כל 20 שניות (שנה ל-30, 60, וכו')
```

---

## ⚠️ אזהרות חשובות!

---

## ⚠️ אזהרות חשובות!

### 🔴 **הבוט כרגע ב-SIMULATION MODE**
- הוא **לא מבצע עסקאות אמיתיות**
- הוא רק **מראה** מה הוא היה עושה
- בטוח ללמידה ובדיקה

### 🔐 **אבטחה:**
- ✅ **השתמש בארנק TEST בלבד** - לא הארנק הראשי שלך!
- ✅ גבה את ה-Recovery Phrase במקום בטוח
- ✅ **לעולם אל תשתף** את קובץ ה-`.env`
- ✅ בדוק שה-`.env` ב-`.gitignore` לפני commit

### 💰 **סיכונים:**
- מסחר בקריפטו מסוכן - אפשר להפסיד כסף
- התחל עם סכומים **קטנים מאוד** ($1-5)
- בדוק את הלוגים **כל יום**
- אל תשקיע מה שאתה לא יכול להפסיד

---

## 🛠️ פתרון בעיות

### הבוט לא מתחיל:
```powershell
# בדוק Python
python --version  # צריך 3.10+

# בדוק dependencies
pip list

# בדוק .env
Test-Path .env
```

### שגיאת RPC:
- בדוק שה-QuickNode endpoint נכון
- נסה לגשת אליו בדפדפן (אמור להחזיר JSON)

### שגיאת Wallet:
- בדוק ש-WALLET_PRIVATE_KEY_JSON מכיל 64 מספרים
- בדוק שאין רווחים או תווים מוזרים

### Docker לא עובד:
```powershell
# בדוק שDocker רץ
docker version

# בדוק לוגים
docker-compose logs
```

---

## 📚 תיעוד נוסף

| קובץ | תיאור |
|------|--------|
| [SETUP.md](SETUP.md) | הגדרת QuickNode + Solflare (צעד אחר צעד) |
| [DOCKER_README.md](DOCKER_README.md) | הפעלה עם Docker - מדריך מהיר |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Docker מתקדם - כל הפקודות |
| [HOW_TO_RUN.md](HOW_TO_RUN.md) | כל דרכי ההפעלה (ידני, ברקע, Task Scheduler) |
| [CRITICAL_FIXES_2025.md](CRITICAL_FIXES_2025.md) | תיקונים חשובים ל-solana-py 2025 |

---

## 🎯 Roadmap

- [x] מחירים דינמיים בזמן אמת
- [x] אסטרטגיית קנה-נמוך-מכור-גבוה
- [x] תמיכה ב-Docker
- [x] Health checks אוטומטיים
- [ ] ביצוע עסקאות אמיתיות (מצריך הפעלה ידנית)
- [ ] תמיכה ב-multiple pairs (SOL/USDC, SOL/USDT)
- [ ] Telegram notifications
- [ ] Web dashboard

---

## 🤝 תרומה

רוצה לשפר? Pull Requests מתקבלים בברכה!

1. Fork את הפרויקט
2. צור branch חדש (`git checkout -b feature/amazing`)
3. Commit את השינויים (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. פתח Pull Request

---

## 📄 License

MIT License - השתמש על אחריותך בלבד.

---

## ⚡ מהירות התחלה

```powershell
# Clone
git clone <repo-url>
cd Solana_autotrade

# Setup
Copy-Item .env.example .env
# ערוך .env

# Run
python .\scripts\run_live_bot.py

# או עם Docker
.\docker_start.ps1
```

---

**בהצלחה במסחר! 🚀💰**

> ⚠️ **Disclaimer:** פרויקט זה למטרות חינוכיות בלבד. מסחר בקריפטו מסוכן ואתה אחראי לפעולות שלך. תמיד עשה מחקר משלך (DYOR).
