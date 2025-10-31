# התראות Discord - מדריך מהיר 🔔

## מה זה עושה?

כשהבוט קונה או מוכר SOL, תקבל אוטומטית הודעה ב-Discord עם כל הפרטים:
- 🟢 **קנייה**: כמות, מחיר, סיבה
- 🔴 **מכירה**: כמות, מחיר, רווח/הפסד
- 📊 **סיכום**: סך הכל רווחים והפסדים היום

## איך מגדירים?

### שלב 1: צור Webhook ב-Discord

1. פתח את השרת שלך ב-Discord
2. לחץ לחיצה ימנית על הערוץ שבו אתה רוצה לקבל הודעות
3. **עריכת ערוץ** → **אינטגרציות** → **Webhooks**
4. **New Webhook** (או "יצירת Webhook")
5. תן שם (למשל "בוט מסחר SOL")
6. העתק את **Webhook URL**

### שלב 2: הוסף את ה-URL ל-.env

פתח את הקובץ `.env` והוסף שורה:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1433781062730780682/Smd_T5guackTVHKW6CWGdAGsrqzR-9btTcxNdXaka7XzEOGScfagILbTvjMzl5xAfIVj
```

(החלף את ה-URL בזה שהעתקת משלב 1)

### שלב 3: בדוק שזה עובד

הרץ סקריפט בדיקה:

```bash
python scripts/test_discord_webhook.py
```

אמור להופיע:
```
✅ Test notification sent successfully!
   Check your Discord channel for the message
```

ותקבל הודעת בדיקה ב-Discord!

### שלב 4: הרץ את הבוט

עכשיו כשהבוט רץ ומבצע עסקאות, תקבל אוטומטית התראות:

```bash
python scripts/run_live_bot.py
```

## דוגמאות להודעות

### הודעת קנייה (ירוק)
```
🟢 BUY SIGNAL EXECUTED
Amount: 0.026809 SOL
Price: $186.50
Total Value: $5.00
Details: Price dropped 2.15% from $190.60
         Entry: $186.50
         Position size: $5.00 USDC
```

### הודעת מכירה (אדום)
```
🔴 SELL SIGNAL EXECUTED
Amount: 0.026809 SOL
Price: $190.23
Total Value: $5.10
Details: Entry: $186.50
         Exit: $190.23
         Profit: +$0.10 (+2.00%)
         Received: $5.10 USDC
         Total P&L today: +$0.10
```

## איך לכבות?

אם אתה לא רוצה התראות:
1. מחק או הפוך לhash את השורה `DISCORD_WEBHOOK_URL` ב-`.env`
2. או השאר אותה ריקה: `DISCORD_WEBHOOK_URL=`

הבוט ימשיך לעבוד בלי בעיה, פשוט לא ישלח התראות.

## בעיות נפוצות

### "No webhook URL configured"
- ודא ש-`DISCORD_WEBHOOK_URL` קיים ב-`.env`
- בדוק שה-URL מתחיל ב-`https://discord.com/api/webhooks/`

### "Failed to send notification"
- בדוק שה-URL נכון
- בדוק חיבור לאינטרנט
- ודא שה-Webhook לא נמחק ב-Discord

### ההודעות לא מופיעות
- בדוק שאתה בערוץ הנכון ב-Discord
- ודא שה-Webhook פעיל בהגדרות Discord
- הרץ `test_discord_webhook.py` כדי לבדוק את החיבור

## אבטחה ⚠️

- **אל תשתף** את ה-Webhook URL בשום מקום!
- כל מי שיש לו את ה-URL יכול לשלוח הודעות לערוץ שלך
- הקובץ `.env` לא מועלה ל-Git (הוא ב-`.gitignore`)

## מה הלאה?

✅ בדוק את החיבור עם `test_discord_webhook.py`  
✅ הרץ את הבוט עם `run_live_bot.py`  
📱 תשאיר את Discord פתוח כדי לראות התראות בזמן אמת  
📊 עקוב אחרי הביצועים שלך דרך ההודעות!

בהצלחה! 🚀
