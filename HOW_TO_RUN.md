# 🚀 איך להריץ את בוט המסחר

## 🎯 3 דרכים להפעלה

---

### 1️⃣ **הרצה ידנית (מומלץ להתחלה)**

פשוט תריץ בטרמינל:

```powershell
python .\scripts\run_live_bot.py
```

**✅ יתרונות:**
- רואה הכל בזמן אמת
- שליטה מלאה
- לחיצה על `Ctrl+C` עוצרת את הבוט

**❌ חסרונות:**
- צריך להשאיר את הטרמינל פתוח
- הבוט נעצר אם תסגור את הטרמינל

---

### 2️⃣ **הרצה ברקע (Recommended)**

#### להתחיל את הבוט:
```powershell
.\start_bot.ps1
```

הבוט ירוץ ברקע, גם אם תסגור את הטרמינל!

#### לראות את הלוגים:
```powershell
.\view_logs.ps1
```

או:
```powershell
Get-Content bot_log.txt -Wait
```

#### לעצור את הבוט:
```powershell
.\stop_bot.ps1
```

או באופן ידני:
```powershell
# מצא את ה-Process ID
Get-Content bot_pid.txt

# עצור את התהליך
Stop-Process -Id <PROCESS_ID>
```

---

### 3️⃣ **הפעלה אוטומטית (Task Scheduler)**

הבוט יתחיל אוטומטית עם Windows!

#### ⚠️ **צריך הרשאות Administrator!**

הרץ PowerShell **כ-Administrator** ואז:

```powershell
.\schedule_bot.ps1
```

#### לנהל את ה-Task:

**להתחיל:**
```powershell
Start-ScheduledTask -TaskName "SOL_Trading_Bot"
```

**לעצור:**
```powershell
Stop-ScheduledTask -TaskName "SOL_Trading_Bot"
```

**לבדוק סטטוס:**
```powershell
Get-ScheduledTask -TaskName "SOL_Trading_Bot" | Get-ScheduledTaskInfo
```

**למחוק:**
```powershell
Unregister-ScheduledTask -TaskName "SOL_Trading_Bot" -Confirm:$false
```

---

## 📊 **מה הבוט עושה?**

כל **10 שניות** הבוט:

1. 🔄 מושך מחיר **חי** של SOL מ-Binance
2. 📊 בודק אם יש הזדמנות לקנות/למכור
3. 💡 מציג המלצה + מבקש אישור

### 📈 **אסטרטגיה:**
- **קנייה**: כשהמחיר יורד **2%** מהשיא האחרון
- **מכירה**: כשהמחיר עולה **2%** מהקנייה
- **Stop Loss**: אם המחיר יורד **5%** מהקנייה

### 💰 **סכומים:**
- כל עסקה: **$5 USDC**
- מקסימום ביום: **10 עסקאות**

---

## ⚠️ **אזהרות חשובות!**

### 🔴 **כרגע הבוט במצב SIMULATION!**

הבוט **לא מבצע עסקאות אמיתיות** עדיין!
- הוא רק **מראה** מה הוא היה עושה
- צריך לאשר כל עסקה באופן ידני
- זה בטוח ללמידה ובדיקה

### 🟢 **כדי להפעיל מסחר אמיתי:**

בקובץ `scripts/run_live_bot.py`, צריך:

1. להוסיף קריאה אמיתית ל-DEX swap
2. להסיר את השורה: `print("⚠️ SIMULATION MODE")`
3. **לבדוק היטב עם סכומים קטנים מאוד!**

---

## 📝 **קבצי לוג**

- `bot_log.txt` - פלט רגיל של הבוט
- `bot_log.txt.err` - שגיאות (אם יש)
- `bot_pid.txt` - Process ID (לעצירה)

---

## 🛠️ **פתרון בעיות**

### הבוט לא מתחיל:
```powershell
# בדוק שה-venv פעיל
.venv\Scripts\Activate.ps1

# בדוק שיש את כל הספריות
pip list
```

### הבוט קפא:
```powershell
# מצא תהליכי Python
Get-Process python

# עצור את כולם
Stop-Process -Name python -Force
```

### לא רואה לוגים:
```powershell
# בדוק אם הקובץ קיים
Test-Path bot_log.txt

# הצג תוכן
Get-Content bot_log.txt
```

---

## 💡 **טיפים**

### 🎯 **מצב לימוד (3-7 ימים):**
1. הרץ את הבוט במצב סימולציה
2. בדוק את ההחלטות שלו
3. צפה בלוגים מדי יום
4. תבין את ההיגיון

### 🚀 **מצב אמיתי (אחרי לימוד):**
1. התחל עם **$1-5** לעסקה
2. שים limit של **2-3 עסקאות ביום**
3. בדוק תוצאות כל יום
4. אם זה עובד - העלה בהדרגה

### 🔒 **ביטחון:**
- **אל תשאיר** את המפתח הפרטי בקוד
- השתמש ב-`.env` בלבד
- **גבה** את הארנק לפני שינויים
- התחל עם ארנק **טסט**!

---

## 📞 **תמיכה**

יש בעיה? בדוק:
1. האם ה-RPC של QuickNode עובד?
2. האם יש יתרת SOL בארנק?
3. האם ה-.env מוגדר נכון?

---

**בהצלחה! 🚀💰**
