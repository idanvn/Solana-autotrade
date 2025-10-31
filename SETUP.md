# 🔧 הגדרת סביבת העבודה

## 📋 שלב 1: העתק את קובץ הדוגמה

```powershell
Copy-Item .env.example .env
```

---

## 🔑 שלב 2: הגדר QuickNode RPC

### 2.1 צור חשבון ב-QuickNode (חינם)
1. לך ל: https://www.quicknode.com/
2. לחץ "Start for Free"
3. צור חשבון חדש

### 2.2 צור Endpoint
1. בחר **Solana** → **Mainnet**
2. לחץ "Create Endpoint"
3. העתק את ה-HTTP Provider URL

### 2.3 הדבק ב-.env
פתח את `.env` והדבק:
```
RPC_URL=https://your-endpoint.solana-mainnet.quiknode.pro/your-api-key
```

---

## 💼 שלב 3: הגדר ארנק Solflare

### ⚠️ **חשוב מאוד: השתמש בארנק TEST בלבד!**

### 3.1 צור ארנק חדש (או השתמש בקיים)
1. פתח את Solflare Extension
2. צור ארנק חדש ל-Testing
3. שמור את ה-Recovery Phrase במקום בטוח!

### 3.2 ייצוא המפתח הפרטי
1. Solflare → **Settings** (⚙️)
2. **Export Private Key**
3. בחר **Array Format**
4. תראה משהו כזה:
   ```
   [216,151,25,177,61,255,244,...]
   ```

### 3.3 הדבק ב-.env
העתק את כל המערך והדבק:
```
WALLET_PRIVATE_KEY_JSON=[216,151,25,177,...]
```

### 3.4 טען SOL לארנק (אופציונלי)
- לפחות **0.05 SOL** עבור transaction fees
- אם רוצה לסחור: תוסיף USDC

---

## ✅ שלב 4: בדיקה

הרץ:
```powershell
.\docker_check.ps1
```

אם הכל ירוק ✅ - אתה מוכן!

---

## 🔐 אבטחה

### ❌ **לעולם אל תעשה את זה:**
- לא לשתף את קובץ ה-`.env`
- לא ל-commit ל-Git
- לא להעלות לפורומים/Discord

### ✅ **תמיד:**
- השתמש בארנק TEST
- גבה את ה-Recovery Phrase
- בדוק שה-`.env` ב-`.gitignore`

---

## 📁 מבנה הקבצים שלך:

```
.
├── .env.example          ← דוגמה (בטוח לשתף)
├── .env                  ← שלך (אל תשתף!)
├── .gitignore           ← וודא ש-.env פה!
└── ...
```

---

## 🆘 פתרון בעיות

### "RPC error" או "connection failed":
- בדוק שה-QuickNode endpoint נכון
- נסה לגשת לו בדפדפן (אמור להחזיר JSON)

### "Keypair not loaded":
- בדוק שיש 64 מספרים במערך
- בדוק שאין רווחים או תווים מוזרים

### "Insufficient balance":
- טען SOL לארנק
- לפחות 0.05 SOL

---

**מוכן? המשך ל-** `DOCKER_README.md` **או** `HOW_TO_RUN.md`
